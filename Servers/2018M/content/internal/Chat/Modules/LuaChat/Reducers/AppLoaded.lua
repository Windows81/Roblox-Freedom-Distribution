local CoreGui = game:GetService("CoreGui")
local Modules = CoreGui.RobloxGui.Modules

local SetAppLoaded = require(Modules.LuaChat.Actions.SetAppLoaded)

return function(state, action)
	state = state or false

	if action.type == SetAppLoaded.name then
		return action.value
	end

	return state
end