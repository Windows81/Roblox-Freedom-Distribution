local Players = game:GetService("Players")
local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local Functional = require(Common.Functional)
local WebApi = require(LuaChat.WebApi)
local DateTime = require(LuaChat.DateTime)
local MockId = require(LuaApp.MockId)
local Constants = require(LuaChat.Constants)
local Alert = require(LuaChat.Models.Alert)
local ToastModel = require(LuaChat.Models.ToastModel)
local ConversationModel = require(LuaChat.Models.Conversation)
local UserModel = require(LuaApp.Models.User)
local getConversationDisplayTitle = require(LuaChat.Utils.getConversationDisplayTitle)
local reportToDiagByCountryCode = require(LuaChat.Utils.reportToDiagByCountryCode)
local truncateAssetLink = require(LuaChat.Utils.truncateAssetLink)

local AddUser = require(LuaApp.Actions.AddUser)
local ChangedParticipants = require(LuaChat.Actions.ChangedParticipants)
local DecrementUnreadConversationCount = require(LuaChat.Actions.DecrementUnreadConversationCount)
local FetchingOlderMessages = require(LuaChat.Actions.FetchingOlderMessages)
local FetchedOldestMessage = require(LuaChat.Actions.FetchedOldestMessage)
local GetFriendCount = require(LuaChat.Actions.GetFriendCount)
local RequestAllFriends = require(LuaChat.Actions.RequestAllFriends)
local ReceivedAllFriends = require(LuaChat.Actions.ReceivedAllFriends)
local IncrementUnreadConversationCount = require(LuaChat.Actions.IncrementUnreadConversationCount)
local MessageFailedToSend = require(LuaChat.Actions.MessageFailedToSend)
local MessageModerated = require(LuaChat.Actions.MessageModerated)
local ReadConversation = require(LuaChat.Actions.ReadConversation)
local ReceivedConversation = require(LuaChat.Actions.ReceivedConversation)
local ReceivedOldestConversation = require(LuaChat.Actions.ReceivedOldestConversation)
local RequestPageConversations = require(LuaChat.Actions.RequestPageConversations)
local ReceivedPageConversations = require(LuaChat.Actions.ReceivedPageConversations)
local ReceivedMessages = require(LuaChat.Actions.ReceivedMessages)
local RequestLatestMessages = require(LuaChat.Actions.RequestLatestMessages)
local ReceivedLatestMessages = require(LuaChat.Actions.ReceivedLatestMessages)
local RequestUserPresence = require(LuaChat.Actions.RequestUserPresence)
local ReceivedUserPresence = require(LuaChat.Actions.ReceivedUserPresence)
local RemovedConversation = require(LuaChat.Actions.RemovedConversation)
local RenamedGroupConversation = require(LuaChat.Actions.RenamedGroupConversation)
local SendingMessage = require(LuaChat.Actions.SendingMessage)
local SentMessage = require(LuaChat.Actions.SentMessage)
local SetConversationLoadingStatus = require(LuaChat.Actions.SetConversationLoadingStatus)
local SetUnreadConversationCount = require(LuaChat.Actions.SetUnreadConversationCount)
local SetUserIsFriend = require(LuaApp.Actions.SetUserIsFriend)
local ShowAlert = require(LuaChat.Actions.ShowAlert)
local ShowToast = require(LuaChat.Actions.ShowToast)
local SetUserLeavingConversation = require(LuaChat.Actions.SetUserLeavingConversation)
local ShareGameToChatThunks = require(LuaChat.Actions.ShareGameToChatFromChat.ShareGameToChatFromChatThunks)

local LuaChatUseNewFriendsAndPresenceEndpoint = settings():GetFFlag("LuaChatUseNewFriendsAndPresenceEndpoint")
local LuaChatPerformanceTracking = settings():GetFFlag("LuaChatPerformanceTracking")

local LuaChatCreateChatEnabled = settings():GetFFlag("LuaChatCreateChatEnabled")
local FFlagShareGameToChatStatusAnalytics = settings():GetFFlag("ShareGameToChatStatusAnalytics")

local Promise = require(LuaApp.Promise)

local GET_MESSAGES_PAGE_SIZE = Constants.PageSize.GET_MESSAGES

local lastAscendingNumber = 0

local function getAscendingNumber()
	lastAscendingNumber = lastAscendingNumber + 1
	return lastAscendingNumber
end

