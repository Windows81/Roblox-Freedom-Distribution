return function()
	it("should return a table", function()
		local action = require(script.Parent.ResetUserThumbnails)

		expect(action).to.be.a("table")
	end)

	it("should return a table when called as a function", function()
		local action = require(script.Parent.ResetUserThumbnails)()

		expect(action).to.be.a("table")
	end)

	it("should set the name", function()
		local action = require(script.Parent.ResetUserThumbnails)

		expect(action.name).to.equal("ResetUserThumbnails")
	end)

	it("should set the type", function()
		local action = require(script.Parent.ResetUserThumbnails)()

		expect(action.type).to.equal("ResetUserThumbnails")
	end)
end