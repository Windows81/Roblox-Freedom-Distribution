local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Immutable = require(Modules.Common.Immutable)
local NavigateToRoute = require(Modules.LuaApp.Thunks.NavigateToRoute)

return function(page, navLockEndTime)
	assert(type(page) == "table", "NavigateSideways thunk expects page to be a table")
	assert(type(navLockEndTime) == "nil" or type(navLockEndTime) == "number",
		"NavigateSideways thunk expects navLockEndTime to be nil or a number")

	return function(store)
		local state = store:getState()

		local oldRoute = state.Navigation.history[#state.Navigation.history]
		local truncatedRoute = Immutable.RemoveFromList(oldRoute, #oldRoute)
		local newRoute = Immutable.Append(truncatedRoute, page)
		store:dispatch(NavigateToRoute(newRoute, navLockEndTime))
	end
end