local ConversationActions = {}

local function processConversations(store, status, result)
	local state = store:getState()

	if status ~= WebApi.Status.OK then
		warn("WebApi failure in processConversation, Status: "..tostring(status))
		return
	end

	local conversations = result.conversations
	local users = result.users

	local convoIds = {}
	local userIds = {}
	for _, convo in ipairs(conversations) do
		store:dispatch(ReceivedConversation(convo))
		table.insert(convoIds, convo.id)
	end

	for _, user in pairs(users) do
		if state.Users[user.id] == nil then
			store:dispatch(AddUser(user))
			table.insert(userIds, user.id)
		end
	end

	store:dispatch(ConversationActions.GetLatestMessages(convoIds))
	store:dispatch(ConversationActions.GetUserPresences(userIds))
end

local function getUserConversations(store, pageNumber, pageSize)
	local status, result = WebApi.GetUserConversations(pageNumber, pageSize)

	if status ~= WebApi.Status.OK then
		return status, result
	end

	if #result.conversations < pageSize then
		store:dispatch(ReceivedOldestConversation(true))
		store:dispatch(ConversationActions.CreateMockOneOnOneConversationsAsync())
	end

	return status, result
end

local function shouldFetchPageConversations(state)
	if state.ChatAppReducer.ConversationsAsync.pageConversationsIsFetching then
		return false
	end
	return true
end

function ConversationActions.GetLocalUserConversationsAsync(pageNumber, pageSize)
	return function(store)
		if not shouldFetchPageConversations(store:getState()) then
			return Promise.new(function(resolve) resolve() end)
		end
		-- sets status in state we are fetching pages
		store:dispatch(RequestPageConversations())

		return Promise.new(function(resolve)
			local status, result = getUserConversations(store, pageNumber, pageSize)
			processConversations(store, status, result)
			store:dispatch(ReceivedPageConversations())

			resolve()
		end)
	end
end

local function refreshMessages(conversationId, store)
	--Returns true if their are no new messages
	local status, messages = WebApi.GetMessages(conversationId, 1)

	if status ~= WebApi.Status.OK then
		warn("WebApi failure in refreshMessages", status)
		return true
	end

	local conversation = store:getState().ChatAppReducer.Conversations[conversationId]
	if not conversation then
		return false
	end

	local hasNewMessages = false
	if conversation.messages:Length() > 0 then
		local mostRecentKnown = conversation.messages:Last().sent:GetUnixTimestamp()
		for _, message in ipairs(messages) do
			if message.sent:GetUnixTimestamp() > mostRecentKnown then
				hasNewMessages = true
				break
			end
		end
	else
		hasNewMessages = #messages > 0
	end

	if hasNewMessages then
		local newMessageNotificationReceivedLocalTime = tick()
		store:dispatch(
			ConversationActions.GetNewMessages(
				conversationId,
				false,
				newMessageNotificationReceivedLocalTime
			)
		)
	end

	return not hasNewMessages
end

local function hasSameParticipants(existingConvo, newConvo)
	--O(n^2), but n is at most 6!
	if #existingConvo.participants ~= #newConvo.participants then
		return false
	end
	for _, existingPart in ipairs(existingConvo.participants) do
		local found = false
		for _, newPart in ipairs(newConvo.participants) do
			if existingPart == newPart then
				found = true
				break
			end
		end
		if not found then
			return false
		end
	end
	return true
end

local function refreshConversations(pageNumber, store)

	local status, result = getUserConversations(store, pageNumber, Constants.PageSize.GET_CONVERSATIONS)
	if status ~= WebApi.Status.OK then
		warn("WebApi failure in WebApi.GetUserConversations")
		return
	end

	local state = store:getState()
	local conversations = result.conversations
	local users = result.users

	for _, user in pairs(users) do
		if state.Users[user.id] == nil then
			store:dispatch(AddUser(user))
		end
	end

	local needInitialMessages = {}

	for _, convo in ipairs(conversations) do
		local convoIsIdentical = true
		if state.ChatAppReducer.Conversations[convo.id] then
			local existing = state.ChatAppReducer.Conversations[convo.id]
			if existing.title ~= convo.title then
				convoIsIdentical = false
				store:dispatch(RenamedGroupConversation(convo.id, convo.title))
			end
			if not hasSameParticipants(convo, existing) then
				convoIsIdentical = false
				store:dispatch(ChangedParticipants(convo.id, convo.participants))
			end
			if not existing.fetchingOlderMessages then
				convoIsIdentical = convoIsIdentical and refreshMessages(existing.id, store)
			end
		else
			convoIsIdentical = false
			store:dispatch(ReceivedConversation(convo))
			table.insert(needInitialMessages, convo.id)
		end
		if convoIsIdentical then
			return
		end
	end

	--We're going to continue getting conversations
	--until we run into one that hasn't changed. This,
	--potentially, means that we're getting all conversations,
	--if all conversations have changed.
	if #conversations == Constants.PageSize.GET_CONVERSATIONS then
		refreshConversations(pageNumber+1, store)
	end
