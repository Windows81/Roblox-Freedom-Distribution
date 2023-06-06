local CoreGui = game:GetService("CoreGui")
local Action = require(CoreGui.RobloxGui.Modules.Common.Action)

return Action("AddError", function(error, timestamp)
	error = error or {}
	return {
		error = {
			Title = error.Title,
			Msg = error.Msg,
			Code = error.Code,
			timestamp = timestamp
		}
	}
end)