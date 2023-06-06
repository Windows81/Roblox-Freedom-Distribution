local CoreGui = game:GetService("CoreGui")
local UserInputService = game:GetService("UserInputService")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaChat = Modules.LuaChat
local LuaApp = Modules.LuaApp

local Constants = require(LuaChat.Constants)
local Create = require(LuaChat.Create)
local FlagSettings = require(LuaChat.FlagSettings)
local LuaAppFlagSettings = require(LuaApp.FlagSettings)
local Signal = require(Common.Signal)

local Components = LuaChat.Components
local BaseHeader = require(Components.BaseHeader)
local TextButton = require(Components.TextButton)

local UseCppTextTruncation = FlagSettings.UseCppTextTruncation()
local GroupChatIconEnabled = settings():GetFFlag("LuaChatGroupChatIconEnabled")

local HEIGHT_OF_DISCONNECTED = 32

local PLATFORM_SPECIFIC_CONSTANTS = {
	[Enum.Platform.Android] = {
		HEADER_CONTENT_FRAME_Y_OFFSET = 0,
		HEADER_TITLE_FRAME_POSITION_NO_BACK_BUTTON = UDim2.new(0, 15, 0, 0),
		HEADER_TITLE_FRAME_POSITION = UDim2.new(0, 72, 0, 0),
		HEADER_TITLE_FRAME_ANCHOR_POINT = Vector2.new(0, 0),
		HEADER_VERTICAL_ALIGNMENT = Enum.VerticalAlignment.Center,
		HEADER_TEXT_X_ALIGNMENT = 0,
	},
	Default = {
		HEADER_CONTENT_FRAME_Y_OFFSET = 24,
		HEADER_TITLE_FRAME_POSITION_NO_BACK_BUTTON = UDim2.new(0.5, 0, 0, 0),
		HEADER_TITLE_FRAME_POSITION = UDim2.new(0.5, 0, 0, 0),
		HEADER_TITLE_FRAME_ANCHOR_POINT = Vector2.new(0.5, 0),
		HEADER_VERTICAL_ALIGNMENT = Enum.VerticalAlignment.Top,
		HEADER_TEXT_X_ALIGNMENT = 2,
	},
}

local GROUP_CHAT_ICON_HEIGHT = 25
local GROUP_CHAT_ICON_WIDTH = 25
local GROUP_CHAT_ICON = "rbxasset://textures/ui/LuaChat/icons/ic-group-16x16.png"
local TITLE_LABEL_HEIGHT = 25
local TITLE_LABEL_WIDTH = 200
local SUBTITLE_LABEL_HEIGHT = 12
local SUBTITLE_LABEL_WIDTH = 200

local function getPlatformSpecific(platform)
	return PLATFORM_SPECIFIC_CONSTANTS[platform] or PLATFORM_SPECIFIC_CONSTANTS.Default
end

local Header = BaseHeader:Template()
Header.__index = Header