end

function ConversationActions.StartOneToOneConversation(conversation, onSuccess)
	return function(store)
		spawn(function()
			local userId = nil
			for _, participantId in ipairs(conversation.participants) do
				if participantId ~= tostring(Players.LocalPlayer.UserId) then
					userId = participantId
				end
			end
			local status, result = WebApi.StartOneToOneConversation(userId, conversation.clientId)
			if status ~= WebApi.Status.OK then
				warn("WebApi failure in StartOneToOneConversation, status:", status)
				return
			end

			--The StartOneToOneConversation API endpoint returns a conversation with a null
			--title. Have to call GetConversation to get correct data.
			status, result = WebApi.GetConversations({result.id})

			if status ~= WebApi.Status.OK then
				warn("WebApi failure in GetConversations, status:", status)
				return
			end

			if #result.conversations <= 0 then
				warn("WebApi invalid result from GetConversations")
				return
			end

			local serverConversation = result.conversations[1]
			store:dispatch(ReceivedConversation(serverConversation))

			store:dispatch(RemovedConversation(conversation.id))
			if onSuccess then
				if LuaChatCreateChatEnabled then
					onSuccess(serverConversation.id)
				else
					onSuccess(serverConversation)
				end
			end
		end)
	end
end

function ConversationActions.CreateMockOneOnOneConversationsAsync()
	return function(store)
		local onFetchedAllFriends = function()
			local state = store:getState()
			local needsMockConversation = {}
			for userId, user in pairs(state.Users) do
				if user.isFriend then
					needsMockConversation[userId] = user
				end
			end

			for _, conversation in pairs(state.ChatAppReducer.Conversations) do
				if conversation.conversationType == ConversationModel.Type.ONE_TO_ONE_CONVERSATION then
					for _, userId in ipairs(conversation.participants) do
						needsMockConversation[userId] = nil
					end
				end
			end

			for _, user in pairs(needsMockConversation) do
				local conversation = ConversationModel.fromUser(user)
				store:dispatch(ReceivedConversation(conversation))
			end
		end

		return Promise.new(function(resolve)
			store:dispatch(ConversationActions.GetAllFriendsAsync())
			onFetchedAllFriends()
			resolve()
		end)
	end
end

function ConversationActions.RefreshConversations()
	return function(store)
		local state = store:getState()
		if next(state.ChatAppReducer.Conversations) == nil then
			spawn(function()
				store:dispatch(ConversationActions.GetLocalUserConversationsAsync(1, Constants.PageSize.GET_CONVERSATIONS))
			end)
		else
			spawn(function()
				refreshConversations(1, store)
			end)
		end
	end
end

function ConversationActions.GetConversations(convoIds)
	return function(store)
		local status, result = WebApi.GetConversations(convoIds)

		processConversations(store, status, result)
		return status
	end
end

local function shouldGetAllFriends(state)
	if state.UsersAsync.allFriendsIsFetching then
		return false
	end
	return true
end

