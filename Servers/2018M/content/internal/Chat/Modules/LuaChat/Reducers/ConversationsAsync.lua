local Modules = game:GetService("CoreGui").RobloxGui.Modules

local LuaChat = Modules.LuaChat

local ReceivedLatestMessages = require(LuaChat.Actions.ReceivedLatestMessages)
local ReceivedOldestConversation = require(LuaChat.Actions.ReceivedOldestConversation)
local ReceivedPageConversations = require(LuaChat.Actions.ReceivedPageConversations)
local RequestLatestMessages = require(LuaChat.Actions.RequestLatestMessages)
local RequestPageConversations = require(LuaChat.Actions.RequestPageConversations)

local Immutable = require(Modules.Common.Immutable)

return function(state, action)
	state = state or {}

	if action.type == RequestPageConversations.name then
		return Immutable.JoinDictionaries(state, {
			pageConversationsIsFetching = true,
		})
	elseif action.type == ReceivedPageConversations.name then
		return Immutable.JoinDictionaries(state, {
			pageConversationsIsFetching = false,
		})
	elseif action.type == RequestLatestMessages.name then
		return Immutable.JoinDictionaries(state, {
			latestMessagesIsFetching = true,
		})
	elseif action.type == ReceivedLatestMessages.name then
		return Immutable.JoinDictionaries(state, {
			latestMessagesIsFetching = false,
		})
	elseif action.type == ReceivedOldestConversation.name then
		return Immutable.JoinDictionaries(state, {
			oldestConversationIsFetched = true,
		})
	end

	return state
end