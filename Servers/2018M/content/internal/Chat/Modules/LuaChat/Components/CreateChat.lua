local CoreGui = game:GetService("CoreGui")
local Players = game:GetService("Players")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaChat = Modules.LuaChat

local Constants = require(LuaChat.Constants)
local ConversationActions = require(LuaChat.Actions.ConversationActions)
local ConversationModel = require(LuaChat.Models.Conversation)
local Create = require(LuaChat.Create)
local DialogInfo = require(LuaChat.DialogInfo)
local Immutable = require(Common.Immutable)
local Signal = require(Common.Signal)


local Components = LuaChat.Components
local FriendSearchBoxComponent = require(Components.FriendSearchBox)
local HeaderLoader = require(Components.HeaderLoader)
local ResponseIndicator = require(Components.ResponseIndicator)
local SectionComponent = require(Components.ListSection)

local RemoveRoute = require(LuaChat.Actions.RemoveRoute)

local Intent = DialogInfo.Intent

local CreateChat = {}
CreateChat.__index = CreateChat

function CreateChat.new(appState)
	local self = {
		appState = appState,
	}
	setmetatable(self, CreateChat)
	self.connections = {}

	self.conversation = ConversationModel.empty()

	self.responseIndicator = ResponseIndicator.new(appState)
	self.responseIndicator:SetVisible(false)

	-- Header:
	self.header = HeaderLoader.GetHeader(appState, Intent.CreateChat)
	self.header:SetDefaultSubtitle()
	self.header:SetTitle(appState.localization:Format("Feature.Chat.Heading.ChatWithFriends"))
	self.header:SetBackButtonEnabled(true)
	self.header:SetConnectionState(Enum.ConnectionState.Disconnected)

	-- Search for friends:
	self.searchComponent = FriendSearchBoxComponent.new(
		appState,
		self.conversation.participants,
		Constants.MAX_PARTICIPANT_COUNT,
		function(user)
			return user.isFriend and user.id ~= tostring(Players.LocalPlayer.UserId)
		end
	)
	self.searchComponent.rbx.LayoutOrder = 3
	local addParticipantConnection = self.searchComponent.addParticipant:Connect(function(id)
		self.searchComponent.search:ReleaseFocus()
		self:ChangeParticipants(Immutable.Set(self.conversation.participants, #self.conversation.participants+1, id))
	end)
	table.insert(self.connections, addParticipantConnection)

	local removeParticipantConnection = self.searchComponent.removeParticipant:Connect(function(id)
		self.searchComponent.search:ReleaseFocus()
		self:ChangeParticipants(Immutable.RemoveValueFromList(self.conversation.participants, id))
	end)
	table.insert(self.connections, removeParticipantConnection)

	-- Assemble the dialog from components we just made:
	self.sectionComponent = SectionComponent.new(appState, nil, 2)
	self.rbx = Create.new"Frame" {
		Size = UDim2.new(1, 0, 1, 0),
		BackgroundTransparency = 1,
		BorderSizePixel = 0,

		Create.new("UIListLayout") {
			Name = "ListLayout",
			SortOrder = Enum.SortOrder.LayoutOrder,
		},
		self.header.rbx,
		Create.new"Frame" {
			Name = "Content",
			Size = UDim2.new(1, 0, 1, -(self.header.heightOfHeader)),
			BackgroundColor3 = Constants.Color.GRAY5,
			BorderSizePixel = 0,
			LayoutOrder = 1,
			ClipsDescendants = true,

			Create.new"UIListLayout" {
				Name = "ListLayout",
				SortOrder = Enum.SortOrder.LayoutOrder,
			},
			self.sectionComponent.rbx,
			self.searchComponent.rbx,
		},
		self.responseIndicator.rbx,
	}

	-- Wire up the save button to actually create our new chat group:
	self.createChat = self.header:CreateHeaderButton("CreateChat", "Feature.Chat.Action.StartChatWithFriends")
	self.header.innerButtons.Position = UDim2.new(1, 0, 0, 0)
	self.createChat.rbx.Size = UDim2.new(0, 60, 1, 0)
	self.createChat:SetEnabled(false)
	local createChatConnection = self.createChat.Pressed:Connect(function()
		self.searchComponent.search:ReleaseFocus()
		if #self.conversation.participants >= Constants.MIN_PARTICIPANT_COUNT then
			self.responseIndicator:SetVisible(true)
			self.appState.store:dispatch(
				ConversationActions.CreateConversation(self.conversation, function(id)
					self.responseIndicator:SetVisible(false)
					if id ~= nil then
						self.ConversationSaved:Fire(id)
					end
					self.appState.store:dispatch(RemoveRoute(Intent.CreateChat))
				end)
			)
		end
	end)
	table.insert(self.connections, createChatConnection)

	self.BackButtonPressed = Signal.new()
	self.header.BackButtonPressed:Connect(function()
		self.searchComponent.search:ReleaseFocus()
		self.BackButtonPressed:Fire()
	end)
	self.ConversationSaved = Signal.new()

	spawn(function()
		self.appState.store:dispatch(ConversationActions.GetAllFriendsAsync())
	end)

	self.tooManyFriendsAlertId = nil

	local headerSizeConnection = self.header.rbx:GetPropertyChangedSignal("AbsoluteSize"):Connect(function()
		self:Resize()
	end)
	table.insert(self.connections, headerSizeConnection)

	return self
end

function CreateChat:Resize()
	-- Content frame must resize if the header changes size (which happens when it shows the "Connecting" message):
	local sizeContent = UDim2.new(1, 0, 1, -self.header.rbx.AbsoluteSize.Y)
	self.rbx.Content.Size = sizeContent

	-- Friends Search frame must resize to fit properly with their peers:
	local sizeSearch = UDim2.new(1, 0, 1, -self.sectionComponent.rbx.AbsoluteSize.Y)
	self.searchComponent.rbx.Size = sizeSearch
end

function CreateChat:ChangeParticipants(participants)
	self.conversation = Immutable.Set(self.conversation, "participants", participants)
	self.searchComponent:Update(participants)
	self.createChat:SetEnabled(#participants >= Constants.MIN_PARTICIPANT_COUNT)
end

function CreateChat:Update(current)
	self.header:SetConnectionState(current.ConnectionState)
	self.searchComponent:Update(self.conversation.participants)
end

function CreateChat:Destruct()
	for _, connection in pairs(self.connections) do
		connection:Disconnect()
	end
	self.connections = {}

	self.header:Destroy()
	self.responseIndicator:Destruct()
	self.searchComponent:Destruct()
	self.rbx:Destroy()
end

return CreateChat