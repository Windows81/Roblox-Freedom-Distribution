return function()
	it("should return a table", function()
		local action = require(script.Parent.SetCrossPlayEnabled)

		expect(action).to.be.a("table")
	end)

	it("should return a table when called as a function", function()
		local action = require(script.Parent.SetCrossPlayEnabled)()

		expect(action).to.be.a("table")
	end)

	it("should set the name", function()
		local action = require(script.Parent.SetCrossPlayEnabled)

		expect(action.name).to.equal("SetCrossPlayEnabled")
	end)

	it("should set the enabled value and timestamp", function()
		local action = require(script.Parent.SetCrossPlayEnabled)(true, 10)

		expect(action.enabled).to.equal(true)
		expect(action.timestamp).to.equal(10)
	end)

	it("should set the type", function()
		local action = require(script.Parent.SetCrossPlayEnabled)()

		expect(action.type).to.equal("SetCrossPlayEnabled")
	end)
end