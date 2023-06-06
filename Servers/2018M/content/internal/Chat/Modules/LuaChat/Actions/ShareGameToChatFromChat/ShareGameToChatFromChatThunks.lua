local Modules = game:GetService("CoreGui").RobloxGui.Modules
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat
local ShareGameToChatActions = LuaChat.Actions.ShareGameToChatFromChat

local AddGamesBySort = require(ShareGameToChatActions.AddGamesBySortShareGameToChatFromChat)
local AddGamesInformation =  require(ShareGameToChatActions.AddGamesInformationShareGameToChatFromChat)
local Constants = require(LuaChat.Constants)
local ClearAllGamesInSorts = require(ShareGameToChatActions.ClearAllGamesInSortsShareGameToChatFromChat)
local FailedToFetchGamesBySort = require(ShareGameToChatActions.FailedToFetchGamesBySortShareGameToChatFromChat)
local FailedToShareGameToChat = require(ShareGameToChatActions.FailedToShareGameToChatFromChat)
local FetchedGamesBySort = require(ShareGameToChatActions.FetchedGamesBySortShareGameToChatFromChat)
local FetchingGamesBySort = require(ShareGameToChatActions.FetchingGamesBySortShareGameToChatFromChat)
local PopRoute = require(LuaChat.Actions.PopRoute)
local ResetShareGame = require(ShareGameToChatActions.ResetShareGameToChatFromChat)
local ResetShareGameToChatAsync = require(ShareGameToChatActions.ResetShareGameToChatFromChatAsync)
local SharedGameToChat = require(ShareGameToChatActions.SharedGameToChatFromChat)
local SharingGameToChat = require(ShareGameToChatActions.SharingGameToChatFromChat)
local ShowToast = require(LuaChat.Actions.ShowToast)
local ToastModel = require(LuaChat.Models.ToastModel)
local SetGameThumbnails = require(LuaApp.Actions.SetGameThumbnails)
local UpdateGameSortsTokens = require(ShareGameToChatActions.UpdateGameSortsTokensShareGameToChatFromChat)
local WebApi = require(LuaChat.WebApi)

local SHARED_GAMES_SORT = "GamesAllSorts"

local ShareGameToChatFromChatThunks = {}

function ShareGameToChatFromChatThunks.FetchGames(gameSortName, fetchedThumbnailSize)
	return function(store)
		spawn(function()
			if store:getState().ChatAppReducer.ShareGameToChatAsync.fetchingGamesBySort[gameSortName] then
				return
			end

			store:dispatch(FetchingGamesBySort(gameSortName))

			if not store:getState().ChatAppReducer.SharedGameSorts[gameSortName]
				or not store:getState().ChatAppReducer.SharedGameSorts[gameSortName].tokenExpiry
					or store:getState().ChatAppReducer.SharedGameSorts[gameSortName].tokenExpiry < tick() then
				local gameSorts = WebApi.GetGamesSorts(SHARED_GAMES_SORT)
				if not gameSorts then
					store:dispatch(FailedToFetchGamesBySort(gameSortName))
					warn("Failed to get game sorts")
					return
				end

				store:dispatch(UpdateGameSortsTokens(gameSorts))
			end

			local gamesList = nil
			if store:getState().ChatAppReducer.SharedGameSorts[gameSortName] and
					store:getState().ChatAppReducer.SharedGameSorts[gameSortName].token then
				gamesList = WebApi.GetGamesInSortByToken(store:getState().ChatAppReducer.SharedGameSorts[gameSortName].token)
			end

			if gamesList then
				local placeIds = {}
				local newPlaceIds = {}
				local games = {}

				for _, game in pairs(gamesList) do
					table.insert(placeIds, game.placeId)
					if not store:getState().ChatAppReducer.SharedGamesInfo[game.placeId] then
						games[game.placeId] = game
					end

					if not store:getState().ChatAppReducer.SharedGamesInfo[game.placeId] or
							not store:getState().ChatAppReducer.SharedGamesInfo[game.placeId].url then
						table.insert(newPlaceIds, game.placeId)
					end
				end

				if #newPlaceIds > 0 then
					local _, placesInfo = WebApi.GetMultiplePlaceInfos(newPlaceIds)
					local imageTokens = {}
					for _, placeInfo in pairs(placesInfo) do
						games[placeInfo.placeId].url = placeInfo.url
						games[placeInfo.placeId].isPlayable = placeInfo.isPlayable
						table.insert(imageTokens, placeInfo.imageToken)
					end

					store:dispatch(AddGamesInformation(games))

					local thumbnails = WebApi.GetPlacesThumbnails(imageTokens, fetchedThumbnailSize, fetchedThumbnailSize)
					store:dispatch(SetGameThumbnails(thumbnails))
				end

				store:dispatch(FetchedGamesBySort(gameSortName))
				store:dispatch(AddGamesBySort(gameSortName, placeIds))
			else
				store:dispatch(AddGamesBySort(gameSortName, nil))
				store:dispatch(FailedToFetchGamesBySort(gameSortName))
				warn("No " .. gameSortName .. " games found")
			end
		end)
	end
end

function ShareGameToChatFromChatThunks.HasGameFetchRequestCompleted(sortName, shareGameToChatAsync)
	return shareGameToChatAsync.fetchedGamesBySort[sortName] or
			shareGameToChatAsync.failedToFetchGamesBySort[sortName]
end

function ShareGameToChatFromChatThunks.Sharing(store)
	store:dispatch(SharingGameToChat())
end

function ShareGameToChatFromChatThunks.Shared(store)
	store:dispatch(PopRoute())
	store:dispatch(SharedGameToChat())

	store:dispatch(ResetShareGame())
	store:dispatch(ClearAllGamesInSorts())
	store:dispatch(ResetShareGameToChatAsync())
end

function ShareGameToChatFromChatThunks.FailedToShare(store)
	local messageKey = "Feature.Chat.ShareGameToChat.FailedToShareTheGame"
	local toastModel = ToastModel.new(Constants.ToastIDs.GAME_NOT_SHAREABLE, messageKey)

	store:dispatch(ShowToast(toastModel))
	store:dispatch(FailedToShareGameToChat())
end

return ShareGameToChatFromChatThunks