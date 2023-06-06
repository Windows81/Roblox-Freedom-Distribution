local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Immutable = require(Modules.Common.Immutable)
local SetNextTokenRefreshTime = require(Modules.LuaApp.Actions.SetNextTokenRefreshTime)

return function(state, action)
	state = state or {
		Games = -1,
		HomeGames = -1,
		GamesSeeAll = -1,
	}

	if action.type == SetNextTokenRefreshTime.name then
		state = Immutable.Set(state, action.sortCategory, action.nextRefreshTime)
	end
	return state
end