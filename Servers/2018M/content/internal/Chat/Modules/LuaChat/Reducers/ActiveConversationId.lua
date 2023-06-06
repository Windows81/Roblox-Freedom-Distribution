local CoreGui = game:GetService("CoreGui")
local Modules = CoreGui.RobloxGui.Modules

local SetActiveConversationId = require(Modules.LuaChat.Actions.SetActiveConversationId)

return function(state, action)
	state = state or {}

	if action.type == SetActiveConversationId.name then
		return action.conversationId
	end

	return state
end