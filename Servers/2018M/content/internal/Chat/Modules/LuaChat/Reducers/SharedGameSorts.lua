local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local Immutable = require(Common.Immutable)
local LuaChat = Modules.LuaChat
local ShareGameToChatActions = LuaChat.Actions.ShareGameToChatFromChat

local AddGamesBySort = require(ShareGameToChatActions.AddGamesBySortShareGameToChatFromChat)
local UpdateGameSortsTokens = require(ShareGameToChatActions.UpdateGameSortsTokensShareGameToChatFromChat)
local ClearAllGamesInSorts = require(ShareGameToChatActions.ClearAllGamesInSortsShareGameToChatFromChat)

return function(state, action)
	state = state or {}

	if action.type == AddGamesBySort.name then
		local sort = state[action.name] or {}
		local newSort = Immutable.JoinDictionaries(sort, {
			token = sort.token,
			tokenExpiry = sort.tokenExpiry,
			placeIds = action.placeIds
		})
		state = Immutable.Set(state, action.name, newSort)
	elseif action.type == UpdateGameSortsTokens.name then
		for _, gameSort in pairs(action.gameSorts) do
			local sort = state[gameSort.name] or {}
			local placeIds = state[gameSort.name] ~= nil and state[gameSort.name].placeIds or nil
			local newSort = Immutable.JoinDictionaries(sort, {
				token = gameSort.token,
				tokenExpiry = gameSort.tokenExpiryInSeconds + tick(),
				placeIds = placeIds
			})
			state = Immutable.Set(state, gameSort.name, newSort)
		end
	elseif action.type == ClearAllGamesInSorts.name then
		state = {}
	end

	return state
end