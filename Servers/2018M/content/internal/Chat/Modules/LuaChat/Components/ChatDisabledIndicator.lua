local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaChat = Modules.LuaChat

local Constants = require(LuaChat.Constants)
local Create = require(LuaChat.Create)
local Signal = require(Common.Signal)

local Text = require(LuaChat.Text)
local getInputEvent = require(LuaChat.Utils.getInputEvent)

local PADDING_HEIGHT = 32
local TEXT_FONT = Enum.Font.SourceSans
local TEXT_FONT_SIZE = Constants.Font.FONT_SIZE_18

local ChatDisabledIndicator = {}

ChatDisabledIndicator.__index = ChatDisabledIndicator

function ChatDisabledIndicator.new(appState)
	local self = {}

	local imageButtonText = appState.localization:Format("Feature.Chat.Label.PrivacySettings")
	local ibtWidth = Text.GetTextWidth(imageButtonText, Enum.Font.SourceSans, Constants.Font.FONT_SIZE_16)

	local imageButton = Create.new "ImageButton" {
		Name = "PrivacySettings",
		AutoButtonColor = false,
		Size = UDim2.new(0, ibtWidth+6, 0, 36),
		BackgroundTransparency = 1,
		LayoutOrder = 3,
		BorderSizePixel = 0,
		ScaleType = "Slice",
		SliceCenter = Rect.new(3,3,4,4),
		Image = "rbxasset://textures/ui/LuaChat/9-slice/input-default.png",
		ImageColor3 = Constants.Color.GREEN_PRIMARY,

		Create.new "TextLabel" {
			Name = "Title",
			Size = UDim2.new(1, 0, 1, 0),
			BackgroundTransparency = 1,
			Font = Enum.Font.SourceSans,
			TextSize = Constants.Font.FONT_SIZE_16,
			TextColor3 = Constants.Color.WHITE,
			Text = imageButtonText,
			TextXAlignment = Enum.TextXAlignment.Center,
			TextYAlignment = Enum.TextYAlignment.Center,
		}
	}

	local textLabelText = appState.localization:Format("Feature.Chat.Message.TurnOnChat")

	local textLabel = Create.new "TextLabel" {
		BackgroundTransparency = 1,
		LayoutOrder = 2,
		Font = TEXT_FONT,
		TextColor3 = Constants.Color.GRAY2,
		TextSize = TEXT_FONT_SIZE,
		Text = textLabelText,
		TextWrapped = true
	}

	self.rbx = Create.new "Frame" {
		Name = "ChatDisabledIndicator",
		BackgroundTransparency = 1,
		Size = UDim2.new(1, 0, 0, 300),

		Create.new "Frame" {
			Name = "IndicatorInner",
			BackgroundTransparency = 1,
			Size = UDim2.new(1, 0, 0, 160),
			Position = UDim2.new(0.5, 0, 0.5, 0),
			AnchorPoint = Vector2.new(0.5, 0.5),

			Create.new "UIListLayout" {
				SortOrder = Enum.SortOrder.LayoutOrder,
				HorizontalAlignment = Enum.HorizontalAlignment.Center,
			},

			Create.new "ImageLabel" {
				BackgroundTransparency = 1,
				Size = UDim2.new(0, 72, 0, 72),
				LayoutOrder = 1,
				Image = "rbxasset://textures/ui/LuaChat/icons/ic-friends.png",
			},

			textLabel,

			imageButton,
		},
	}

	local function rescaleFromParentSize()
		local parentSize = self.rbx.AbsoluteSize
		local tltHeight = Text.GetTextHeight(textLabelText, TEXT_FONT, TEXT_FONT_SIZE, parentSize.X)
		textLabel.Size = UDim2.new(0,parentSize.X,0,tltHeight+PADDING_HEIGHT)
	end

	self.rbx:GetPropertyChangedSignal("AbsoluteSize"):Connect(rescaleFromParentSize)
	rescaleFromParentSize()

	self.openPrivacySettings = Signal.new()
	getInputEvent(self.rbx.IndicatorInner.PrivacySettings):Connect(function()
		self.openPrivacySettings:Fire()
	end)

	setmetatable(self, ChatDisabledIndicator)

	return self
end

return ChatDisabledIndicator