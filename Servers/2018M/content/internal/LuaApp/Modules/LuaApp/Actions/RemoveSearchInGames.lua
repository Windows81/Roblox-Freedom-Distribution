local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Action = require(Modules.Common.Action)

--[[
	{
		searchUuid : number
		searchesInGames : table [] (SearchInGames model),
    }
]]

return Action(script.Name, function(searchUuid)
	return {
		searchUuid = searchUuid
	}
end)