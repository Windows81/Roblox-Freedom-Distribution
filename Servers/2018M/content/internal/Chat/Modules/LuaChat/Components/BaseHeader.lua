local PlayerService = game:GetService("Players")
local CoreGui = game:GetService("CoreGui")
local TweenService = game:GetService("TweenService")

local Modules = CoreGui.RobloxGui.Modules

local Common = Modules.Common
local LuaChat = Modules.LuaChat

local Components = LuaChat.Components

local ChatGameDrawer = require(Components.ChatGameDrawer)
local Constants = require(LuaChat.Constants)
local DialogInfo = require(LuaChat.DialogInfo)
local GetUser = require(LuaChat.Actions.GetUser)
local PaddedImageButton = require(LuaChat.Components.PaddedImageButton)
local Roact = require(CoreGui.RobloxGui.Modules.Common.Roact)
local RoactRodux = require(CoreGui.RobloxGui.Modules.Common.RoactRodux)
local Text = require(Common.Text)

local PLATFORM_SPECIFIC_CONSTANTS = {
	[Enum.Platform.Android] = {
		BACK_BUTTON_ASSET_ID = "rbxasset://textures/ui/LuaChat/icons/ic-back-android.png",
	},

	Default = {
		BACK_BUTTON_ASSET_ID = "rbxasset://textures/ui/LuaChat/icons/ic-back.png",
	},
}

local TITLE_LABEL_MAX_WIDTH = 200
local TITLE_LABEL_HEIGHT = 25

local function getPlatformSpecific(platform)
	return PLATFORM_SPECIFIC_CONSTANTS[platform] or PLATFORM_SPECIFIC_CONSTANTS.Default
end

local BaseHeader = {}

--[[
	This type of pseudo-inheritance for components is usually bad, but this is a special exception.
	It is not recommended to do this.
]]
function BaseHeader:Template()
	local class = {}
	for key, value in pairs(self) do
		class[key] = value
	end
	return class
end

function BaseHeader:SetPlatform(platform)
	self.platform = platform
end

function BaseHeader:SetTitle(text)
	local label = self.titleLabel
	if label then
		local labelFont = label.Font
		local labelTextSize = label.TextSize
		label.Text = Text.Truncate(text, labelFont, labelTextSize, TITLE_LABEL_MAX_WIDTH, "...")
		local titleTextLength = Text.GetTextWidth(label.Text, labelFont, labelTextSize)

		self.titleLabel.Size = UDim2.new(0, titleTextLength, 0, TITLE_LABEL_HEIGHT)
	end

	self.title = text
end

function BaseHeader:SetDefaultSubtitle()
	if (self.dialogType ~= DialogInfo.DialogType.Centered) and (self.dialogType ~= DialogInfo.DialogType.Left) then
		self:SetSubtitle("")
		return
	end

	local displayText = ""
	local player = PlayerService.LocalPlayer
	if player then
		local userId = tostring(player.UserId)
		local localUser = self.appState.store:getState().Users[userId]
		if localUser and not localUser.isFetching then
			if player:GetUnder13() then
				displayText = string.format("%s: <13", localUser.name)
			else
				displayText = string.format("%s: 13+", localUser.name)
			end
		else
			self.appState.store:dispatch(GetUser(userId))
			return
		end
	end

	self:SetSubtitle(displayText)
end

--[[
	Sets the Header's subtitle

	Pass an empty string to hide the subtitle completely.

	Otherwise pass nil to default to the userAge label.
]]
function BaseHeader:SetSubtitle(displayText)
	assert(type(displayText) == "nil" or type(displayText) == "string",
		"Invalid argument number #1 to SetSubtitle, expected string or nil.")

	self.subtitle = displayText

	if displayText == "" then
		self.innerSubtitle.Visible = false
	else
		self.innerSubtitle.Visible = true
		self.innerSubtitle.Text = displayText
	end
end

