local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Constants = require(Modules.LuaApp.Constants)
local Promise = require(Modules.LuaApp.Promise)
local ApiFetchSearchInGames = require(Modules.LuaApp.Thunks.ApiFetchSearchInGames)
-- local ApiFetchSearchInGroups = require(Modules.LuaApp.Thunks.ApiFetchSearchInGroups)
-- local ApiFetchSearchInPlayers = require(Modules.LuaApp.Thunks.ApiFetchSearchInPlayers)
-- local ApiFetchSearchInCatalog = require(Modules.LuaApp.Thunks.ApiFetchSearchInCatalog)
-- local ApiFetchSearchInLibrary = require(Modules.LuaApp.Thunks.ApiFetchSearchInLibrary)

local thunkMap = {
	[Constants.SearchTypes.Games] = function(store, ...)
		return store:Dispatch(ApiFetchSearchInGames(...))
	end,
	-- [Constants.SearchTypes.Groups] = function(store, ...)
	-- 	return store:Dispatch(ApiFetchSearchInGroups(...))
	-- end,
	-- [Constants.SearchTypes.Players] = function(store, ...)
	-- 	return store:Dispatch(ApiFetchSearchInPlayers(...))
	-- end,
	-- [Constants.SearchTypes.Catalog] = function(store, ...)
	-- 	return store:Dispatch(ApiFetchSearchInCatalog(...))
	-- end,
	-- [Constants.SearchTypes.Library] = function(store, ...)
	-- 	return store:Dispatch(ApiFetchSearchInLibrary(...))
	-- end,
}

--[[
	searchArguments = {
		searchKeyword : string,
		searchUuid : number,
		searchType : Constants.SearchTypes,
		isAppend : boolean,
	}
]]

return function(networkImpl, searchArguments, optionalSettings)
	if not searchArguments.searchUuid then
		return function()
			Promise.reject("Must have a searchUuid.")
		end
	end

	if not searchArguments.searchKeyword then
		return function()
			Promise.reject("Must have a searchKeyword to search with.")
		end
	end
	-- Default search Games, will need to update when design is done
	if not searchArguments.searchType then
		searchArguments.searchType = Constants.SearchTypes.Games
	end
	return function(store)
		if thunkMap[searchArguments.searchType] then
			return thunkMap[searchArguments.searchType](store, networkImpl, searchArguments, optionalSettings)
		else
			Promise.reject("We don't support this searchType.")
		end
	end
end