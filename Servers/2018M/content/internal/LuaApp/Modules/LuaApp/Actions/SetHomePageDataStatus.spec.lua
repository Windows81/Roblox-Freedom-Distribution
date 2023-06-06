return function()
	local SetHomePageDataStatus = require(script.Parent.SetHomePageDataStatus)

	it("should assert if given a non-string for status", function()
		SetHomePageDataStatus("hello")

		expect(function()
			SetHomePageDataStatus(nil)
		end).to.throw()
	end)
end