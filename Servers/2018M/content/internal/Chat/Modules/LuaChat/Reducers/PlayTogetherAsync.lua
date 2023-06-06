local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaChat = Modules.LuaChat
local Actions = LuaChat.Actions

local FailedToFetchMostRecentlyPlayedGames = require(Actions.FailedToFetchMostRecentlyPlayedGames)
local FetchedMostRecentlyPlayedGames = require(Actions.FetchedMostRecentlyPlayedGames)
local FetchingMostRecentlyPlayedGames = require(Actions.FetchingMostRecentlyPlayedGames)
local GameFailedToPin = require(Actions.GameFailedToPin)
local GameFailedToUnpin = require(Actions.GameFailedToUnpin)
local PinnedGame = require(Actions.PinnedGame)
local PinningGame = require(Actions.PinningGame)
local UnpinnedGame = require(Actions.UnpinnedGame)
local UnpinningGame = require(Actions.UnpinningGame)

local Immutable = require(Common.Immutable)

return function(state, action)
    state = state or {
        pinningGames = {},
        unPinningGames = {},
    }
    -- play together async
    if action.type == PinningGame.name then
        local newPinningGames = Immutable.Set(state.pinningGames, action.conversationId, true)
        return Immutable.JoinDictionaries(state, {
            pinningGames = newPinningGames;
        })
    elseif action.type == PinnedGame.name then
        local newPinningGames = Immutable.Set(state.pinningGames, action.conversationId, false)
        return Immutable.JoinDictionaries(state, {
            pinningGames = newPinningGames;
        })
    elseif action.type == GameFailedToPin.name then
        local newPinningGames = Immutable.Set(state.pinningGames, action.conversationId, false)
        return Immutable.JoinDictionaries(state, {
            pinningGames = newPinningGames;
        })
    elseif action.type == UnpinningGame.name then
        local newUnpinningGames = Immutable.Set(state.unPinningGames, action.conversationId, true)
        return Immutable.JoinDictionaries(state, {
            unPinningGames = newUnpinningGames;
        })
    elseif action.type == UnpinnedGame.name then
        local newUnpinningGames = Immutable.Set(state.unPinningGames, action.conversationId, false)
        return Immutable.JoinDictionaries(state, {
            unPinningGames = newUnpinningGames;
        })
    elseif action.type == GameFailedToUnpin.name then
        local newUnpinningGames = Immutable.Set(state.unPinningGames, action.conversationId, false)
        return Immutable.JoinDictionaries(state, {
            unPinningGames = newUnpinningGames;
        })
    elseif action.type == FetchingMostRecentlyPlayedGames.name then
        return Immutable.JoinDictionaries(state, {
            fetchingMostRecentlyPlayedGames = true,
            fetchedMostRecentlyPlayedGames = false
        })
    elseif action.type == FetchedMostRecentlyPlayedGames.name then
        return Immutable.JoinDictionaries(state, {
            fetchingMostRecentlyPlayedGames = false,
            fetchedMostRecentlyPlayedGames = true,
        })
    elseif action.type == FailedToFetchMostRecentlyPlayedGames.name then
        return Immutable.JoinDictionaries(state, {
            fetchingMostRecentlyPlayedGames = false,
            fetchedMostRecentlyPlayedGames = false
        })
    end

    return state
end