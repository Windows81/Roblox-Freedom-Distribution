local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local Action = require(Common.Action)

return Action(script.Name, function(conversationId, isFetchingOlderMessages)
	return {
		conversationId = conversationId,
		fetchingOlderMessages = isFetchingOlderMessages,
	}
end)