return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local LuaApp = Modules.LuaApp

	local TabBarVisible = require(LuaApp.Reducers.TabBarVisible)
	local SetTabBarVisible = require(LuaApp.Actions.SetTabBarVisible)

	describe("Action TabBarVisible", function()
		it("sets the TabBarVisible flag", function()
			local state = TabBarVisible(nil, {})

			expect(state).to.equal(true)

			state = TabBarVisible(state, SetTabBarVisible(false))

			expect(state).to.equal(false)

			state = TabBarVisible(state, SetTabBarVisible(true))

			expect(state).to.equal(true)
		end)
	end)
end