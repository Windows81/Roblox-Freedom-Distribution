local Modules = game:GetService("CoreGui").RobloxGui.Modules
local ApplyNavigateToRoute = require(Modules.LuaApp.Actions.ApplyNavigateToRoute)

return function(route, navLockEndTime)
	assert(type(route) == "table", "NavigateToRoute thunk expects route to be a table")
	assert(type(navLockEndTime) == "nil" or type(navLockEndTime) == "number",
		"NavigateToRoute thunk expects navLockEndTime to be nil or a number")

	return function(store)
		local state = store:getState()

		if state.Navigation.lockTimer > tick() then
			return
		end

		store:dispatch(ApplyNavigateToRoute(route, navLockEndTime))
	end
end