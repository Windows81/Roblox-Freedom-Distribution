local CoreGui = game:GetService("CoreGui")
local Action = require(CoreGui.RobloxGui.Modules.Common.Action)

return Action("SetCrossPlayEnabled", function(enabled, timestamp)
	return {
		enabled = enabled,
		timestamp = timestamp
	}
end)