local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Action = require(Modules.Common.Action)

--[[
	{
		searchUuid : number
		fetchStatus : SearchRetrievalStatus,
    }
]]

return Action(script.Name, function(searchUuid, status)
	return {
		searchUuid = searchUuid,
		status = status,
	}
end)