function Header.new(appState, dialogType)
	local self = {}
	setmetatable(self, Header)

	local platform = appState.store:getState().Platform

	local isLuaAppStarterScriptEnabled = LuaAppFlagSettings:IsLuaAppStarterScriptEnabled()

	self:SetPlatform(platform)
	local platformConstants = getPlatformSpecific(platform)

	self.heightOfHeader = UserInputService.NavBarSize.Y + UserInputService.StatusBarSize.Y
	self.heightOfDisconnected = HEIGHT_OF_DISCONNECTED

	self.buttons = {}
	self.connections = {}
	self.appState = appState
	self.dialogType = dialogType
	self.backButton = BaseHeader:GetNewBackButton(dialogType)
	self.backButton.rbx.Visible = false
	self.title = ""
	self.subtitle = nil
	self.connectionState = Enum.ConnectionState.Connected

	self.luaChatPlayTogetherEnabled = FlagSettings.IsLuaChatPlayTogetherEnabled(
		self.appState.store:getState().FormFactor)

	self.BackButtonPressed = Signal.new()
	local backButtonConnection = self.backButton.Pressed:Connect(function()
		self.BackButtonPressed:Fire()
	end)
	table.insert(self.connections, backButtonConnection)

	self.titleLabel = Create.new "TextLabel" {
		Name = "Title",
		AnchorPoint = Vector2.new(0.5, 0.5),
		BackgroundTransparency = 1,
		Font = Enum.Font.SourceSansBold,
		LayoutOrder = 1,
		Size = UDim2.new(0, TITLE_LABEL_WIDTH, 0, TITLE_LABEL_HEIGHT),
		Text = self.title,
		TextColor3 = Constants.Color.WHITE,
		TextSize = Constants.Font.FONT_SIZE_20,
		TextXAlignment = platformConstants.HEADER_TEXT_X_ALIGNMENT,
	}

	if GroupChatIconEnabled then
		self.groupChatIcon = Create.new "ImageLabel" {
			Name = "GroupChatIcon",
			Visible = false,
			BackgroundTransparency = 1,
			LayoutOrder = 0,
			Size = UDim2.new(0, GROUP_CHAT_ICON_WIDTH, 0, GROUP_CHAT_ICON_HEIGHT),
			AnchorPoint = Vector2.new(1, 0),
			Image = GROUP_CHAT_ICON,
		}

		self.innerTitleFrame = Create.new "Frame" {
			Name = "InnerTitleFrame",
			AnchorPoint = Vector2.new(0.5, 0.5),
			BackgroundTransparency = 1,
			LayoutOrder = 0,
			Size = UDim2.new(0, TITLE_LABEL_WIDTH + GROUP_CHAT_ICON_WIDTH, 0, GROUP_CHAT_ICON_HEIGHT),

			Create.new "UIListLayout" {
				SortOrder = Enum.SortOrder.LayoutOrder,
				Padding = UDim.new(0, 5),
				FillDirection = Enum.FillDirection.Horizontal,
				HorizontalAlignment = Enum.HorizontalAlignment.Center,
			},

			self.groupChatIcon,
			self.titleLabel,
		}
	end

	self.innerSubtitle = Create.new "TextLabel" {
		Name = "Subtitle",
		AnchorPoint = Vector2.new(0.5, 0.5),
		BackgroundTransparency = 1,
		Font = Enum.Font.SourceSans,
		LayoutOrder = 2,
		Size = UDim2.new(0, SUBTITLE_LABEL_WIDTH, 0, SUBTITLE_LABEL_HEIGHT),
		Text = "",
		TextColor3 = Constants.Color.WHITE,
		TextSize = Constants.Font.FONT_SIZE_12,
		TextXAlignment = platformConstants.HEADER_TEXT_X_ALIGNMENT,
	}

	self.innerTitles = Create.new "Frame" {
		Name = "Titles",
		AnchorPoint = platformConstants.HEADER_TITLE_FRAME_ANCHOR_POINT,
		BackgroundTransparency = 1,
		Position = self:GetHeaderTitleFramePosition(),
		Size = UDim2.new(0, TITLE_LABEL_WIDTH, 1, 0),

		Create.new "UIListLayout" {
			SortOrder = Enum.SortOrder.LayoutOrder,
			VerticalAlignment = isLuaAppStarterScriptEnabled and Enum.VerticalAlignment.Center
								or platformConstants.HEADER_VERTICAL_ALIGNMENT,
			HorizontalAlignment = Enum.HorizontalAlignment.Center,
		},
	}

	if GroupChatIconEnabled then
		self.innerTitleFrame.Parent = self.innerTitles
	else
		self.titleLabel.Parent = self.innerTitles
	end

	if not isLuaAppStarterScriptEnabled then
		self.innerSubtitle.Parent = self.innerTitles
	end

	self.innerButtons = Create.new "Frame" {
		Name = "Buttons",
		AnchorPoint = Vector2.new(1, 0),
		BackgroundTransparency = 1,
		Position = UDim2.new(1, -5, 0, 0),
		Size = UDim2.new(0, 100, 1, 0),

		Create.new "UIListLayout" {
			FillDirection = Enum.FillDirection.Horizontal,
			HorizontalAlignment = Enum.HorizontalAlignment.Right,
			SortOrder = Enum.SortOrder.LayoutOrder,
			VerticalAlignment = platformConstants.HEADER_VERTICAL_ALIGNMENT,
		},
	}

	self.innerContent = Create.new "Frame" {
		Name = "Content",
		BackgroundTransparency = 1,
		Position = UDim2.new(0, 0, 0, UserInputService.StatusBarSize.Y),
		Size = UDim2.new(1, 0, 0, UserInputService.NavBarSize.Y),

		self.backButton.rbx,
		self.innerTitles,
		self.innerButtons,
	}

	self.innerHeader = Create.new "Frame" {
		Name = "Header",
		BackgroundColor3 = Constants.Color.BLUE_PRESSED,
		BorderSizePixel = 0,
		LayoutOrder = 1,
		Size = UDim2.new(1, 0, 0, self.heightOfHeader),

		self.innerContent,
	}

	self.rbx = Create.new "Frame" {
		Name = "HeaderFrame",
		BackgroundTransparency = 1,
		Size = UDim2.new(1, 0, 0, self.heightOfHeader),

		Create.new "UIListLayout" {
			FillDirection = Enum.FillDirection.Vertical,
			HorizontalAlignment = Enum.HorizontalAlignment.Center,
			SortOrder = Enum.SortOrder.LayoutOrder,
			VerticalAlignment = Enum.VerticalAlignment.Top,
		},

		self.innerHeader,

		Create.new "Frame" {
			Name = "Disconnected",
			AnchorPoint = Vector2.new(0, 1),
			BackgroundColor3 = Constants.Color.GRAY3,
			BorderSizePixel = 0,
			ClipsDescendants = true,
			LayoutOrder = 2,
			Size = UDim2.new(1, 0, 0, 0), -- Note: Deliberately has zero vertical height, will be scaled when shown.

			Create.new "TextLabel" {
				Name = "Title",
				AnchorPoint = Vector2.new(0.5, 1),
				BackgroundTransparency = 1,
				Font = Enum.Font.SourceSans,
				LayoutOrder = 0,
				Position = UDim2.new(0.5, 0, 1, 0),
				Size = UDim2.new(1, 0, 0, HEIGHT_OF_DISCONNECTED),
				Text = appState.localization:Format("Feature.Chat.Message.NoConnectionMsg"),
				TextColor3 = Constants.Color.WHITE,
				TextSize = Constants.Font.FONT_SIZE_14,
			},
		},

		Create.new "Frame" {
			Name = "GameDrawer",
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ClipsDescendants = false,
			LayoutOrder = 3,
			Size = UDim2.new(1, 0, 0, 0), -- Note: Deliberately zero height, will be scaled open.
			Visible = false,
		},
	}

	local parentChangedConnection = self.rbx:GetPropertyChangedSignal("Parent"):Connect(function()
		if self.rbx and self.rbx.Parent then
			if not UseCppTextTruncation then
				game:GetService("RunService").Stepped:wait() -- TextBounds isn't recalculated when this fires so we wait
			end
			self:SetTitle(self.title) -- Again, this can be much cleaner once we have proper truncation support
		end
	end)
	table.insert(self.connections, parentChangedConnection)

	local navBarSignal = UserInputService:GetPropertyChangedSignal("NavBarSize")
	local navBarConnection = navBarSignal:Connect(function()
		self:AdjustLayout()
	end)
	local statusBarSignal = UserInputService:GetPropertyChangedSignal("StatusBarSize")
	local statusBarConnection = statusBarSignal:Connect(function()
		self:AdjustLayout()
	end)
	self:AdjustLayout()
	table.insert(self.connections, navBarConnection)
	table.insert(self.connections, statusBarConnection)

	do
		local connection = appState.store.Changed:Connect(function(state, oldState)
			self:SetPlatform(state.Platform)
			self:SetConnectionState(state.ConnectionState)
		end)
		table.insert(self.connections, connection)
	end

	return self
