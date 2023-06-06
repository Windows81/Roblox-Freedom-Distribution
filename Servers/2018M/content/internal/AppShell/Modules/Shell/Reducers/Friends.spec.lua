return function()
	local FriendsReducer = require(script.Parent.Friends)
	local Actions = script.Parent.Parent.Actions

	local SetFriendsData = require(Actions.SetFriendsData)

	describe("initial state", function()
		it("should return an table when passed nil", function()
			local state = FriendsReducer(nil, {})
			expect(state).to.be.a("table")
		end)

		it("should set initial values when passed nil", function()
			local state = FriendsReducer(nil, {})
			expect(state.initialized).to.be.a("boolean")
			expect(state.initialized).to.equal(false)
			expect(state.data).to.be.a("table")
			expect(#state.data).to.equal(0)
		end)
	end)

	describe("Action SetFriendsData", function()
		it("should initialize friends in data", function()
			local action = SetFriendsData({ {}, {} })
			local state = FriendsReducer(nil, action)

			expect(state.data).to.be.a("table")
			expect(state.data[2]).to.be.a("table")
			expect(state.initialized).to.equal(true)
		end)

		it("should put friend data into the entries", function()
			local action = SetFriendsData({ { xuid=12345, robloxName="TestName", xboxStatus="online" } })
			local state = FriendsReducer(nil, action)

			expect(state.data[1].xuid).to.be.a("number")
			expect(state.data[1].xuid).to.equal(12345)
			expect(state.data[1].robloxName).to.be.a("string")
			expect(state.data[1].robloxName).to.equal("TestName")
		end)

		it("should clear the friends array when passed an empty table", function()
			local action = SetFriendsData({ { xuid=12345, robloxName="TestName", xboxStatus="online" } })
			local state = FriendsReducer(nil, action)

			action = SetFriendsData({})
			state = FriendsReducer(state, action)

			expect(state.data).to.be.a("table")
			expect(#state.data).to.equal(0)
		end)

		it("should reset the state when passed a nil SetFriendsData action", function()
			local action = SetFriendsData({ { xuid=12345, robloxName="TestName", xboxStatus="online" } })
			local state = FriendsReducer(nil, action)
			action = SetFriendsData(nil)
			state = FriendsReducer(state, action)

			expect(state.initialized).to.be.a("boolean")
			expect(state.initialized).to.equal(false)
			expect(state.data).to.be.a("table")
			expect(#state.data).to.equal(0)
		end)
	end)
end