local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common

local Action = require(Common.Action)

return Action(script.Name, function(conversationId, userId, isUserTyping)
	return {
		conversationId = conversationId,
		userId = userId,
		value = isUserTyping,
	}
end)