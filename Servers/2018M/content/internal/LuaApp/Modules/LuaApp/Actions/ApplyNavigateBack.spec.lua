return function()
	local ApplyNavigateBack = require(script.Parent.ApplyNavigateBack)

	it("should assert if given a non-nil non-number for navLockEndTime", function()
		ApplyNavigateBack(nil)
		ApplyNavigateBack(0)

		expect(function()
			ApplyNavigateBack("Blargle!")
		end).to.throw()

		expect(function()
			ApplyNavigateBack({})
		end).to.throw()

		expect(function()
			ApplyNavigateBack(false)
		end).to.throw()

		expect(function()
			ApplyNavigateBack(function() end)
		end).to.throw()
	end)
end