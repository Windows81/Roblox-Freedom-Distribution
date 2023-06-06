local Modules = game:GetService("CoreGui").RobloxGui.Modules
local ApiFetchGamesInSort = require(Modules.LuaApp.Thunks.ApiFetchGamesInSort)
local Promise = require(Modules.LuaApp.Promise)
local Constants = require(Modules.LuaApp.Constants)

-- create a thunk that fetches all the information we'll need for the games page
return function(networkImpl, sortCategory, targetSort)

	-- Default fetching for Games Page data
	if not sortCategory then
		sortCategory = Constants.GameSortGroups.Games
	end

	return function(store)
		local fetchPromises = {}
		local state = store:getState()
		if not targetSort then
			for _, sortName in ipairs(state.GameSortGroups[sortCategory].sorts) do
				local sort = state.GameSorts[sortName]
				local promise = store:dispatch(ApiFetchGamesInSort(networkImpl, sort))
				table.insert(fetchPromises, promise)
			end
		else
			if state.GameSorts[targetSort] then
				local promise = store:dispatch(ApiFetchGamesInSort(networkImpl, state.GameSorts[targetSort]))
				table.insert(fetchPromises, promise)
			else
				Promise.reject()
			end
		end
		return Promise.all(fetchPromises)
	end
end