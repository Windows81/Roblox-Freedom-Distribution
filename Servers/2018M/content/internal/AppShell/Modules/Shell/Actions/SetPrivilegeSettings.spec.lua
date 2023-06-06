return function()
	it("should return a table", function()
		local action = require(script.Parent.SetPrivilegeSettings)

		expect(action).to.be.a("table")
	end)

	it("should return a table when called as a function", function()
		local action = require(script.Parent.SetPrivilegeSettings)()

		expect(action).to.be.a("table")
	end)

	it("should set the name", function()
		local action = require(script.Parent.SetPrivilegeSettings)

		expect(action.name).to.equal("SetPrivilegeSettings")
	end)

	it("should set the privilege settings and timestamp", function()
		local action = require(script.Parent.SetPrivilegeSettings)({Multiplayer = {}, SharedContent = {}, timestamp = 10})

		expect(action.Multiplayer).to.be.a("table")
		expect(action.SharedContent).to.be.a("table")
		expect(action.timestamp).to.equal(10)
	end)

	it("should set the type", function()
		local action = require(script.Parent.SetPrivilegeSettings)()

		expect(action.type).to.equal("SetPrivilegeSettings")
	end)
end