function ConversationActions.GetAllFriendsAsync()
	return function(store)
		if not shouldGetAllFriends(store:getState()) then
			return Promise.new(function(resolve) resolve() end)
		end
		--marks in store we are fetching
		store:dispatch(RequestAllFriends())

		if LuaChatUseNewFriendsAndPresenceEndpoint then
			-- New endpoint lets us pass in a uid to get one page of all of a user's friends.
			return Promise.new(function(resolve, reject)
				-- We cannot use LocalUserId here unless LuaAppStarterScript is enabled.
				local localUserId = tostring(Players.LocalPlayer.UserId)
				local status, result = WebApi.GetFriends(localUserId)
				if status == WebApi.Status.OK then
					local state = store:getState()

					local friendsWhoNeedPresence = {}
					for friendUserId, user in pairs(result) do
						if state.Users[friendUserId] == nil then
							store:dispatch(AddUser(user))
							table.insert(friendsWhoNeedPresence, friendUserId)
						else
							store:dispatch(SetUserIsFriend(friendUserId, user.isFriend))
						end
					end

					local presenceStatus, presenceResult = WebApi.GetUserPresences(friendsWhoNeedPresence)
					if presenceStatus == WebApi.Status.OK then
						for userId, presenceModel in pairs(presenceResult) do
							store:dispatch(ReceivedUserPresence(
								userId, presenceModel.presence, presenceModel.lastLocation, presenceModel.placeId
							))
						end
					end

					store:dispatch(ReceivedAllFriends())
					resolve(status, result)
				else
					reject(status, result)
				end
			end)
		else
			-- Continue using the old endpoint. We need to do extra work by fetching the amount
			-- of friends a user has to determine if we've fetched the final friend page.
			return Promise.new(function(resolve)
				local state = store:getState()
				local getFriendCountStatus, totalCount = WebApi.GetFriendCount()
				if getFriendCountStatus ~= WebApi.Status.OK then
					return
				end
				local count = 0
				local page = 1
				local needsPresence = {}
				while count < totalCount do
					local getFriendsStatus, result = WebApi.GetFriends(page)
					page = page + 1
					if getFriendsStatus ~= WebApi.Status.OK then
						return
					end

					local lastCount = count
					for userId, user in pairs(result) do
						count = count + 1
						if state.Users[userId] == nil then
							store:dispatch(AddUser(user))
							table.insert(needsPresence, userId)
						else
							store:dispatch(SetUserIsFriend(userId, user.isFriend))
						end
					end
					if lastCount == count then
						return
					end
				end

				store:dispatch(ReceivedAllFriends())
				store:dispatch(ConversationActions.GetUserPresences(needsPresence))
				resolve()
			end)
		end
	end
end

function ConversationActions.FriendshipCreated(userId)
	return function(store)
		spawn(function()
			local status, result = WebApi.GetUser(userId)
			if status ~= WebApi.Status.OK then
				warn("WebApi.GetUser failure with status", status, " for user id", userId)
				return
			end

			-- request updated friend count when new friendship is formed
			store:dispatch(GetFriendCount())

			local user = UserModel.fromData(userId, result.Username, true)
			store:dispatch(AddUser(user))
			store:dispatch(ConversationActions.GetUserPresences({userId}))

			local state = store:getState()

			local needsMockConversation = true
			for _, conversation in pairs(state.ChatAppReducer.Conversations) do
				if conversation.conversationType == ConversationModel.Type.ONE_TO_ONE_CONVERSATION then
					for _, participantId in ipairs(conversation.participants) do
						if participantId == userId then
							needsMockConversation = false
							break
						end
					end
				end
			end

			if needsMockConversation then
				local conversation = ConversationModel.fromUser(user)
				store:dispatch(ReceivedConversation(conversation))
			end
		end)
	end
end

function ConversationActions.GetAllUserPresences()
	return function(store)
		spawn(function()
			local users = store:getState().Users;
			local userIds = {}
			for userId, _ in pairs(users) do
				table.insert(userIds, userId)
			end
			store:dispatch(ConversationActions.GetUserPresences(userIds))
		end)
	end
end

local function shouldFetchUserPresences(state, userIds)
	local filteredUserIds = Functional.Filter(userIds, function(userId)
		local userAS = state.UsersAsync[userId]
		if userAS and userAS.presenceIsFetching then
			return false
		end
		return true
	end)

	if #filteredUserIds == 0 then
		return false, filteredUserIds
	end

	return true, filteredUserIds
end

function ConversationActions.GetUserPresences(userIds)
	return function(store)
		local ret, newUserIds = shouldFetchUserPresences(store:getState(), userIds)
		if not ret then
			return
		end

		for _, v in ipairs(newUserIds) do
			store:dispatch(RequestUserPresence(v))
		end

		spawn(function()
			local status, result = WebApi.GetUserPresences(newUserIds)

			if status ~= WebApi.Status.OK then
				warn("WebApi failure in GetUserPresences")
				return
			end

			for userId, result in pairs(result) do
				store:dispatch(ReceivedUserPresence(userId, result.presence, result.lastLocation, result.placeId))
			end
		end)
	end
