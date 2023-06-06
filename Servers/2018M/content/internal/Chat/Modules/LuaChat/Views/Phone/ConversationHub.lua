local UserInputService = game:GetService("UserInputService")

local Modules = game:GetService("CoreGui").RobloxGui.Modules
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local BaseScreen = require(LuaChat.Views.Phone.BaseScreen)
local Create = require(LuaChat.Create)

local ConversationHubComponent = require(LuaChat.Components.ConversationHub)

local DialogInfo = require(LuaChat.DialogInfo)
local Constants = require(LuaChat.Constants)
local ConversationActions = require(LuaChat.Actions.ConversationActions)

local SetRoute = require(LuaChat.Actions.SetRoute)
local SetTabBarVisible = require(LuaApp.Actions.SetTabBarVisible)

local LuaChatCreateChatEnabled = settings():GetFFlag("LuaChatCreateChatEnabled")

local Intent = DialogInfo.Intent

local ConversationHub = BaseScreen:Template()

ConversationHub.__index = ConversationHub

function ConversationHub.new(appState, route)
	local self = {}

	setmetatable(self, ConversationHub)

	self.appState = appState
	self.route = route

	self.ConversationHubComponent = ConversationHubComponent.new(appState)
	self.rbx = self.ConversationHubComponent.rbx

	local spacer = Create.new "Frame" {
		Name = "Spacer",
		Size = UDim2.new(1, 0, 0, UserInputService.BottomBarSize.Y),
		BackgroundColor3 = Constants.Color.WHITE,
		BorderColor3 = Constants.Color.WHITE,
		BackgroundTransparency = 0,
		LayoutOrder = 2,
	}
	spacer.Parent = self.rbx

	self.ConversationHubComponent.ConversationTapped:Connect(function(convoId)
		if self.appState.screenManager:GetCurrentView() ~= self then
			return
		end

		local conversation = self.appState.store:getState().ChatAppReducer.Conversations[convoId]

		if conversation == nil then
			return
		end

		if conversation.serverState == Constants.ServerState.NONE then
			if LuaChatCreateChatEnabled then
				self.appState.store:dispatch(ConversationActions.StartOneToOneConversation(conversation, function(id)
					self.appState.store:dispatch(SetRoute(Intent.Conversation, {conversationId = id}))
				end))
			else
				self.appState.store:dispatch(ConversationActions.StartOneToOneConversation(conversation, function(serverConversation)
					self.appState.store:dispatch(SetRoute(Intent.Conversation, {conversationId = serverConversation.id}))
				end))
			end
		else
			self.appState.store:dispatch(SetRoute(Intent.Conversation, {conversationId = convoId}))
		end
	end)

	self.ConversationHubComponent.CreateChatButtonPressed:Connect(function()
		self.appState.store:dispatch(SetRoute(LuaChatCreateChatEnabled and Intent.CreateChat or Intent.NewChatGroup, {}))
	end)

	return self
end

function ConversationHub:Start()
	BaseScreen.Start(self)
	self.ConversationHubComponent:Start()
	self.appState.store:dispatch(SetTabBarVisible(true))
end

function ConversationHub:Stop()
	BaseScreen.Stop(self)
	self.ConversationHubComponent:Stop()
	self.appState.store:dispatch(SetTabBarVisible(false))
end

function ConversationHub:Resume()
	BaseScreen.Resume(self)
	self.appState.store:dispatch(SetTabBarVisible(true))
end

function ConversationHub:Pause()
	BaseScreen.Pause(self)
	self.appState.store:dispatch(SetTabBarVisible(false))
end

function ConversationHub:Update(state, oldState)
	self.ConversationHubComponent:Update(state, oldState)
end

return ConversationHub