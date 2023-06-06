local Modules = game:GetService("CoreGui").RobloxGui.Modules
local LuaChat = Modules.LuaChat

local SetFriendCount = require(LuaChat.Actions.SetFriendCount)

return function(state, action)
	state = state or 0

	if action.type == SetFriendCount.name then
		return action.count
	end

	return state
end