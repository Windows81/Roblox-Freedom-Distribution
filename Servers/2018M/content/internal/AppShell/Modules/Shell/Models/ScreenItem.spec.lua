return function()
	local ScreenItem = require(script.Parent.ScreenItem)

	it("should create without errors", function()
		ScreenItem.new("foo", 1, {})
	end)

	it("should set fields without errors", function()
		local screenItem = ScreenItem.new("foo", 1, {})

		expect(screenItem).to.be.a("table")
		expect(screenItem.id).to.equal("foo")
		expect(screenItem.priority).to.equal(1)
		expect(screenItem.data).to.be.a("table")
		expect(screenItem.createdAt).to.be.a("number")
	end)
end