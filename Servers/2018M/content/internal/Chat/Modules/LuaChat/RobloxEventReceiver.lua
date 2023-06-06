local CoreGui = game:GetService("CoreGui")
local HttpService = game:GetService("HttpService")
local NotificationService = game:GetService("NotificationService")
local GuiService = game:GetService("GuiService")
local UserInputService = game:GetService("UserInputService")
local Players = game:GetService("Players")

local Modules = CoreGui.RobloxGui.Modules
local LuaChat = Modules.LuaChat
local LuaApp = Modules.LuaApp

local Constants = require(LuaChat.Constants)
local WebApi = require(LuaChat.WebApi)
local ConversationActions = require(LuaChat.Actions.ConversationActions)
local FetchChatEnabled = require(LuaChat.Actions.FetchChatEnabled)
local ReceivedUserTyping = require(LuaChat.Actions.ReceivedUserTyping)
local PlayTogetherActions = require(LuaChat.Actions.PlayTogetherActions)
local DialogInfo = require(LuaChat.DialogInfo)
local Config = require(LuaApp.Config)
local ToastModel = require(LuaChat.Models.ToastModel)
local NotificationType = require(LuaApp.Enum.NotificationType)

local ChangedParticipants = require(LuaChat.Actions.ChangedParticipants)
local PopRoute = require(LuaChat.Actions.PopRoute)
local RemovedConversation = require(LuaChat.Actions.RemovedConversation)
local RenamedGroupConversation = require(LuaChat.Actions.RenamedGroupConversation)
local SetChatEnabled = require(LuaChat.Actions.SetChatEnabled)
local SetConnectionState = require(LuaChat.Actions.SetConnectionState)
local SetRoute = require(LuaChat.Actions.SetRoute)
local ShowToast = require(LuaChat.Actions.ShowToast)
local SetPreloading = require(LuaApp.Actions.SetPreloading)

local FlagSettings = require(LuaApp.FlagSettings)

local isLuaAppFriendshipCreatedSignalREnabled = FlagSettings.IsLuaAppFriendshipCreatedSignalREnabled()
local luaChatDisconnectBackButtonWhenOffScreen = settings():GetFFlag("LuaChatDisconnectBackButtonWhenOffScreen")

local Intent = DialogInfo.Intent

local function jsonDecode(data)
	return HttpService:JSONDecode(data)
end

local function getNewestWithNilPreviousMessageId(messages)
	for id, message, _ in messages:CreateReverseIterator() do
		if message.previousMessageId == nil then
			return id
		end
	end
	return messages.keys[1]
end

