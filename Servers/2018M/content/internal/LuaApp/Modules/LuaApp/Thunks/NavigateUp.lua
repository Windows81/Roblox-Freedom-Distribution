local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Immutable = require(Modules.Common.Immutable)
local AppPage = require(Modules.LuaApp.AppPage)
local NavigateToRoute = require(Modules.LuaApp.Thunks.NavigateToRoute)

return function(navLockEndTime)
	assert(type(navLockEndTime) == "nil" or type(navLockEndTime) == "number",
		"NavigateUp thunk expects navLockEndTime to be nil or a number")

	return function(store)
		local state = store:getState()

		local currentRoute = state.Navigation.history[#state.Navigation.history]
		if #currentRoute == 1 then
			store:dispatch(NavigateToRoute({ AppPage.Home }, navLockEndTime))
		else
			local newRoute = Immutable.RemoveFromList(currentRoute, #currentRoute)
			store:dispatch(NavigateToRoute(newRoute, navLockEndTime))
		end
	end
end