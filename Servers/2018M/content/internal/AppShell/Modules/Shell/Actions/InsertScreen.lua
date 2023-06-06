local CoreGui = game:GetService("CoreGui")
local Action = require(CoreGui.RobloxGui.Modules.Common.Action)

return Action("InsertScreen", function(item)
	return {
		item = item,
	}
end)
