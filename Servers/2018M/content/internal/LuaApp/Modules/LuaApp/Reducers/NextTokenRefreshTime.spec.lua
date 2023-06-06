return function()
	local Modules = game:GetService("CoreGui"):FindFirstChild("RobloxGui").Modules
	local NextTokenRefreshTime = require(script.parent.NextTokenRefreshTime)
	local SetNextTokenRefreshTime = require(Modules.LuaApp.Actions.SetNextTokenRefreshTime)

	it("Should not be mutated by other actions", function()
		local oldState = NextTokenRefreshTime(nil, {})
		local newState = NextTokenRefreshTime(oldState, { type = "not a real action" })
		expect(oldState).to.equal(newState)
	end)

	describe("SetNextTokenRefreshTime", function()
		it("should preserve purity", function()
			local oldState = NextTokenRefreshTime(nil, {})
			local newState = NextTokenRefreshTime(oldState, SetNextTokenRefreshTime("Games", 10))
			expect(oldState).to.never.equal(newState)
		end)

		it("should correctly update next token refresh time", function()
			local oldState = NextTokenRefreshTime(nil, {})
			local newState = NextTokenRefreshTime(oldState, SetNextTokenRefreshTime("Games", 10))
			expect(newState["Games"]).to.equal(10)
		end)
	end)
end