local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local Action = require(Common.Action)

return Action(script.Name, function(id, participants, title, lastUpdated)
	return {
		conversationId = id,
		participants = participants,
		title = title,
		lastUpdated = lastUpdated,
	}
end)