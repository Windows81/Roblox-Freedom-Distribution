local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local LocalizedTextLabel = require(Modules.LuaApp.Components.LocalizedTextLabel)
local LocalizedTextButton = require(Modules.LuaApp.Components.LocalizedTextButton)
local Constants = require(Modules.LuaApp.Constants)

local END_OF_SCROLL_PADDING = 20
local END_OF_SCROLL_FONT_SIZE = 20
local END_OF_SCROLL_MESSAGE_HEIGHT = END_OF_SCROLL_FONT_SIZE
local END_OF_SCROLL_BUTTON_HEIGHT = END_OF_SCROLL_FONT_SIZE + 10
local END_OF_SCROLL_HEIGHT = END_OF_SCROLL_PADDING * 2 + END_OF_SCROLL_MESSAGE_HEIGHT + END_OF_SCROLL_BUTTON_HEIGHT

local function GamesListEndOfScroll(props)
	local backToTopCallback = props.backToTopCallback
	local LayoutOrder = props.LayoutOrder

	return Roact.createElement("Frame", {
		BackgroundTransparency = 1,
		Size = UDim2.new(1, 0, 0, END_OF_SCROLL_HEIGHT),
		LayoutOrder = LayoutOrder,
	}, {
		Message = Roact.createElement(LocalizedTextLabel, {
			Size = UDim2.new(1, 0, 0, END_OF_SCROLL_MESSAGE_HEIGHT),
			Position = UDim2.new(0, 0, 0, END_OF_SCROLL_PADDING),
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Text = "Feature.GamePage.Message.EndOfList",
			TextSize = END_OF_SCROLL_FONT_SIZE,
			Font = Enum.Font.SourceSans,
			TextColor3 = Constants.Color.GRAY2,
			TextXAlignment = Enum.TextXAlignment.Center,
			TextYAlignment = Enum.TextYAlignment.Center,
		}),
		BackToTopButton = Roact.createElement(LocalizedTextButton, {
			Size = UDim2.new(0.5, 0, 0, END_OF_SCROLL_BUTTON_HEIGHT),
			Position = UDim2.new(0.25, 0, 0, END_OF_SCROLL_MESSAGE_HEIGHT + END_OF_SCROLL_PADDING),
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Text = "Feature.GamePage.Action.BackToTop",
			TextSize = END_OF_SCROLL_FONT_SIZE,
			Font = Enum.Font.SourceSans,
			TextColor3 = Constants.Color.BLUE_PRIMARY,
			TextXAlignment = Enum.TextXAlignment.Center,
			TextYAlignment = Enum.TextYAlignment.Center,
			[Roact.Event.Activated] = backToTopCallback,
		}),
	})
end

return GamesListEndOfScroll