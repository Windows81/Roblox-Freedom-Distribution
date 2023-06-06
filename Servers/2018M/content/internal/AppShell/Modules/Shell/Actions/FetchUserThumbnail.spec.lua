return function()
	it("should return a table", function()
		local action = require(script.Parent.FetchUserThumbnail)

		expect(action).to.be.a("table")
	end)

	it("should return a table when called as a function", function()
		local action = require(script.Parent.FetchUserThumbnail)()

		expect(action).to.be.a("table")
	end)

	it("should set the name", function()
		local action = require(script.Parent.FetchUserThumbnail)

		expect(action.name).to.equal("FetchUserThumbnail")
	end)

	it("should set the rbxuid, thumbnailType and thumbnailSize", function()
		local action = require(script.Parent.FetchUserThumbnail)(
		{
			rbxuid = 12345,
			thumbnailType = Enum.ThumbnailType.HeadShot,
			thumbnailSize = Enum.ThumbnailSize.Size180x180
		})


		expect(action.rbxuid).to.equal(12345)
		expect(action.thumbnailType).to.equal(Enum.ThumbnailType.HeadShot)
		expect(action.thumbnailSize).to.equal(Enum.ThumbnailSize.Size180x180)
	end)

	it("should set the type", function()
		local action = require(script.Parent.FetchUserThumbnail)()

		expect(action.type).to.equal("FetchUserThumbnail")
	end)
end