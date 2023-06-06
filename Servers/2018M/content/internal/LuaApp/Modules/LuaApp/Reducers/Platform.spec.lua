return function()
	local Modules = game:GetService("CoreGui"):FindFirstChild("RobloxGui").Modules
	local SetPlatform = require(Modules.LuaApp.Actions.SetPlatform)

	local PlatformReducer = require(Modules.LuaApp.Reducers.Platform)

	describe("Platform", function()
		it("should be none by default", function()
			local state = PlatformReducer(nil, {})

			expect(state).to.equal(Enum.Platform.None)
		end)

		it("should be unmodified by other actions", function()
			local oldState = PlatformReducer(nil, {})
			local newState = PlatformReducer(oldState, { type = "not a real action" })

			expect(oldState).to.equal(newState)
		end)

		it("should be changed using SetPlatform", function()
			local state = PlatformReducer(nil, {})

			state = PlatformReducer(state, SetPlatform(Enum.Platform.IOS))
			expect(state).to.equal(Enum.Platform.IOS)

			state = PlatformReducer(state, SetPlatform(Enum.Platform.Android))
			expect(state).to.equal(Enum.Platform.Android)
		end)
	end)

end