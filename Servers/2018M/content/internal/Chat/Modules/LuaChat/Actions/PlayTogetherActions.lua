local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local LuaChat = Modules.LuaChat
local Actions = LuaChat.Actions

local Constants = require(LuaChat.Constants)
local PlaceInfoModel = require(LuaChat.Models.PlaceInfoModel)
local ToastModel = require(LuaChat.Models.ToastModel)
local WebApi = require(LuaChat.WebApi)

local FailedToFetchedMostRecentlyPlayedGames = require(Actions.FailedToFetchMostRecentlyPlayedGames)
local FailedToFetchMultiplePlaceInfos = require(Actions.FailedToFetchMultiplePlaceInfos)
local FetchedMostRecentlyPlayedGames = require(Actions.FetchedMostRecentlyPlayedGames)
local FetchingMostRecentlyPlayedGames = require(Actions.FetchingMostRecentlyPlayedGames)
local GameFailedToPin = require(Actions.GameFailedToPin)
local GameFailedToUnpin = require(Actions.GameFailedToUnpin)
local PinnedGame = require(Actions.PinnedGame)
local PinningGame = require(Actions.PinningGame)
local ReceivedMultiplePlaceInfos = require(Actions.ReceivedMultiplePlaceInfos)
local RequestMultiplePlaceInfos = require(Actions.RequestMultiplePlaceInfos)
local SetMostRecentlyPlayedGamesForUser = require(Actions.SetMostRecentlyPlayedGamesForUser)
local SetMostRecentlyPlayedPlayableGameForUser = require(Actions.SetMostRecentlyPlayedPlayableGameForUser)
local SetPinnedGameForConversation = require(Actions.SetPinnedGameForConversation)
local ShowToast = require(Actions.ShowToast)
local UnpinnedGame = require(Actions.UnpinnedGame)
local UnpinningGame = require(Actions.UnpinningGame)

local PlayTogetherActions = {}

local HOME_GAMES_SORTS = "HomeSorts"
local MOST_RECENTLY_PLAYED_GAMES = "MyRecent"

function PlayTogetherActions.PinGame(conversationId, universeId)
    return function(store)
        if universeId == store:getState().ChatAppReducer.Conversations[conversationId].pinnedGame.universeId then
            local messageKey = "Feature.Chat.Message.AlreadyPinnedGame"
            local toastModel = ToastModel.new(Constants.ToastIDs.PIN_PINNED_GAME, messageKey)
            store:Dispatch(ShowToast(toastModel))
            return
        end

        if store:getState().ChatAppReducer.PlayTogetherAsync.pinningGames[conversationId] then
            return
        end

        store:Dispatch(PinningGame(conversationId))

        spawn(function()
            local status, _ = WebApi.PinGame(conversationId, universeId)
            if status == WebApi.Status.OK then
                store:Dispatch(PinnedGame(conversationId))
            else
                store:Dispatch(GameFailedToPin(conversationId))

                local messageKey = "Feature.Chat.Message.PinFailed"
                local toastModel = ToastModel.new(Constants.ToastIDs.PIN_GAME_FAILED, messageKey)
                store:Dispatch(ShowToast(toastModel))

                warn("Game could not be pinned.")
            end
        end)
    end
end

function PlayTogetherActions.UnpinGame(conversationId)
    return function(store)
        if store:getState().ChatAppReducer.PlayTogetherAsync.unPinningGames[conversationId] then
            return
        end

        store:Dispatch(UnpinningGame(conversationId))

        spawn(function()
            local status, _ = WebApi.UnpinGame(conversationId)
            if status == WebApi.Status.OK then
                store:Dispatch(UnpinnedGame(conversationId))
            else
                store:Dispatch(GameFailedToUnpin(conversationId))

                local messageKey = "Feature.Chat.Message.UnpinFailed"
                local toastModel = ToastModel.new(Constants.ToastIDs.UNPIN_GAME_FAILED, messageKey)
                store:Dispatch(ShowToast(toastModel))

                warn("Game could not be unpinned.")
            end
        end)
    end
end

function PlayTogetherActions.SetPinnedGameForConversation(universeId, rootPlaceId, conversationId)
    return function(store)
        spawn(function()
            store:Dispatch(SetPinnedGameForConversation(
                universeId,
                rootPlaceId,
                conversationId
            ))
        end)
    end
end

function PlayTogetherActions.GetMostRecentlyPlayedGames()
    return function(store)
        spawn(function()
            if store:getState().ChatAppReducer.PlayTogetherAsync.fetchingMostRecentlyPlayedGames then
                return
            end

            store:Dispatch(FetchingMostRecentlyPlayedGames())

            local gameSorts = WebApi.GetGamesSorts(HOME_GAMES_SORTS)
            if not gameSorts then
                warn("Failed to get game sorts")
                store:Dispatch(FailedToFetchedMostRecentlyPlayedGames())
                return
            end

            for _, sort in pairs(gameSorts) do
                if sort.name == MOST_RECENTLY_PLAYED_GAMES then
                    local games = WebApi.GetMostRecentlyPlayedGames(sort.token)
                    if games then
                        store:Dispatch(FetchedMostRecentlyPlayedGames())
                        store:Dispatch(SetMostRecentlyPlayedGamesForUser(games))
                    else
                        warn("No most recently played games found")
                        store:Dispatch(FailedToFetchedMostRecentlyPlayedGames())
                    end

                    return
                end
            end

            warn("No most recently played game sort")
            store:Dispatch(FailedToFetchedMostRecentlyPlayedGames())
        end)
    end
end

function PlayTogetherActions.GetMostRecentlyPlayedPlayableGame()
    return function(store)
        local mostRecentlyPlayedGames = store:getState().ChatAppReducer.MostRecentlyPlayedGames.games
        if not mostRecentlyPlayedGames or #mostRecentlyPlayedGames == 0 then
            return
        end

        spawn(function()
            local mostRecentlyPlayedPlayableGamePlaceId = nil
            for _, game in pairs(mostRecentlyPlayedGames) do
                local placeId = tostring(game.placeId)
                local placeInfo = store:getState().ChatAppReducer.PlaceInfos[placeId]

                if (placeInfo == nil) and (not store:getState().ChatAppReducer.PlaceInfosAsync[placeId]) then
                    local placeIds = { placeId }
                    store:Dispatch(RequestMultiplePlaceInfos(placeIds))

                    local status, result = WebApi.GetMultiplePlaceInfos(placeIds)

                    if status ~= WebApi.Status.OK then
                        warn("WebApi failure in GetMostRecentlyPlayedPlayableGame")
                        store:Dispatch(FailedToFetchMultiplePlaceInfos(placeIds))
                    else
                        local placeInfos = {}
                        for _, placeInfoData in pairs(result) do
                            table.insert(placeInfos, PlaceInfoModel.fromWeb(placeInfoData))
                        end
                        store:Dispatch(ReceivedMultiplePlaceInfos(placeInfos))
                    end
                    break
                end

                if placeInfo and placeInfo.isPlayable then
                    mostRecentlyPlayedPlayableGamePlaceId = placeId
                    break
                end
            end

            if mostRecentlyPlayedPlayableGamePlaceId then
                store:Dispatch(SetMostRecentlyPlayedPlayableGameForUser(mostRecentlyPlayedPlayableGamePlaceId))
            end
        end)
    end
end

return PlayTogetherActions