end

function Header:AdjustLayout()
	self.heightOfHeader = UserInputService.NavBarSize.Y + UserInputService.StatusBarSize.Y
	self.rbx.Size = UDim2.new(1, 0, 0, self.heightOfHeader)
	self.innerHeader.Size = UDim2.new(1, 0, 0, self.heightOfHeader)

	self.innerContent.Position = UDim2.new(0, 0, 0, UserInputService.StatusBarSize.Y)
	self.innerContent.Size = UDim2.new(1, 0, 0, UserInputService.NavBarSize.Y)
end

function Header:CreateHeaderButton(name, textKey)
	local saveGroup = TextButton.new(self.appState, name, textKey)
	self:AddButton(saveGroup)
	return saveGroup
end

function Header:SetBackButtonEnabled(enabled)
	self.backButton.rbx.Visible = enabled
	self.innerTitles.Position = self:GetHeaderTitleFramePosition()
end

function Header:GetHeaderTitleFramePosition()
	if self.backButton and self.backButton.rbx and self.backButton.rbx.Visible then
		return getPlatformSpecific(self.platform).HEADER_TITLE_FRAME_POSITION
	end

	return getPlatformSpecific(self.platform).HEADER_TITLE_FRAME_POSITION_NO_BACK_BUTTON
end

function Header:SetGroupChatIconVisibility(enabled)
	if enabled then
		self.groupChatIcon.Visible = true
	else
		self.groupChatIcon.Visible = false
	end
end

return Header