function BaseHeader:SetBackButtonEnabled(enabled)
	self.backButton.rbx.Visible = enabled
end


function BaseHeader:AddButton(button)
	table.insert(self.buttons, button)
	button.rbx.Parent = self.innerButtons
	button.rbx.LayoutOrder = #self.buttons
end

function BaseHeader:AddContent(content)
	content.rbx.Parent = self.innerContent
end

function BaseHeader:SetConnectionState(connectionState)
	if not self.subtitle then
		self:SetDefaultSubtitle()
	end

	if self.dialogType == DialogInfo.DialogType.Right then
		return
	end

	if connectionState ~= self.connectionState and self.rbx.Parent ~= nil and self.rbx.Parent.Parent ~= nil then
		if connectionState == Enum.ConnectionState.Disconnected then
			self.isDisconnectedOpen = true
			self:DoSizeTweening()
		else
			self.isDisconnectedOpen = false
			self:DoSizeTweening()
		end
		self.connectionState = connectionState
	end
end

function BaseHeader:GetNewBackButton(dialogType)
	local backButton
	if dialogType == DialogInfo.DialogType.Modal then
		backButton = PaddedImageButton.new(self.appState, "Close", "rbxasset://textures/ui/LuaChat/icons/ic-close-gray2.png")
	elseif dialogType == DialogInfo.DialogType.Popup then
		backButton = PaddedImageButton.new(self.appState, "Close", "rbxasset://textures/ui/LuaChat/icons/ic-close-white.png")
	else
		backButton = PaddedImageButton.new(self.appState, "Back", getPlatformSpecific(self.platform).BACK_BUTTON_ASSET_ID)
	end
	backButton.rbx.Position = UDim2.new(0, 0, 0.5, 0)
	backButton.rbx.AnchorPoint = Vector2.new(0, 0.5)
	return backButton
end

function BaseHeader:Destroy()
	for _, conn in pairs(self.connections) do
		conn:Disconnect()
	end
	self.connections = {}
	self.buttons = {}

	-- Destroy an attached Roact Gamedrawer if we have one:
	if self.roactInstanceGameDrawer ~= nil then
		Roact.teardown(self.roactInstanceGameDrawer)
	end
end

function BaseHeader:CreateGameDrawer(store, conversationId, autoshow)
	-- Create the game drawer. Note it's probably not shown yet:
	self.heightOfGameDrawer = 0
	self.hasFriendsInGame = false
	self.isGameDrawerSized = false
	self.isGameDrawerOpen = false
	local newGameDrawer = Roact.createElement(ChatGameDrawer, {
		AnchorPoint = Vector2.new(0, 0),
		conversationId = conversationId,
		Localization = self.appState.localization,
		Position = UDim2.new(0, 0, 0, 0),
		onSize = function(newSize, forceOpen)
			self:SetGameDrawerSize(newSize, forceOpen)
		end,
	})

	-- Wrap this in a store provider so we can monitor store state:
	self.roactInstanceGameDrawer = Roact.mount(Roact.createElement(RoactRodux.StoreProvider, {
		store = store,
	}, {
		newGameDrawer
	}), self.rbx.GameDrawer, "ChatGameDrawer")
end

function BaseHeader:ToggleGameDrawer()
	if self.isGameDrawerOpen == false then
		self.isGameDrawerOpen = true
	else
		self.isGameDrawerOpen = false
	end
	self:DoSizeTweening()
end

-- Note: Start is called whenever we return to a conversation:
function BaseHeader:Start()
	self.lastHeight = -1
	self.lastHeightDisconnected = -1
	self.lastHeightDrawer = -1
	if self.luaChatPlayTogetherEnabled then
		if self.hasFriendsInGame then
			self:OpenDrawer()
		else
			self:CloseDrawer()
		end
	end
end

