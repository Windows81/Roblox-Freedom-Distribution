local CoreGui = game:GetService("CoreGui")
local Action = require(CoreGui.RobloxGui.Modules.Common.Action)

return Action("RemoveScreen", function(item)
	return {
		item = item,
	}
end)
