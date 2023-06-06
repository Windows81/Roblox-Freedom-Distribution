local Modules = game:GetService("CoreGui").RobloxGui.Modules

local ToggleChatPaused = require(Modules.LuaChat.Actions.ToggleChatPaused)

return function(state, action)
	state = state or false

	if action.type == ToggleChatPaused.name then
		state = action.value
	end

	return state
end