local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Action = require(Modules.Common.Action)

--[[
	{
		sortName : string
		fetchStatus : RetrievalStatus,
    }
]]

return Action(script.Name, function(sortName, status)
	return {
		sortName = sortName,
		status = status,
	}
end)