function BaseHeader:OpenDrawer()
	if self.isGameDrawerSized and (not self.isGameDrawerOpen) then
		self.isGameDrawerOpen = true
		self:DoSizeTweening()
	end
end

function BaseHeader:CloseDrawer()
	if self.isGameDrawerSized and self.isGameDrawerOpen then
		self.isGameDrawerOpen = false
		self:DoSizeTweening()
	end
end

function BaseHeader:InputFocus()
	if self.luaChatPlayTogetherEnabled then
		self:CloseDrawer()
	end
end

-- Set the open game drawer size - and tween it open:
function BaseHeader:SetGameDrawerSize(drawerSize, hasFriendsInGame)
	if drawerSize > 0 and hasFriendsInGame and not self.isGameDrawerSized then
		self.isGameDrawerOpen = true
	end
	self.heightOfGameDrawer = drawerSize
	self.hasFriendsInGame = hasFriendsInGame
	self.isGameDrawerSized = true
	self:DoSizeTweening()
end

-- Do tweening for any drawers that might be open:
function BaseHeader:DoSizeTweening()
	-- Base height of our header is the main contents:
	local desiredHeight = self.heightOfHeader

	-- Disconnected is the network error message:
	if self.isDisconnectedOpen then
		desiredHeight = desiredHeight + self.heightOfDisconnected
		if not self.rbx.Disconnected.Visible or
			(self.lastHeightDisconnected ~= self.heightOfDisconnected) then
			local size = UDim2.new(1, 0, 0, self.heightOfDisconnected)
			local resizeTween = TweenService:Create(
				self.rbx.Disconnected,
				TweenInfo.new(Constants.Tween.DEFAULT_TWEEN_TIME, Constants.Tween.DEFAULT_TWEEN_STYLE, Enum.EasingDirection.In),
				{ Size = size }
			)
			resizeTween:Play()
			self.rbx.Disconnected.Visible = true
			self.lastHeightDisconnected = self.heightOfDisconnected
		end
	else
		if self.rbx.Disconnected.Visible then
			self.rbx.Disconnected.Size = UDim2.new(1, 0, 0, 0)
			self.rbx.Disconnected.Visible = false
			self.lastHeightDisconnected = 0
		end
	end

	if self.luaChatPlayTogetherEnabled then
		-- Game drawer is the list of games being played by participants of this conversation:
		if self.isGameDrawerOpen and self.heightOfGameDrawer then
			desiredHeight = desiredHeight + self.heightOfGameDrawer
			if not self.rbx.GameDrawer.Visible or
				(self.lastHeightDrawer ~= self.heightOfGameDrawer) then
				self.rbx.GameDrawer.Visible = true
				local size = UDim2.new(1, 0, 0, self.heightOfGameDrawer)
				local resizeTween = TweenService:Create(
					self.rbx.GameDrawer,
					TweenInfo.new(Constants.Tween.DEFAULT_TWEEN_TIME, Constants.Tween.DEFAULT_TWEEN_STYLE, Enum.EasingDirection.In),
					{ Size = size }
				)
				resizeTween:Play()
				self.lastHeightDrawer = self.heightOfGameDrawer
			end
		else
			if self.rbx.GameDrawer.Visible then
				self.rbx.GameDrawer.Size = UDim2.new(1, 0, 0, 0)
				self.rbx.GameDrawer.Visible = false
				self.lastHeightDrawer = 0
			end
		end
	end

	-- Set the size of the main drawer:
	if (self.lastHeight ~= desiredHeight) then
		local size = UDim2.new(1, 0, 0, desiredHeight)
		local resizeTween = TweenService:Create(
			self.rbx,
			TweenInfo.new(Constants.Tween.DEFAULT_TWEEN_TIME, Constants.Tween.DEFAULT_TWEEN_STYLE, Enum.EasingDirection.In),
			{ Size = size }
		)
		resizeTween:Play()
		self.lastHeight = desiredHeight
	end
end

return BaseHeader