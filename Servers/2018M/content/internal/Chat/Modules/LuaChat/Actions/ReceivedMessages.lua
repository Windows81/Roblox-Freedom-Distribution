local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local Action = require(Common.Action)

return Action(script.Name, function(conversationId, messages, shouldMarkConversationUnread, messageId)
		return {
			conversationId = conversationId,
			messages = messages,
			shouldMarkConversationUnread = shouldMarkConversationUnread,
			exclusiveStartMessageId = messageId,
		}
	end
)