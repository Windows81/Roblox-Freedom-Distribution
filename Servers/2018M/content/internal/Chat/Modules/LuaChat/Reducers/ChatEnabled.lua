local CoreGui = game:GetService("CoreGui")
local Modules = CoreGui.RobloxGui.Modules

local SetChatEnabled = require(Modules.LuaChat.Actions.SetChatEnabled)

return function(state, action)
	state = (state == nil) and true or state

	if action.type == SetChatEnabled.name then
		return action.value
	end

	return state
end