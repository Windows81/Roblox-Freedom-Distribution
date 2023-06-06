local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Immutable = require(Modules.Common.Immutable)

local SetSearchInGamesStatus = require(Modules.LuaApp.Actions.SetSearchInGamesStatus)

return function(state, action)
	state = state or {}

	if action.type == SetSearchInGamesStatus.name then
		state = Immutable.Set(state, action.searchUuid, action.status)
	end

	return state
end