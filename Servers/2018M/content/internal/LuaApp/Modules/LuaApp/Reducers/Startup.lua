local Modules = game:GetService("CoreGui").RobloxGui.Modules

local GamesPageDataStatus = require(Modules.LuaApp.Reducers.GamesPageDataStatus)
local HomePageDataStatus = require(Modules.LuaApp.Reducers.HomePageDataStatus)
local SetPreloading = require(Modules.LuaApp.Actions.SetPreloading)

return function(state, action)
	state = state or {}
	local Preloading = state.Preloading == nil and true or state.Preloading

	if action.type == SetPreloading.name then
		Preloading = action.isPreloading
	end

	return {
		GamesPageDataStatus = GamesPageDataStatus(state.GamesPageDataStatus, action),
		HomePageDataStatus = HomePageDataStatus(state.HomePageDataStatus, action),
		Preloading = Preloading,
	}
end