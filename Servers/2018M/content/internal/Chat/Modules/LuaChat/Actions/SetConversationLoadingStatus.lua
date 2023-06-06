local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local Action = require(Common.Action)

return Action(script.Name, function(convoId, conversationLoadingState)
	return {
		conversationId = convoId,
		value = conversationLoadingState
	}
end)