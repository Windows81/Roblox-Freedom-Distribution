local Modules = game:GetService("CoreGui").RobloxGui.Modules
local SetTabBarVisible = require(Modules.LuaApp.Actions.SetTabBarVisible)

return function(state, action)
	if state == nil then
		state = true
	end

	if action.type == SetTabBarVisible.name then
		state = action.isVisible
	end

	return state
end