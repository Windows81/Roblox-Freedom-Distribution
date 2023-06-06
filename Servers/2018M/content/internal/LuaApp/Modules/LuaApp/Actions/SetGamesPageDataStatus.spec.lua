return function()
	local SetGamesPageDataStatus = require(script.Parent.SetGamesPageDataStatus)

	it("should assert if given a non-string for status", function()
		SetGamesPageDataStatus("hello")

		expect(function()
			SetGamesPageDataStatus(nil)
		end).to.throw()
	end)
end