local Modules = game:GetService("CoreGui").RobloxGui.Modules
local LuaChat = Modules.LuaChat
local Components = LuaChat.Components

local DialogInfo = require(LuaChat.DialogInfo)

local BaseScreen = require(LuaChat.Views.Phone.BaseScreen)

local createChatComponent = require(Components.CreateChat)

local PopRoute = require(LuaChat.Actions.PopRoute)
local SetRoute = require(LuaChat.Actions.SetRoute)

local Intent = DialogInfo.Intent

local CreateChat = BaseScreen:Template()
CreateChat.__index = CreateChat

function CreateChat.new(appState, route)
	local self = {
		appState = appState,
		route = route,
		connections = {};
	}
	setmetatable(self, CreateChat)

	self.createChatComponent = createChatComponent.new(appState)
	self.rbx = self.createChatComponent.rbx

	local backButtonPressedConnection = self.createChatComponent.BackButtonPressed:Connect(function()
		self.appState.store:dispatch(PopRoute())
	end)
	table.insert(self.connections, backButtonPressedConnection)

	local conversationSavedConnection = self.createChatComponent.ConversationSaved:Connect(function(id)
		self.appState.store:dispatch(SetRoute(Intent.Conversation, {conversationId = id}, Intent.ConversationHub))
	end)
	table.insert(self.connections, conversationSavedConnection)

	return self
end

function CreateChat:Start()
	BaseScreen.Start(self)
	do
		local connection = self.appState.store.Changed:Connect(function(current, previous)
			self:Update(current, previous)
		end)
		table.insert(self.connections, connection)
	end
end

function CreateChat:Stop()
	for _, connection in pairs(self.connections) do
		connection:Disconnect()
	end
	self.connections = {}

	BaseScreen.Stop(self)
end

function CreateChat:Destruct()
	self.createChatComponent:Destruct()
	self.createChatComponent = nil

	BaseScreen.Destruct(self)
end

function CreateChat:Update(current, previous)
	self.createChatComponent:Update(current, previous)
end

return CreateChat