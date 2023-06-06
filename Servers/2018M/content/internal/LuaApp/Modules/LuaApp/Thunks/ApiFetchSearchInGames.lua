local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Actions = Modules.LuaApp.Actions
local Requests = Modules.LuaApp.Http.Requests
local AddGames = require(Actions.AddGames)
local SetSearchInGames = require(Actions.SetSearchInGames)
local AppendSearchInGames = require(Actions.AppendSearchInGames)
local SetSearchInGamesStatus = require(Actions.SetSearchInGamesStatus)
local AddPlaceIdsToUniverseIds = require(Actions.AddPlaceIdsToUniverseIds)
local GamesGetList = require(Requests.GamesGetList)
local Immutable = require(Modules.Common.Immutable)
local SearchRetrievalStatus = require(Modules.LuaApp.Enum.SearchRetrievalStatus)
local ApiFetchGameThumbnails = require(Modules.LuaApp.Thunks.ApiFetchGameThumbnails)
local Game = require(Modules.LuaApp.Models.Game)
local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
local SearchInGames = require(Modules.LuaApp.Models.SearchInGames)
local Constants = require(Modules.LuaApp.Constants)
local Promise = require(Modules.LuaApp.Promise)
local TableUtilities = require(Modules.LuaApp.TableUtilities)

return function(networkImpl, searchArguments, optionalSettings)
	return function(store)
		local searchKeyword = searchArguments.searchKeyword
		local searchUuid = searchArguments.searchUuid

		if not searchUuid then
			return Promise.reject("Must have a searchUuid.")
		end

		if not searchKeyword then
			return Promise.reject("Must have a searchKeyword to search with.")
		end

		local searchesInGamesStatus = store:getState().RequestsStatus.SearchesInGamesStatus
		local searchStatus = searchesInGamesStatus[searchUuid]

		if searchStatus == SearchRetrievalStatus.Fetching then
			return Promise.resolve("Search with Uuid "..searchUuid.." has been debounced")
		end

		local argTableSearch = Immutable.JoinDictionaries({ keyword = searchKeyword }, optionalSettings or {})

		-- Some default values
		argTableSearch.startRows = argTableSearch.startRows or 0
		argTableSearch.maxRows = argTableSearch.maxRows or Constants.DEFAULT_GAME_FETCH_COUNT
		argTableSearch.isKeywordSuggestionEnabled = argTableSearch.isKeywordSuggestionEnabled or false

		store:dispatch(SetSearchInGamesStatus(searchUuid, SearchRetrievalStatus.Fetching))

		return GamesGetList(networkImpl, argTableSearch):andThen(
			function(result)
				local entries = {}
				local decodedGamesData = {}
				local placeIdsToUniverseIds = {}
				local thumbnailTokens = {}
				local storedGames = store:getState().Games
				local data = result.responseBody

				searchesInGamesStatus = store:getState().RequestsStatus.SearchesInGamesStatus
				searchStatus = searchesInGamesStatus[searchUuid]

				if searchStatus == SearchRetrievalStatus.Removed then
					return Promise.resolve("Search with Uuid "..searchUuid.." has been terminated")
				end

				for index, game in pairs(data.games) do
					local placeId = game.placeId
					local universeId = game.universeId
					local decodedGameData = Game.fromJsonData(game)

					if not TableUtilities.ShallowEqual(decodedGameData, storedGames[universeId]) then
						decodedGamesData[universeId] = decodedGameData

						if storedGames[universeId] == nil or decodedGameData.imageToken ~= storedGames[universeId].imageToken then
							table.insert(thumbnailTokens, decodedGameData.imageToken)
						end
					end

					-- convert universeId into entry so we keep some sponsor info
					local entry = GameSortEntry.fromJsonData(game)
					entries[index] = entry


					if placeId and universeId and store:getState().PlaceIdsToUniverseIds[placeId] ~= universeId then
						placeIdsToUniverseIds[placeId] = universeId
					end
				end

				if next(decodedGamesData) then
					store:dispatch(AddGames(decodedGamesData))
				end

				if next(placeIdsToUniverseIds) then
					store:dispatch(AddPlaceIdsToUniverseIds(placeIdsToUniverseIds))
				end

				local rowsRequested = argTableSearch.startRows + argTableSearch.maxRows
				local searchInGamesData = SearchInGames.fromJsonData(result.responseBody, searchKeyword, entries, rowsRequested,
					argTableSearch.isKeywordSuggestionEnabled)

				if searchArguments.isAppend then
					store:dispatch(AppendSearchInGames(searchUuid, searchInGamesData))
				else
					store:dispatch(SetSearchInGames(searchUuid, searchInGamesData))
				end

				store:dispatch(SetSearchInGamesStatus(searchUuid, SearchRetrievalStatus.Done))

				if #thumbnailTokens > 0 then
					return store:dispatch(ApiFetchGameThumbnails(networkImpl, thumbnailTokens))
				else
					return Promise.resolve()
				end
			end,

			function(err)
				store:dispatch(SetSearchInGamesStatus(searchUuid, SearchRetrievalStatus.Failed))
				return Promise.reject(err)
			end
		)
	end
end