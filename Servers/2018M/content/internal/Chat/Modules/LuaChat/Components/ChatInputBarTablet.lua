local CoreGui = game:GetService("CoreGui")
local PlayerService = game:GetService("Players")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaChat = Modules.LuaChat

local Constants = require(LuaChat.Constants)
local Create = require(LuaChat.Create)
local DialogInfo = require(LuaChat.DialogInfo)
local getInputEvent = require(LuaChat.Utils.getInputEvent)
local Intent = DialogInfo.Intent
local SetRoute = require(LuaChat.Actions.SetRoute)
local Signal = require(Common.Signal)
local Text = require(LuaChat.Text)

local FFlagLuaChatShareGameToChatFromChat = settings():GetFFlag("LuaChatShareGameToChatFromChat")

local GAME_ICON = "rbxasset://textures/ui/LuaChat/icons/ic-game.png"
local PRESSED_GAME_ICON = "rbxasset://textures/ui/LuaChat/icons/ic-game-pressed-24x24.png"
local SEND_BUTTON_IMAGE = "rbxasset://textures/ui/LuaChat/graphic/send-white.png"
local SEND_ICON = "rbxasset://textures/ui/LuaChat/icons/ic-send.png"

local GAME_ICON_BOTTOM_PADDING = 8
local MIN_TEXT_HEIGHT = 36
local RIGHT_BUTTON_WIDTH = 52
local RIGHT_BUTTON_HEIGHT = 48
local SEND_BUTTON_BOTTOM_PADDING = 16
local TEXT_FRAME_HEIGHT_DIFF = 28

local function isMessageValid(text)
	if #text >= 160 then
		return false
	end

	-- Only whitespace
	if text:match("^%s*$") then
		return false
	end

	return true
end

local ChatInputBar = {}

function ChatInputBar.new(appState)
	local self = {}
	self.appState = appState
	self.sendButtonEnabled = false
	self.SendButtonPressed = Signal.new()
	self.UserChangedText = Signal.new()
	self.blockUserChangedText = true
	self._analytics = appState.analytics

	self.rbx = Create.new "TextButton" {
		Name = "ChatInputBar",
		Text = "",
		AutoButtonColor = false,
		BackgroundColor3 = Constants.Color.WHITE,
		BorderSizePixel = 0,
		Size = UDim2.new(1, 0, 0, 64),

		Create.new "Frame" {
			Name = "TopBorder",
			Size = UDim2.new(1, 0, 0, 1),
			BackgroundColor3 = Constants.Color.GRAY3,
			BorderSizePixel = 0,
			Position = UDim2.new(0, 0, 0, 0),
		},

		Create.new "Frame" {
			Name = "InputBarFrame",
			Size = UDim2.new(1, -68, 1, -12),
			Position = UDim2.new(0, 12, 0, 6),
			BackgroundTransparency = 1,

			Create.new "TextBox" {
				Name = "InputText",
				BackgroundTransparency = 1,
				Size = UDim2.new(1, 0, 1, 0),
				Position = UDim2.new(0, 0, 0, 0),
				Text = "",
				Font = Enum.Font.SourceSans,
				TextSize = Constants.Font.FONT_SIZE_18,
				TextColor3 = Constants.Text.INPUT,
				TextXAlignment = Enum.TextXAlignment.Left,
				TextYAlignment = Enum.TextYAlignment.Center,
				TextWrapped = true,
				OverlayNativeInput = true,
				ClearTextOnFocus = false,
				ManualFocusRelease = true,
				MultiLine = true,
				PlaceholderText = appState.localization:Format("Feature.Chat.Label.ChatInputPlaceholder"),
				PlaceholderColor3 = Constants.Text.INPUT_PLACEHOLDER,
			}
		},

		Create.new "ImageButton" {
			Name = "GameButton",
			BackgroundTransparency = 1,
			Size = UDim2.new(0, RIGHT_BUTTON_WIDTH, 0, RIGHT_BUTTON_HEIGHT),
			AnchorPoint = Vector2.new(0, 0),
			Position = UDim2.new(1, -RIGHT_BUTTON_WIDTH, 1, -RIGHT_BUTTON_HEIGHT - GAME_ICON_BOTTOM_PADDING),
			Visible = FFlagLuaChatShareGameToChatFromChat,

			Create.new "ImageLabel" {
				Name = "GameIcon",
				BackgroundTransparency = 1,
				Size = UDim2.new(0, 24, 0, 24),
				AnchorPoint = Vector2.new(0.5, 0.5),
				Position = UDim2.new(0.5, 0, 0.5, 0),
				Image = GAME_ICON,
			}
		},

		Create.new "ImageButton" {
			Name = "SendButton",
			BackgroundTransparency = 1,
			Size = UDim2.new(0, 32, 0, 32),
			AnchorPoint = Vector2.new(0, 1),
			Position = UDim2.new(1, -12 - 32, 1, -SEND_BUTTON_BOTTOM_PADDING),
			Image = SEND_BUTTON_IMAGE,
			ImageColor3 = Constants.Color.GRAY3,
			Visible = not FFlagLuaChatShareGameToChatFromChat,

			Create.new "ImageLabel" {
				Name = "Icon",
				BackgroundTransparency = 1,
				Size = UDim2.new(0, 16, 0, 16),
				Position = UDim2.new(0.5, 1, 0.5, 0),
				AnchorPoint = Vector2.new(0.5, 0.5),
				Image = SEND_ICON,
			}
		},
	}

	self.rbx.TouchTap:Connect(function()
		--Sink this tap so the keyboard doesn't close
	end)

	self.textBox = self.rbx.InputBarFrame.InputText

	self.textBox.Focused:Connect(function()
		self.blockUserChangedText = false
	end)

	self.textBox.FocusLost:Connect(function()
		if #self.textBox.Text <= 0 then
			self:Reset()
		end
	end)

	self.textBox:GetPropertyChangedSignal("Text"):Connect(function()
		local text = self.textBox.Text
		if FFlagLuaChatShareGameToChatFromChat then
			self:RightButtonVisibility(string.len(text) == 0)
		end
		local sizeY = Text.GetTextHeight(text, self.textBox.Font, self.textBox.TextSize, self.textBox.AbsoluteSize.X)
		local maxTextHeight = Text.GetTextHeight("A\nB\nC\nD\nE", self.textBox.Font, self.textBox.TextSize,
			self.textBox.AbsoluteSize.X) * 0.95

		if sizeY < MIN_TEXT_HEIGHT then
			sizeY = MIN_TEXT_HEIGHT
		elseif sizeY > maxTextHeight then
			sizeY = maxTextHeight
		end

		self.rbx.Size = UDim2.new(1, 0, 0, sizeY + TEXT_FRAME_HEIGHT_DIFF)

		if isMessageValid(text) then
			self:SetSendButtonEnabled(true)
		else
			self:SetSendButtonEnabled(false)
		end

		if not self.blockUserChangedText then
			self.UserChangedText:Fire()
		end
	end)

	getInputEvent(self.rbx.SendButton):Connect(function()
		self:SendMessage()
	end)

	if FFlagLuaChatShareGameToChatFromChat then
		getInputEvent(self.rbx.GameButton):Connect(function()
			self:ReportBrowseGamesButtonTappedEvent()
			if self.textBox:IsFocused() then
				self.textBox:ReleaseFocus()
			end
			appState.store:dispatch(SetRoute(Intent.BrowseGames, {}))
		end)

		self.rbx.GameButton.InputBegan:Connect(function()
			self:SetGameButtonIcon(true)
		end)

		self.rbx.GameButton.InputEnded:Connect(function()
			self:SetGameButtonIcon(false)
		end)
	end

	setmetatable(self, ChatInputBar)
	return self
