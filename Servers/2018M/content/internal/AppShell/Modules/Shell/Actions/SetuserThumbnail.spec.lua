return function()
	it("should return a table", function()
		local action = require(script.Parent.SetUserThumbnail)

		expect(action).to.be.a("table")
	end)

	it("should return a table when called as a function", function()
		local action = require(script.Parent.SetUserThumbnail)(
		{
			success = true,
			rbxuid = 12345,
			imageUrl = "x",
			thumbnailType = Enum.ThumbnailType.HeadShot,
			thumbnailSize = Enum.ThumbnailSize.Size180x180,
			isFinal = true,
			timestamp = 10
		})

		expect(action).to.be.a("table")
	end)

	it("should set the name", function()
		local action = require(script.Parent.SetUserThumbnail)

		expect(action.name).to.equal("SetUserThumbnail")
	end)

	it("should set the success, rbxuid, imageUrl, thumbnailType, thumbnailSize and isFinal values", function()
		local action = require(script.Parent.SetUserThumbnail)(
		{
			rbxuid = 12345,
			thumbnailType = Enum.ThumbnailType.HeadShot,
			thumbnailSize = Enum.ThumbnailSize.Size180x180,
			success = true,
			imageUrl = "x",
			isFinal = true,
			timestamp = 10
		})

		expect(action.success).to.equal(true)
		expect(action.rbxuid).to.equal(12345)
		expect(action.imageUrl).to.equal("x")
		expect(action.thumbnailType).to.equal(Enum.ThumbnailType.HeadShot)
		expect(action.thumbnailSize).to.equal(Enum.ThumbnailSize.Size180x180)
		expect(action.isFinal).to.equal(true)
		expect(action.timestamp).to.equal(10)
	end)

	it("should set the success, rbxuid, imageUrl, thumbnailType, thumbnailSize and isFinal to nil if passed an empty table", function()
		local action = require(script.Parent.SetUserThumbnail)({})

		expect(action.success).never.to.be.ok()
		expect(action.rbxuid).never.to.be.ok()
		expect(action.imageUrl).never.to.be.ok()
		expect(action.thumbnailType).never.to.be.ok()
		expect(action.thumbnailSize).never.to.be.ok()
		expect(action.isFinal).never.to.be.ok()
	end)

	it("should set the type", function()
		local action = require(script.Parent.SetUserThumbnail)({})
		expect(action.type).to.equal("SetUserThumbnail")
	end)
end