local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Immutable = require(Modules.Common.Immutable)
local NavigateToRoute = require(Modules.LuaApp.Thunks.NavigateToRoute)

return function(page, navLockEndTime)
	assert(type(page) == "table", "NavigateDown thunk expects page to be a table")
	assert(type(navLockEndTime) == "nil" or type(navLockEndTime) == "number",
		"NavigateDown thunk expects navLockEndTime to be nil or a number")

	return function(store)
		local state = store:getState()

		local currentRoute = state.Navigation.history[#state.Navigation.history]
		local newRoute = Immutable.Append(currentRoute, page)
		store:dispatch(NavigateToRoute(newRoute, navLockEndTime))
	end
end