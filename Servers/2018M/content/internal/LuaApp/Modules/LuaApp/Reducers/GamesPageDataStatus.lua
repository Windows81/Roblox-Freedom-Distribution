local Modules = game:GetService("CoreGui").RobloxGui.Modules
local SetGamesPageDataStatus = require(Modules.LuaApp.Actions.SetGamesPageDataStatus)
local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)

return function(state, action)
	state = state or RetrievalStatus.NotStarted

	if action.type == SetGamesPageDataStatus.name then
		state = action.status
	end

	return state
end