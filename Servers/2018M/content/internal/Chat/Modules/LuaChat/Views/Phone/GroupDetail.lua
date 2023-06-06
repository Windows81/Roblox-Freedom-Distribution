local Modules = game:GetService("CoreGui").RobloxGui.Modules
local LuaChat = Modules.LuaChat

local BaseScreen = require(LuaChat.Views.Phone.BaseScreen)
local Constants = require(LuaChat.Constants)
local ToastModel = require(LuaChat.Models.ToastModel)
local DialogInfo = require(LuaChat.DialogInfo)

local GroupDetailComponent = require(LuaChat.Components.GroupDetail)

local PopRoute = require(LuaChat.Actions.PopRoute)
local SetRoute = require(LuaChat.Actions.SetRoute)
local ShowToast = require(LuaChat.Actions.ShowToast)

local Intent = DialogInfo.Intent

local GroupDetail = BaseScreen:Template()
GroupDetail.__index = GroupDetail

function GroupDetail.new(appState, route)
	local self = {}

	self.appState = appState
	self.route = route

	self.groupDetailComponent = GroupDetailComponent.new(appState, route.parameters.conversationId)
	self.rbx = self.groupDetailComponent.rbx
	self.connections = {}

	setmetatable(self, GroupDetail)

	local backButtonConnection = self.groupDetailComponent.BackButtonPressed:Connect(function()
		self.appState.store:dispatch(PopRoute())
	end)
	table.insert(self.connections, backButtonConnection)

	local addFriendsConnection = self.groupDetailComponent.AddFriendsPressed:Connect(function()
		if self.appState.screenManager:GetCurrentView() ~= self then
			return
		end

		local participantCount = #self.groupDetailComponent.conversation.participants
		if participantCount >= Constants.MAX_PARTICIPANT_COUNT + 1 then
			local messageKey = "Feature.Chat.Message.ToastText"
			local messageArguments = {
				friendNum = tostring(Constants.MAX_PARTICIPANT_COUNT+1),
			}
			local toastModel = ToastModel.new(Constants.ToastIDs.TOO_MANY_PEOPLE, messageKey, messageArguments)
			self.appState.store:dispatch(ShowToast(toastModel))
		else
			self.appState.store:dispatch(SetRoute(Intent.EditChatGroup, {
				conversationId = self.groupDetailComponent.conversation.id
			}))
		end
	end)
	table.insert(self.connections, addFriendsConnection)

	return self
end

function GroupDetail:Start()
	BaseScreen.Start(self)

	do
		local connection = self.appState.store.Changed:Connect(function(current, previous)
			local currentConversationId = current.ChatAppReducer.Location.current.parameters.conversationId
			local conversation = current.ChatAppReducer.Conversations[currentConversationId]
			if current ~= previous and conversation then
				self.groupDetailComponent:Update(current, previous)
			else
				if self.appState.screenManager:GetCurrentView() == self then
					self.appState.store:dispatch(SetRoute(nil, {}, Intent.ConversationHub))
				end
			end
		end)
		table.insert(self.connections, connection)
	end
end

-- GroupDetail does not need to slide off-screen when spawning Dialogs.
function GroupDetail:Pause()
	local state = self.appState.store:getState()
	local dialogType = DialogInfo.GetTypeBasedOnIntent(
		self.appState.store:getState().FormFactor,
		state.ChatAppReducer.Location.current.intent
	)

	if dialogType == DialogInfo.DialogType.Popup then
		self.isNextPageGenericDialog = true
	else
		self.isNextPageGenericDialog = false
		BaseScreen.Pause(self)
	end
end

function GroupDetail:Resume()
	if self.isNextPageGenericDialog == nil or self.isNextPageGenericDialog == false then
		BaseScreen.Resume(self)
	end
	self.isNextPageGenericDialog = false
end

function GroupDetail:Stop()
	BaseScreen.Stop(self)

	for _, connection in ipairs(self.connections) do
		connection:Disconnect()
	end

	self.connections = {}
	self.groupDetailComponent:Stop()
end

function GroupDetail:Destruct()
	self.groupDetailComponent:Destruct()
end

return GroupDetail