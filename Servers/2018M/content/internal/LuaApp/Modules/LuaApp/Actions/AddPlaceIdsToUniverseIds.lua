local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Action = require(Modules.Common.Action)


--[[
	Passes a table that looks like this... { placeId = universeId, ... }
]]

return Action(script.Name, function(placeIdsToUniverseIds)
	return {
		placeIdsToUniverseIds = placeIdsToUniverseIds
	}
end)