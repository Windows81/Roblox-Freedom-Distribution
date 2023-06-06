local Modules = game:GetService("CoreGui").RobloxGui.Modules
local SetScreenSize = require(Modules.LuaApp.Actions.SetScreenSize)

return function(state, action)
	state = state or Vector2.new(0, 0)

	if action.type == SetScreenSize.name then
		return action.screenSize
	end

	return state
end