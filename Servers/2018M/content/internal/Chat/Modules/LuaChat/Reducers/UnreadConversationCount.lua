local Modules = game:GetService("CoreGui").RobloxGui.Modules

local SetUnreadConversationCount = require(Modules.LuaChat.Actions.SetUnreadConversationCount)
local IncrementUnreadConversationCount = require(Modules.LuaChat.Actions.IncrementUnreadConversationCount)
local DecrementUnreadConversationCount = require(Modules.LuaChat.Actions.DecrementUnreadConversationCount)

return function(state, action)
	state = state or 0

	if action.type == SetUnreadConversationCount.name then
		state = action.count
	elseif action.type == IncrementUnreadConversationCount.name then
		state = state + 1
	elseif action.type == DecrementUnreadConversationCount.name then
		state = state - 1
	end
	return state
end