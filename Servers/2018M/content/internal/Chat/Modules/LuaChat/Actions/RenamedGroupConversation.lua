local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local Action = require(Common.Action)

return Action(script.Name, function(conversationId, title, isDefaultTitle, lastUpdated)
	return {
		conversationId = conversationId,
		title = title,
		isDefaultTitle = isDefaultTitle,
		lastUpdated = lastUpdated,
	}
end)