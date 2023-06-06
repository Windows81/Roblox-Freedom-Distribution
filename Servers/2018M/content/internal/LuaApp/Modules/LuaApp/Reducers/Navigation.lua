local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Rodux = require(Modules.Common.Rodux)
local Immutable = require(Modules.Common.Immutable)
local AppPage = require(Modules.LuaApp.AppPage)
local ApplyNavigateToRoute = require(Modules.LuaApp.Actions.ApplyNavigateToRoute)
local ApplyNavigateBack = require(Modules.LuaApp.Actions.ApplyNavigateBack)

local DEFAULT_PAGE = { name = AppPage.Home }
local DEFAULT_ROUTE = { DEFAULT_PAGE }

local function newNavState(state, history, timeout)
	return {
		history = history,
		lockTimer = math.max(state.lockTimer, timeout or 0),
	}
end

return Rodux.createReducer({
	history = { DEFAULT_ROUTE },
	lockTimer = 0,
}, {
	[ApplyNavigateToRoute.name] = function(state, action)
		if #action.route == 1 then
			-- If we're navigating to a root page, clear the history.
			return newNavState(state, { action.route }, action.timeout)
		else
			return newNavState(state, Immutable.Append(state.history, action.route), action.timeout)
		end
	end,
	[ApplyNavigateBack.name] = function(state, action)
		if #state.history > 1 then
			return newNavState(state, Immutable.RemoveFromList(state.history, #state.history), action.timeout)
		else
			return state
		end
	end,
})