local RobloxEventReceiver = {}
function RobloxEventReceiver:init(store)
	local function onChatNotifications(eventData)
		local detail = jsonDecode(eventData.detail)
		local detailType = detail.Type or eventData.detailType
		if detailType == "RemovedFromConversation" then
			local conversationId = tostring(detail.ConversationId)
			store:dispatch(RemovedConversation(conversationId))

			local chatReducer = store:getState().ChatAppReducer
			if chatReducer and chatReducer.Location then
				local currentLocation = chatReducer.Location.current
				if currentLocation and currentLocation.parameters then
					if currentLocation.parameters.conversationId == conversationId then
						local messageKey = "Feature.Chat.Message.RemovedFromConversation"
						local toastModel = ToastModel.new(Constants.ToastIDs.REMOVED_FROM_CONVERSATION, messageKey, {})
						store:dispatch(ShowToast(toastModel))
					end
				end
			end
		elseif detailType == "ConversationRemoved" then
			local conversationId = tostring(detail.ConversationId)
			store:dispatch(RemovedConversation(conversationId))
		elseif detailType == "ConversationTitleChanged" then
			local conversationId = tostring(detail.ConversationId)
			spawn(function()
				local status, result = WebApi.GetConversations({conversationId})

				if status ~= WebApi.Status.OK then
					warn("WebApi failure in RobloxEventReceiver->ConversationTitleChanged")
					return
				end

				local conversations = result.conversations

				if #conversations > 0 then
					local conversation = conversations[1]
					local title = conversation.title
					local isDefaultTitle = conversation.isDefaultTitle
					store:dispatch(
						RenamedGroupConversation(conversationId, title, isDefaultTitle, conversation.lastUpdated)
					)
				end
			end)
		elseif detailType == "ParticipantAdded" then
			local convoId = tostring(detail.ConversationId)
			spawn(function()
				local status, result = WebApi.GetConversations({convoId})

				if status ~= WebApi.Status.OK then
					warn("WebApi failure in RobloxEventReceiver->ParticipantAdded")
					return
				end

				local conversations = result.conversations

				if #conversations > 0 then
					local conversation = conversations[1]
					local participants = conversation.participants
					local title = conversation.title
					store:dispatch(ChangedParticipants(convoId, participants, title, conversation.lastUpdated))
				end
			end)
		elseif detailType == "ParticipantLeft" then
			local convoId = tostring(detail.ConversationId)
			spawn(function()
				local status, result = WebApi.GetConversations({convoId})

				if status ~= WebApi.Status.OK then
					warn("WebApi failure in RobloxEventReceiver->ParticipantLeft", status)
					return
				end

				local conversations = result.conversations

				if #conversations > 0 then
					local conversation = conversations[1]
					local participants = conversation.participants
					local title = conversation.title
					store:dispatch(ChangedParticipants(convoId, participants, title, conversation.lastUpdated))
				end
			end)
		elseif detailType == "AddedToConversation" then
			local conversationId = tostring(detail.ConversationId)
			spawn(function()
				local status = store:dispatch(ConversationActions.GetConversations(conversationId))

				if status ~= WebApi.Status.OK then
					warn("WebApi failure in RobloxEventReceiver->AddedToConversation")
					return
				end
			end)
		elseif detailType == "NewConversation" then
			local conversationId = tostring(detail.ConversationId)
			spawn(function()
				local status = store:dispatch(ConversationActions.GetConversations(conversationId))

				if status ~= WebApi.Status.OK then
					warn("WebApi failure in RobloxEventReceiver->NewConversation")
					return
				end
			end)
		elseif detailType == "NewMessage" or detailType == "NewMessageBySelf" then
			local newMessageNotificationReceivedLocalTime = tick()
			local conversationId = tostring(detail.ConversationId)
			store:dispatch(
				ConversationActions.GetNewMessages(
					conversationId,
					detailType == "NewMessageBySelf",
					newMessageNotificationReceivedLocalTime
				)
			)
		elseif detailType == "ParticipantTyping" then
			local conversationId = tostring(detail.ConversationId)
			local userId = tostring(detail.UserId)
			store:dispatch(ReceivedUserTyping(conversationId, userId))
		elseif detailType == "ConversationUniverseChanged" then
			local conversationId = tostring(detail.ConversationId)
			local universeId = detail.UniverseId and tostring(detail.UniverseId)
			local rootPlaceId = detail.RootPlaceId and tostring(detail.RootPlaceId)
			store:dispatch(PlayTogetherActions.SetPinnedGameForConversation(universeId, rootPlaceId, conversationId))
		end
	end

	local function onPresenceNotifications(eventData)
		local detail = jsonDecode(eventData.detail)
		local userId = tostring(detail.UserId)
		store:dispatch(ConversationActions.GetUserPresences({userId}))
	end

	local function onPresenceBulkNotifications(eventData)
		local detail = jsonDecode(eventData.detail)
		local userIds = {}
		for _, update in ipairs(detail) do
			table.insert(userIds, tostring(update.UserId))
		end
		store:dispatch(ConversationActions.GetUserPresences(userIds))
	end

	local function onAppShellNotifications(eventData)
		-- Note: AppShellNotifications are local and don't come from the
		-- network. eventData.detail is not a structure, unlike other messages.
		local detailType = eventData.detailType
		if detailType == "StartConversationWithUserId" then
			local userId = eventData.detail
			spawn(function()
				local status, result = WebApi.StartOneToOneConversation(userId)

				if status ~= WebApi.Status.OK then
					warn("WebApi failure in RobloxEventReceiver->AppShellNotifications, Status: "..tostring(status) )
					return
				end

				if store:getState().ChatAppReducer.Conversations[result.id] == nil then
					--Call GetConversations to make sure we hit the user and presence
					--endpoints if need be. Being a bit lazy I suppose
					local status = store:dispatch(
						ConversationActions.GetConversations({result.id})
					)

					if status ~= WebApi.Status.OK then
						warn("WebApi failure in RobloxEventReceiver->StartConversationWithUserId, Status: "..tostring(status))
						return
					end
				end

				store:dispatch(SetRoute(Intent.Conversation, {conversationId = result.id}, Intent.ConversationHub))
			end)
		elseif detailType == "StartConversationWithId" then
			local convoId = eventData.detail
			if store:getState().ChatAppReducer.Conversations[convoId] == nil then
				local status = store:dispatch(
					ConversationActions.GetConversations({convoId})
				)

				if status ~= WebApi.Status.OK then
					warn("WebApi failure in RobloxEventReceiver->StartConversationWithId, Status: "..tostring(status))
					return
				end
			end

			store:dispatch(SetRoute(Intent.Conversation, {conversationId = convoId}, Intent.ConversationHub))
		elseif detailType == "Preloading" then
			local isPreloading = eventData.detail == "true"
			store:dispatch(SetPreloading(isPreloading))
		end
	end

	local function onPrivacyNotifications(eventData)
		local detail = jsonDecode(eventData.detail)
		local detailType = detail.Type

		if detailType == "ChatDisabled" then
			store:dispatch(SetChatEnabled(false))
		elseif detailType == "ChatEnabled" then
			store:dispatch(SetChatEnabled(true))
		end
	end

	local function onFriendshipNotifications(eventData)
		local detail = jsonDecode(eventData.detail)
		local detailType = detail.Type

		if detailType == "FriendshipCreated" then
			-- LuaApp's RobloxEventReceiver will create the new user and mock conversation if this flag is on
			if not isLuaAppFriendshipCreatedSignalREnabled then
				local userId = tostring(Players.LocalPlayer.UserId) == tostring(detail.EventArgs.UserId1)
					and detail.EventArgs.UserId2 or detail.EventArgs.UserId1
				store:dispatch(ConversationActions.FriendshipCreated(tostring(userId)))
			end
		end
	end

	local function onRobloxEventReceived(eventData)
		if eventData.namespace == "ChatNotifications" then
			onChatNotifications(eventData)
		elseif eventData.namespace == "PresenceNotifications" then
			onPresenceNotifications(eventData)
		elseif eventData.namespace == "PresenceBulkNotifications" then
			onPresenceBulkNotifications(eventData)
		elseif eventData.namespace == "ChatPrivacySettingNotifications" then
			onPrivacyNotifications(eventData)
		elseif eventData.namespace == "AppShellNotifications" then
			onAppShellNotifications(eventData)
		elseif eventData.namespace == "FriendshipNotifications" then
			onFriendshipNotifications(eventData)
		end
	end

	local lastSeqNum = nil
	local function onRobloxConnectionChanged(connectionHubName, connectionState, seqNum)
		if connectionHubName == "signalR" then
			store:dispatch(SetConnectionState(connectionState))
			if connectionState == Enum.ConnectionState.Connected then
				if seqNum ~= lastSeqNum then
					store:dispatch(FetchChatEnabled(function(chatEnabled)
						if chatEnabled then
							store:dispatch(ConversationActions.RefreshConversations())
							spawn(function()
								store:dispatch(ConversationActions.GetAllFriendsAsync())
							end)
							store:dispatch(ConversationActions.GetAllUserPresences())
						end
					end))
					lastSeqNum = seqNum
				end
				local conversations = store:getState().ChatAppReducer.Conversations
				for conversationId, conversation in pairs(conversations) do
					if conversation.fetchingOlderMessages then
						local messages = conversation.messages
						local exclusiveMessageStartId = getNewestWithNilPreviousMessageId(messages)
						store:dispatch(ConversationActions.GetOlderMessages(conversationId, exclusiveMessageStartId))
					end
				end
			end

		end
	end

	local function onBackButtonPressed()
		if #store:getState().ChatAppReducer.Location.history > 1 then
			store:dispatch(PopRoute())
		else
			GuiService:BroadcastNotification("", NotificationType.BACK_BUTTON_NOT_CONSUMED)
		end
	end

	--Protect this call because Tests run in a downgraded security context
	pcall(function()
		NotificationService.RobloxEventReceived:Connect(onRobloxEventReceived)
		NotificationService.RobloxConnectionChanged:Connect(onRobloxConnectionChanged)
		if not luaChatDisconnectBackButtonWhenOffScreen then
			GuiService.ShowLeaveConfirmation:Connect(onBackButtonPressed)
		end
	end)

	if Config.LuaChat.Debug then
		UserInputService.InputEnded:Connect(function(input, gameProcessed)
			if input.UserInputType == Enum.UserInputType.Keyboard then
				if input.KeyCode == Enum.KeyCode.Left then
					onBackButtonPressed()
				end
			end
		end)
	end
end

return RobloxEventReceiver