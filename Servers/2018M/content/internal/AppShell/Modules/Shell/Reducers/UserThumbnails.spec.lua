return function()
	local UserThumbnailsReducer = require(script.Parent.UserThumbnails)
	local Actions = script.Parent.Parent.Actions

	local FetchUserThumbnail = require(Actions.FetchUserThumbnail)
	local SetUserThumbnail = require(Actions.SetUserThumbnail)
	local ResetUserThumbnails = require(Actions.ResetUserThumbnails)

	describe("initial state", function()
		it("should return an initial table when passed nil", function()
			local state = UserThumbnailsReducer(nil, {})
			expect(state).to.be.a("table")
		end)
	end)

	describe("Action FetchUserThumbnail", function()
		it("should set the user's thumbnail table based on rbxuid, thumbnailType and thumbnailSize, make the isFetching to be true", function()
			local action = FetchUserThumbnail({ rbxuid = 12345, thumbnailType = Enum.ThumbnailType.AvatarThumbnail, thumbnailSize = Enum.ThumbnailSize.Size420x420 })
			local state = UserThumbnailsReducer(nil, action)
			local thumbnailId = table.concat{ action.rbxuid, action.thumbnailType.Name, action.thumbnailSize.Name }

			expect(state).to.be.a("table")
			expect(state[thumbnailId]).to.be.a("table")
			expect(state[thumbnailId].isFetching).to.equal(true)
		end)

		it("should concat the thumbnail tables", function()
			local thumbnailIds = {}
			local action = FetchUserThumbnail({ rbxuid = 12345, thumbnailType = Enum.ThumbnailType.AvatarThumbnail, thumbnailSize = Enum.ThumbnailSize.Size420x420 })
			table.insert(thumbnailIds, table.concat{ action.rbxuid, action.thumbnailType.Name, action.thumbnailSize.Name })

			local state = UserThumbnailsReducer(nil, action)
			action = FetchUserThumbnail({ rbxuid = 12345, thumbnailType = Enum.ThumbnailType.HeadShot, thumbnailSize = Enum.ThumbnailSize.Size180x180 })
			table.insert(thumbnailIds, table.concat{ action.rbxuid, action.thumbnailType.Name, action.thumbnailSize.Name })

			state = UserThumbnailsReducer(state, action)
			action = FetchUserThumbnail({ rbxuid = 12345, thumbnailType = Enum.ThumbnailType.AvatarThumbnail, thumbnailSize = Enum.ThumbnailSize.Size180x180 })
			table.insert(thumbnailIds, table.concat{ action.rbxuid, action.thumbnailType.Name, action.thumbnailSize.Name })

			state = UserThumbnailsReducer(state, action)
			action = FetchUserThumbnail({ rbxuid = 54321, thumbnailType = Enum.ThumbnailType.AvatarThumbnail, thumbnailSize = Enum.ThumbnailSize.Size180x180 })
			table.insert(thumbnailIds, table.concat{ action.rbxuid, action.thumbnailType.Name, action.thumbnailSize.Name })
			state = UserThumbnailsReducer(state, action)

			expect(state).to.be.a("table")
			for _, thumbnailId in ipairs(thumbnailIds) do
				expect(state[thumbnailId]).to.be.a("table")
				expect(state[thumbnailId].isFetching).to.equal(true)
			end
		end)
	end)

	describe("Action SetUserThumbnail", function()
		it("should set the user's thumbnail table based on rbxuid, fetchSuccess, lastUpdated, thumbnailTypeand thumbnailSize, make the isFetching to be false and set thumbnail assets if fetch success and is final image",
		function()
			local action = SetUserThumbnail(
			{
				rbxuid = 12345,
				thumbnailType = Enum.ThumbnailType.HeadShot,
				thumbnailSize = Enum.ThumbnailSize.Size180x180,
				success = true,
				isFinal = true,
				imageUrl = "x",
				timestamp = tick()
			})
			local thumbnailId = table.concat{ action.rbxuid, action.thumbnailType.Name, action.thumbnailSize.Name }
			local state = UserThumbnailsReducer(nil, action)

			expect(state).to.be.a("table")
			expect(state[thumbnailId]).to.be.a("table")
			expect(state[thumbnailId].isFetching).to.equal(false)
			expect(state[thumbnailId].fetchSuccess).to.equal(true)
			expect(state[thumbnailId].imageUrl).to.equal("x")
			expect(state[thumbnailId].lastUpdated).to.be.a("number")
		end)

		it("should set the user's thumbnail table based on rbxuid, fetchSuccess, lastUpdated, thumbnailType and thumbnailSize, make the isFetching to be false w/o set thumbnail assets if fetch failed or isn't final image",
		function()
			local action = SetUserThumbnail(
			{
				rbxuid = 12345,
				thumbnailType = Enum.ThumbnailType.HeadShot,
				thumbnailSize = Enum.ThumbnailSize.Size180x180,
				success = true,
				isFinal = false,
				imageUrl = "y",
				timestamp = tick()
			})
			local thumbnailId = table.concat{ action.rbxuid, action.thumbnailType.Name, action.thumbnailSize.Name }
			local state = UserThumbnailsReducer(nil, action)
			expect(state).to.be.a("table")
			expect(state[thumbnailId]).to.be.a("table")
			expect(state[thumbnailId].isFetching).to.equal(false)
			expect(state[thumbnailId].fetchSuccess).to.equal(false)
			expect(state[thumbnailId].imageUrl).never.to.be.ok()
			expect(state[thumbnailId].lastUpdated).to.be.a("number")

			action = SetUserThumbnail(
			{
				rbxuid = 12345,
				thumbnailType = Enum.ThumbnailType.HeadShot,
				thumbnailSize = Enum.ThumbnailSize.Size180x180,
				success = true,
				isFinal = true,
				imageUrl = "x",
				timestamp = tick()
			})
			thumbnailId = table.concat{ action.rbxuid, action.thumbnailType.Name, action.thumbnailSize.Name }
			state = UserThumbnailsReducer(state, action)
			expect(state).to.be.a("table")
			expect(state[thumbnailId]).to.be.a("table")
			expect(state[thumbnailId].isFetching).to.equal(false)
			expect(state[thumbnailId].fetchSuccess).to.equal(true)
			expect(state[thumbnailId].imageUrl).to.equal("x")
			expect(state[thumbnailId].lastUpdated).to.be.a("number")

			action = SetUserThumbnail(
			{
				rbxuid = 12345,
				thumbnailType = Enum.ThumbnailType.HeadShot,
				thumbnailSize = Enum.ThumbnailSize.Size180x180,
				success = false,
				timestamp = tick()
			})
			thumbnailId = table.concat{ action.rbxuid, action.thumbnailType.Name, action.thumbnailSize.Name }
			state = UserThumbnailsReducer(state, action)
			expect(state).to.be.a("table")
			expect(state[thumbnailId]).to.be.a("table")
			expect(state[thumbnailId].isFetching).to.equal(false)
			expect(state[thumbnailId].fetchSuccess).to.equal(false)
			expect(state[thumbnailId].imageUrl).to.equal("x")
			expect(state[thumbnailId].lastUpdated).to.be.a("number")

			action = SetUserThumbnail(
			{
				rbxuid = 12345,
				thumbnailType = Enum.ThumbnailType.HeadShot,
				thumbnailSize = Enum.ThumbnailSize.Size180x180,
				success = true,
				isFinal = false,
				imageUrl = "y",
				timestamp = tick()
			})
			thumbnailId = table.concat{ action.rbxuid, action.thumbnailType.Name, action.thumbnailSize.Name }
			state = UserThumbnailsReducer(state, action)
			expect(state).to.be.a("table")
			expect(state[thumbnailId]).to.be.a("table")
			expect(state[thumbnailId].isFetching).to.equal(false)
			expect(state[thumbnailId].fetchSuccess).to.equal(false)
			expect(state[thumbnailId].imageUrl).to.equal("x")
			expect(state[thumbnailId].lastUpdated).to.be.a("number")
		end)
	end)

	describe("Action ResetUserThumbnails", function()
		it("should reset the state to initial state after reset", function()
			local action = FetchUserThumbnail({ rbxuid = 12345, thumbnailType = Enum.ThumbnailType.HeadShot, thumbnailSize = Enum.ThumbnailSize.Size180x180 })
			local state = UserThumbnailsReducer(nil, action)
			action = ResetUserThumbnails()
			state = UserThumbnailsReducer(state, action)

			expect(state).to.be.a("table")
			expect(next(state)).never.to.be.ok()

			action = SetUserThumbnail(
			{
				rbxuid = 12345,
				thumbnailType = Enum.ThumbnailType.HeadShot,
				thumbnailSize = Enum.ThumbnailSize.Size180x180,
				success = true,
				isFinal = true,
				imageUrl = "x",
				timestamp = tick()
			})
			state = UserThumbnailsReducer(nil, action)
			action = ResetUserThumbnails()
			state = UserThumbnailsReducer(state, action)

			expect(state).to.be.a("table")
			expect(next(state)).never.to.be.ok()
		end)
	end)
end