end

function ChatInputBar:Reset()
	self.blockUserChangedText = true
	self.textBox.Text = ""
	self.textBox:ResetKeyboardMode()
	self.blockUserChangedText = false
end

function ChatInputBar:RightButtonVisibility(isInputBoxEmpty)
	self.rbx.SendButton.Visible = not isInputBoxEmpty
	self.rbx.GameButton.Visible = isInputBoxEmpty
end

function ChatInputBar:SendMessage()
	local text = self.textBox.Text
	if not isMessageValid(text) then
		return
	end

	self:Reset()
	self.SendButtonPressed:Fire(text)
end

function ChatInputBar:SetSendButtonEnabled(value)
	if self.sendButtonEnabled == value then
		return
	end
	self.sendButtonEnabled = value

	local color = value and Constants.Color.BLUE_PRIMARY or Constants.Color.GRAY3
	self.rbx.SendButton.ImageColor3 = color
end

function ChatInputBar:SetGameButtonIcon(isPressed)
	if isPressed then
		self.rbx.GameButton.GameIcon.Image = PRESSED_GAME_ICON
	else
		self.rbx.GameButton.GameIcon.Image = GAME_ICON
	end
end

function ChatInputBar:GetHeight()
	return self.rbx.Size.Y.Offset
end

function ChatInputBar:ReportBrowseGamesButtonTappedEvent()
	local eventContext = "touch"
	local eventName = "chooseGameToShare"

	local player = PlayerService.LocalPlayer
	local userId = "UNKNOWN"
	if player then
		userId = tostring(player.UserId)
	end

	local additionalArgs = {
		uid = userId,
		cid = self.appState.store:getState().ChatAppReducer.ActiveConversationId
	}

	self._analytics.EventStream:setRBXEventStream(eventContext, eventName, additionalArgs)
end

ChatInputBar.__index = ChatInputBar
return ChatInputBar
