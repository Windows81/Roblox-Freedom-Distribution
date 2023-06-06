local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Immutable = require(Modules.Common.Immutable)
local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)
local SetGameSortTokenFetchingStatus = require(Modules.LuaApp.Actions.SetGameSortTokenFetchingStatus)

return function(state, action)
	state = state or {
		Games = RetrievalStatus.NotStarted,
		HomeGames = RetrievalStatus.NotStarted,

		-- Not in-use now
		GamesSeeAll = RetrievalStatus.NotStarted,
	}

	if action.type == SetGameSortTokenFetchingStatus.name then
		state = Immutable.Set(state, action.sortCategory, action.fetchStatus)
	end
	return state
end