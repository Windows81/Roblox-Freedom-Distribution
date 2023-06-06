local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Immutable = require(Modules.Common.Immutable)
local AddGames = require(Modules.LuaApp.Actions.AddGames)
local SetPlayabilityStatus = require(Modules.LuaApp.Actions.SetPlayabilityStatus)

return function(state, action)
	state = state or {}

	if action.type == AddGames.name then
		-- store the data from the games
		state = Immutable.JoinDictionaries(state, action.games)
	elseif action.type == SetPlayabilityStatus.name then
		if state[action.universeId] then
			state[action.universeId] = Immutable.Set(state[action.universeId], "playabilityStatus", action.playabilityStatus)
		end
	end

	return state
end