end

local function shouldFetchLatestMessages(state)
	if state.ChatAppReducer.ConversationsAsync.latestMessagesIsFetching then
		return false
	end
	return true
end

function ConversationActions.GetLatestMessages(convoIds)
	return function(store)
		if not shouldFetchLatestMessages(store:getState()) then
			return
		end

		store:dispatch(RequestLatestMessages())

		spawn(function()
			local status, messages = WebApi.GetLatestMessages(convoIds)

			if status ~= WebApi.Status.OK then
				warn("WebApi failure in GetLatestMessages")
				return
			end

			local state = store:getState()
			for _, message in ipairs(messages) do
				local conversation = state.ChatAppReducer.Conversations[message.conversationId]
				if conversation.messages:Get(message.id) == nil then
					if conversation.messages:Last() ~= nil then
						message.previousMessageId = conversation.messages:Last().id
					end
					store:dispatch(ReceivedMessages(message.conversationId, {message}))
				end
			end

			store:dispatch(ReceivedLatestMessages())
		end)
	end
end

function ConversationActions.GetNewMessages(convoId, fromSelf, newMessageNotificationReceivedLocalTime)
	local function ConversationContainsOldest(conversation, messages)
		return #messages > 0 and conversation.messages:Get(messages[#messages].id) ~= nil
	end

	return function(store)
		spawn(function()
			local conversation = store:getState().ChatAppReducer.Conversations[convoId]
			if not conversation then
				-- If we have not previously cached the conversation, we should first get it.
				local status = store:dispatch(ConversationActions.GetConversations({convoId}))
				if status ~= WebApi.Status.OK then
					warn("WebApi failure in GetNewMessages")
					return
				end
				conversation = store:getState().ChatAppReducer.Conversations[convoId]
				if not conversation then
					warn("Was not able to GetConversation in GetNewMessages")
					return
				end
			end

			local pageSize = Constants.PageSize.GET_NEW_MESSAGES
			local status, messages = WebApi.GetMessages(convoId, pageSize)

			if status ~= WebApi.Status.OK then
				warn("WebApi failure in GetNewMessages")
				return
			end

			local getNewMessageRoundTripTime = tick() - newMessageNotificationReceivedLocalTime
			if LuaChatPerformanceTracking then
				reportToDiagByCountryCode(
					Constants.PerformanceMeasurement.LUA_CHAT_RECEIVE_MESSAGE,
					"MessageReceivedTime",
					getNewMessageRoundTripTime
				)
			end
			-- Did many messages get sent at once?
			-- We may have missed something and need to get catched up
			local lastMessage = conversation and conversation.messages:Last()
			if messages[pageSize] and lastMessage and not ConversationContainsOldest(conversation, messages) then
				repeat
					pageSize = math.min(2 * pageSize, 50)
					local exclusiveMessageStartId = messages[#messages].id
					local moreStatus, moreMessages = WebApi.GetMessages(convoId, pageSize, exclusiveMessageStartId)
					if moreStatus ~= WebApi.Status.OK then
						warn("WebApi failure in GetNewMessages")
						return
					end
					for _, message in ipairs(moreMessages) do
						table.insert(messages, message)
					end
				until ConversationContainsOldest(conversation, messages) or moreMessages[pageSize] == nil
			end

			-- We got a bunch of extra messages in these request
			-- So don't update the ones we already knew about
			local hasUnreadMessages = false
			if conversation then
				local filteredMessages = {}
				local previousMessageId = nil
				for i = #messages, 1, -1 do
					local message = messages[i]
					if not conversation.messages:Get(message.id) then
						hasUnreadMessages = hasUnreadMessages or (not message.read)
						message.previousMessageId = previousMessageId
						table.insert(filteredMessages, message)
					end
					previousMessageId = message.id
				end
				messages = filteredMessages
			end

			local shouldMarkConversationUnread = (not conversation.hasUnreadMessages)
				and (not fromSelf) and hasUnreadMessages

			store:dispatch(ReceivedMessages(convoId, messages, shouldMarkConversationUnread))

			if shouldMarkConversationUnread then
				store:dispatch(IncrementUnreadConversationCount())
			end
		end)
	end
end

function ConversationActions.GetInitialMessages(convoId, exclusiveMessageStartId)
	return function(store)
		store:dispatch(SetConversationLoadingStatus(convoId, Constants.ConversationLoadingState.LOADING))

		spawn(function()
			local status, messages = WebApi.GetMessages(convoId, GET_MESSAGES_PAGE_SIZE, exclusiveMessageStartId)

			if status ~= WebApi.Status.OK then
				return
			end

			store:dispatch(ReceivedMessages(convoId, messages))

			store:dispatch(SetConversationLoadingStatus(convoId, Constants.ConversationLoadingState.DONE))

		end)
	end
end

function ConversationActions.RemoveUserFromConversation(userId, convoId, callback)
	return function(store)
		local conversation = store:getState().ChatAppReducer.Conversations[convoId]
		if conversation and not conversation.isUserLeaving then
			store:dispatch(SetUserLeavingConversation(convoId, true))
			spawn(function()
				local status = WebApi.RemoveUserFromConversation(userId, convoId)

				if status ~= WebApi.Status.OK then
					warn("WebApi.RemoveUserFromConversation failure", status)
					local updatedConversation = store:getState().ChatAppReducer.Conversations[convoId]
					if userId == tostring(Players.LocalPlayer.UserId) then
						local titleKey = "Feature.Chat.Heading.FailedToLeaveGroup"
						local messageKey = "Feature.Chat.Message.FailedToLeaveGroup"
						local messageArguments = {
							CONVERSATION_TITLE = getConversationDisplayTitle(updatedConversation),
						}
						local alert = Alert.new(titleKey, messageKey, messageArguments, Alert.AlertType.DIALOG)
						store:dispatch(ShowAlert(alert))
					else
						local user = store:getState().Users[userId]
						local titleKey = "Feature.Chat.Heading.FailedToRemoveUser"
						local messageKey = "Feature.Chat.Message.FailedToRemoveUser"
						local messageArguments = {
							CONVERSATION_TITLE = getConversationDisplayTitle(updatedConversation),
							USERNAME = user.name,
						}
						local alert = Alert.new(titleKey, messageKey, messageArguments, Alert.AlertType.DIALOG)
						store:dispatch(ShowAlert(alert))
					end
				end
				if callback then
					callback(status == WebApi.Status.OK)
				end
				store:dispatch(SetUserLeavingConversation(convoId, false))
			end)
		end
	end
end

function ConversationActions.RenameGroupConversation(convoId, newName, callback)
	return function(store)
		spawn(function()

			local status = WebApi.RenameGroupConversation(convoId, newName)

			if status == WebApi.Status.MODERATED then
				warn("Message was moderated")
				local messageKey = "Feature.Chat.Response.ChatNameFullyModerated"
				local toastModel = ToastModel.new(Constants.ToastIDs.GROUP_NAME_MODERATED, messageKey)
				store:dispatch(ShowToast(toastModel))
			elseif status ~= WebApi.Status.OK then
				local conversation = store:getState().ChatAppReducer.Conversations[convoId]
				local titleKey = "Feature.Chat.Heading.FailedToRenameConversation"
				local messageKey = "Feature.Chat.Message.FailedToRenameConversation"
				local messageArguments = {
					EXISTING_NAME = getConversationDisplayTitle(conversation),
					NEW_NAME = newName,
				}
				local alert = Alert.new(titleKey, messageKey, messageArguments, Alert.AlertType.DIALOG)
				store:dispatch(ShowAlert(alert))
			end

			if callback then
				callback()
			end
		end)
	end
end

local function SendMessageHelper(store, conversationId, messageText, isSharedGameUrl)
	local conversation = store:GetState().ChatAppReducer.Conversations[conversationId]

	local function GetSpoofedLatestMessageTime()
		-- Get the most recent message date of our messages so we can create a fake date after those
		local lastMessageInConvo = conversation.messages:Last()
		local lastSendingMessageInConvo = conversation.sendingMessages:Last()

		local lastSendingDate;
		if lastMessageInConvo then
			lastSendingDate = lastMessageInConvo.sent:GetUnixTimestamp()
		end
		if lastSendingMessageInConvo then
			local tempDate = lastSendingMessageInConvo.sent:GetUnixTimestamp()
			lastSendingDate = lastSendingDate and math.max(lastSendingDate, tempDate) or tempDate
		end

		-- Add 0.001 seconds to the message date so that we show up slightly after the current one
		local fakeSendingDate = lastSendingDate and DateTime.fromUnixTimestamp(lastSendingDate + 0.001) or DateTime.now()
		return fakeSendingDate
	end

	local previousMessageId = nil

	local message = {
		id = "sending-message-" .. MockId(),
		order = getAscendingNumber(),
		content = messageText,
		conversationId = conversationId,
		senderTargetId = tostring(Players.LocalPlayer.UserId),
		senderType = "User",
		sent = GetSpoofedLatestMessageTime(),
		moderated = false,
		failed = false,
		previousMessageId = previousMessageId,
	}

	if not isSharedGameUrl then
		store:dispatch(SendingMessage(conversationId, message))
	end

	--Making the assumption that when a message is sent, there are no new messages
	--not already in the store... potential race condition
	local status, result = WebApi.SendMessage(conversationId, messageText, previousMessageId)
	return conversation, message, status, result
end

if FFlagShareGameToChatStatusAnalytics then
	function ConversationActions.SendMessage(conversationId, messageText, messageSentLocalTime)
		return function(store)
			return Promise.new(function(resolve)
				spawn(function()
					local conversation, message, status, result = SendMessageHelper(store, conversationId, messageText, false)

					if status == WebApi.Status.OK then
						local sendMessageRoundTripTime = tick() - messageSentLocalTime
						if LuaChatPerformanceTracking then
							reportToDiagByCountryCode(
								Constants.PerformanceMeasurement.LUA_CHAT_SEND_MESSAGE,
								"MessageSentTime",
								sendMessageRoundTripTime
							)
						end
						if conversation.messages:Length() > 0 then
							result.previousMessageId = conversation.messages:Last().id
						end
						store:dispatch(SentMessage(conversationId, message.id))

						store:dispatch(ReceivedMessages(conversationId, {result}))
					elseif status == WebApi.Status.MODERATED then
						store:dispatch(MessageModerated(conversationId, message.id))
						warn("Message was moderated.")
					else
						store:dispatch(MessageFailedToSend(conversationId, message.id))
						warn("Message could not be sent.")
					end

					resolve(status)
				end)
			end)
		end
	end
else
	function ConversationActions.SendMessage(conversationId, messageText, toastModeratedMessageKey, messageSentLocalTime)
		return function(store)
			spawn(function()
				local conversation, message, status, result = SendMessageHelper(store, conversationId, messageText, false)

				if status == WebApi.Status.OK then
					local sendMessageRoundTripTime = tick() - messageSentLocalTime
					if LuaChatPerformanceTracking then
						reportToDiagByCountryCode(
							Constants.PerformanceMeasurement.LUA_CHAT_SEND_MESSAGE,
							"MessageSentTime",
							sendMessageRoundTripTime
						)
					end
					if conversation.messages:Length() > 0 then
						result.previousMessageId = conversation.messages:Last().id
					end
					store:dispatch(SentMessage(conversationId, message.id))

					store:dispatch(ReceivedMessages(conversationId, {result}))
				elseif status == WebApi.Status.MODERATED then
					store:dispatch(MessageModerated(conversationId, message.id))
					warn("Message was moderated.")

					if toastModeratedMessageKey and toastModeratedMessageKey:len() > 0 then
						local toastModel = ToastModel.new(Constants.ToastIDs.MESSAGE_WAS_MODERATED, toastModeratedMessageKey)
						store:dispatch(ShowToast(toastModel))
					end
				else
					store:dispatch(MessageFailedToSend(conversationId, message.id))
					warn("Message could not be sent.")
				end
			end)
		end
	end
end

function ConversationActions.ShareGame(conversationId, gameUrl)
	return function(store)
		spawn(function()
			if store:GetState().ChatAppReducer.ShareGameToChatAsync.sharingGame or
					store:GetState().ChatAppReducer.ShareGameToChatAsync.sharedGame then
				return
			end

			ShareGameToChatThunks.Sharing(store)
			local messageText = truncateAssetLink(gameUrl)
			local conversation, message, status, result = SendMessageHelper(store, conversationId, messageText, true)

			if status == WebApi.Status.OK then
				if conversation.messages:Length() > 0 then
					result.previousMessageId = conversation.messages:Last().id
				end
				store:dispatch(SentMessage(conversationId, message.id))

				store:dispatch(ReceivedMessages(conversationId, {result}))

				ShareGameToChatThunks.Shared(store)
			elseif status == WebApi.Status.MODERATED then
				ShareGameToChatThunks.FailedToShare(store)
				warn("game was moderated.")
			else
				ShareGameToChatThunks.FailedToShare(store)
				warn("game could not be sent.")
			end
		end)
	end
end

function ConversationActions.CreateConversation(conversation, callback)
	return function(store)
		spawn(function()
			if LuaChatCreateChatEnabled then
				if #conversation.participants == 1 then
					store:dispatch(ConversationActions.StartOneToOneConversation(conversation,callback))
				else
					local status, realConversation = WebApi.StartGroupConversation(conversation)
					if status == WebApi.Status.OK then
						store:dispatch(ReceivedConversation(realConversation))
						if callback then
							callback(realConversation.id)
						end
					else
						warn("Conversation could not be created, status:", status)
						if callback then
							callback(nil)
						end
					end
				end
			else
				local status, realConversation = WebApi.StartGroupConversation(conversation)
				if status == WebApi.Status.OK then
					if realConversation.isDefaultTitle and #conversation.title > 0 then
						--When calling the StartGroupConversation endpoint,
						--No explicit feedback regarding whether or not conversation
						--title was moderated, have to infer like this
						warn("Group name was moderated")
						local messageKey = "Feature.Chat.Response.ChatNameFullyModerated"
						local toastModel = ToastModel.new(Constants.ToastIDs.GROUP_NAME_MODERATED, messageKey)
						store:dispatch(ShowToast(toastModel))
					end
					store:dispatch(ReceivedConversation(realConversation))
					if callback then
						callback(realConversation.id)
					end
				else
					warn("Conversation could not be created, status:", status)
					if callback then
						callback(nil)
					end
				end
			end
		end)
	end
end

function ConversationActions.AddUsersToConversation(convoId, participants, callback)
	return function(store)
		spawn(function()
			local status = WebApi.AddUsersToConversation(convoId, participants)
			if status ~= WebApi.Status.OK then
				warn("Users could not be added to conversation, status:", status)
			end
			if callback then
				callback(status == WebApi.Status.OK)
			end
		end)
	end
end

function ConversationActions.GetOlderMessages(convoId, messageId) -- Message ID of the message to collect more after
	return function(store)
		store:dispatch(FetchingOlderMessages(convoId, true))
		spawn(function()
			local status, messages = WebApi.GetMessages(convoId, GET_MESSAGES_PAGE_SIZE, messageId)
			store:dispatch(FetchingOlderMessages(convoId, false))
			if status ~= WebApi.Status.OK then
				warn("WebApi failure in GetMessages, with status:", status)
				return
			end

			if #messages < GET_MESSAGES_PAGE_SIZE then
				store:dispatch(FetchedOldestMessage(convoId, true))
			end

			if #messages <= 0 then
				return
			end

			store:dispatch(ReceivedMessages(convoId, messages, nil, messageId))
		end)
	end
end

function ConversationActions.GetUnreadConversationCountAsync()
	return function(store)
		return Promise.new(function()
			local status, unreadConversationCount = WebApi.GetUnreadConversationCount()

			if status ~= WebApi.Status.OK then
				warn("WebApi failure in GetUnreadConversationCount, with status", status)
				return
			end

			store:dispatch(SetUnreadConversationCount(unreadConversationCount))
		end)
	end
end

function ConversationActions.MarkConversationAsRead(conversationId)
	return function(store)
		local conversation = store:getState().ChatAppReducer.Conversations[conversationId]

		if not conversation then
			warn("Conversation not found in MarkConversationAsRead")
			return
		end

		local messages = conversation.messages

		local lastUnreadMessage = nil
		local count = 0
		local lastUreadMessageId = ''
		for _, message in messages:CreateReverseIterator() do
			count = count + 1
			if not message.read then
				lastUnreadMessage = message
				lastUreadMessageId = lastUnreadMessage.id
				break
			end
		end

		spawn(function()

			if lastUnreadMessage or (conversation.hasUnreadMessages and count == 0) then

				local status = WebApi.MarkAsRead(conversationId, lastUreadMessageId)

				if status ~= WebApi.Status.OK then
					warn("WebApi failure in MarkConversationAsRead")
					return
				end
			end
		end)

		if not conversation.hasUnreadMessages then
			-- Conversation is already read, we can safely return early
			return
		end

		store:dispatch(DecrementUnreadConversationCount())

		store:dispatch(ReadConversation(conversationId))

	end
end

return ConversationActions
