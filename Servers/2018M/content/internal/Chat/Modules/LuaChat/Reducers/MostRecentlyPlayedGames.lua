local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaChat = Modules.LuaChat
local Actions = LuaChat.Actions

local SetMostRecentlyPlayedGamesForUser = require(Actions.SetMostRecentlyPlayedGamesForUser)
local SetMostRecentlyPlayedPlayableGameForUser = require(Actions.SetMostRecentlyPlayedPlayableGameForUser)

local Immutable = require(Common.Immutable)

return function(state, action)
    state = state or {}

    if action.type == SetMostRecentlyPlayedGamesForUser.name then
        return Immutable.JoinDictionaries(state, {
            games = action.games
        })
    elseif action.type == SetMostRecentlyPlayedPlayableGameForUser.name then
        return Immutable.JoinDictionaries(state, {
            playableGamePlaceId = action.placeId,
            setPlayableGame = true
        })
    end

    return state
end