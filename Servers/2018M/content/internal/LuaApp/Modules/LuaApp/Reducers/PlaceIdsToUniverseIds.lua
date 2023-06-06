local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Immutable = require(Modules.Common.Immutable)
local AddPlaceIdsToUniverseIds = require(Modules.LuaApp.Actions.AddPlaceIdsToUniverseIds)

return function(state, action)
	state = state or {}

	if action.type == AddPlaceIdsToUniverseIds.name then
		state = Immutable.JoinDictionaries(state, action.placeIdsToUniverseIds)
	end

	return state
end