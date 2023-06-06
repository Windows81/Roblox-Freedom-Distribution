local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local Immutable = require(Common.Immutable)
local LuaChat = Modules.LuaChat
local ShareGameToChatActions = LuaChat.Actions.ShareGameToChatFromChat

local FailedToFetchGamesBySort = require(ShareGameToChatActions.FailedToFetchGamesBySortShareGameToChatFromChat)
local FailedToShareGameToChat = require(ShareGameToChatActions.FailedToShareGameToChatFromChat)
local FetchedGamesBySort = require(ShareGameToChatActions.FetchedGamesBySortShareGameToChatFromChat)
local FetchingGamesBySort = require(ShareGameToChatActions.FetchingGamesBySortShareGameToChatFromChat)
local ResetShareGameToChatAsync = require(ShareGameToChatActions.ResetShareGameToChatFromChatAsync)
local ResetShareGame = require(ShareGameToChatActions.ResetShareGameToChatFromChat)
local SharedGameToChat = require(ShareGameToChatActions.SharedGameToChatFromChat)
local SharingGameToChat = require(ShareGameToChatActions.SharingGameToChatFromChat)

return function(state, action)
	state = state or {
		fetchingGamesBySort = {},
		fetchedGamesBySort = {},
		failedToFetchGamesBySort = {},
	}

	if action.type == FetchingGamesBySort.name then
		local newFetchingGamesBySort = Immutable.Set(state.fetchingGamesBySort, action.gameSortName, true)
		local newFetchedGamesBySort = Immutable.Set(state.fetchedGamesBySort, action.gameSortName, false)
		local newFailedToFetchGamesBySort = Immutable.Set(state.failedToFetchGamesBySort, action.gameSortName, false)

		return Immutable.JoinDictionaries(state, {
			fetchingGamesBySort = newFetchingGamesBySort;
			fetchedGamesBySort = newFetchedGamesBySort;
			failedToFetchGamesBySort = newFailedToFetchGamesBySort;
		})
	elseif action.type == FetchedGamesBySort.name then
		local newFetchingGamesBySort = Immutable.Set(state.fetchingGamesBySort, action.gameSortName, false)
		local newFetchedGamesBySort = Immutable.Set(state.fetchedGamesBySort, action.gameSortName, true)
		local newFailedToFetchGamesBySort = Immutable.Set(state.failedToFetchGamesBySort, action.gameSortName, false)

		return Immutable.JoinDictionaries(state, {
			fetchingGamesBySort = newFetchingGamesBySort;
			fetchedGamesBySort = newFetchedGamesBySort;
			failedToFetchGamesBySort = newFailedToFetchGamesBySort;
		})
	elseif action.type == FailedToFetchGamesBySort.name then
		local newFetchingGamesBySort = Immutable.Set(state.fetchingGamesBySort, action.gameSortName, false)
		local newFetchedGamesBySort = Immutable.Set(state.fetchedGamesBySort, action.gameSortName, false)
		local newFailedToFetchGamesBySort = Immutable.Set(state.failedToFetchGamesBySort, action.gameSortName, true)

		return Immutable.JoinDictionaries(state, {
			fetchingGamesBySort = newFetchingGamesBySort;
			fetchedGamesBySort = newFetchedGamesBySort;
			failedToFetchGamesBySort = newFailedToFetchGamesBySort;
		})
	elseif action.type == ResetShareGameToChatAsync.name then
		return {
			fetchingGamesBySort = {},
			fetchedGamesBySort = {},
			failedToFetchGamesBySort = {},
		}
	elseif action.type == SharingGameToChat.name then
		return Immutable.JoinDictionaries(state, {
			sharingGame = true,
			sharedGame = false,
		})
	elseif action.type == SharedGameToChat.name then
		return Immutable.JoinDictionaries(state, {
			sharingGame = false,
			sharedGame = true,
		})
	elseif action.type == FailedToShareGameToChat.name then
		return Immutable.JoinDictionaries(state, {
			sharedGame = false,
			sharingGame = false,
		})
	elseif action.type == ResetShareGame.name then
		return Immutable.JoinDictionaries(state, {
			sharedGame = false,
			sharingGame = false,
		})
	end

	return state
end