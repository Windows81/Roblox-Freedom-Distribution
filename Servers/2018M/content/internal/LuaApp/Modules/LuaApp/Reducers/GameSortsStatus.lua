local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Immutable = require(Modules.Common.Immutable)

local SetGameSortStatus = require(Modules.LuaApp.Actions.SetGameSortStatus)

return function(state, action)
	state = state or {}

	if action.type == SetGameSortStatus.name then
		state = Immutable.Set(state, action.sortName, action.status)
	end

	return state
end