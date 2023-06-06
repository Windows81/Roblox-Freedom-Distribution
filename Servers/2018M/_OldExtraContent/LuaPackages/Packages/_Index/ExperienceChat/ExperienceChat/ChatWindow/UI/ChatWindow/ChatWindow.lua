local ExperienceChat = script:FindFirstAncestor("ExperienceChat")
local ProjectRoot = ExperienceChat.Parent

local Roact = require(ProjectRoot.Roact)
local llama = require(ProjectRoot.llama)
local Dictionary = llama.Dictionary

local Config = require(ExperienceChat.Config)

local UI = script:FindFirstAncestor("UI")
local ScrollingView = require(UI.ScrollingView)
local TextMessageLabel = require(UI.TextMessageLabel)

local ChatWindow = Roact.Component:extend("ChatWindow")
-- @TODO: Handle default textChannelId RBXGeneral more elegantly
ChatWindow.defaultProps = {
	LayoutOrder = 1,
	size = UDim2.fromScale(1, 1),
	messages = {},
	messageHistory = {
		RBXGeneral = {},
	},
	transparencyValue = Config.ChatWindowBackgroundTransparency,
	textTransparency = 0,
	onChatWindowHovered = function() end,
	onChatWindowNotHovered = function() end,
	messageLimit = Config.ChatWindowMessageLimit,
}

function ChatWindow:init()
	self.getTransparencyOrBindingValue = function(initialTransparency, bindingOrValue)
		if type(bindingOrValue) == "number" then
			return self.props.transparencyValue
		end

		return bindingOrValue:map(function(value)
			return initialTransparency + value * (1 - initialTransparency)
		end)
	end

	self.createChildren = function(history, msgs)
		local result = {}
		if history and history.RBXGeneral then
			local messageCount = Dictionary.count(history.RBXGeneral)
			result = Dictionary.join(
				{
					layout = Roact.createElement("UIListLayout", {
						Padding = UDim.new(0, 4),
						SortOrder = Enum.SortOrder.LayoutOrder,
					}),
				},
				Dictionary.map(history.RBXGeneral, function(messageId, index)
					if messageCount > self.props.messageLimit and index <= (messageCount - self.props.messageLimit) then
						return
					end

					if msgs[messageId].Status and msgs[messageId].Status ~= Enum.TextChatMessageStatus.Success then
						return
					end

					local child = Roact.createElement(TextMessageLabel, {
						textChatMessage = msgs[messageId],
						LayoutOrder = msgs[messageId].Timestamp or index,
						textTransparency = self.getTransparencyOrBindingValue(0, self.props.textTransparency),
						textStrokeTransparency = self.getTransparencyOrBindingValue(0.5, self.props.textTransparency),
					})
					return child, "message" .. index
				end)
			)
		end

		return result
	end
end

function ChatWindow:render()
	return Roact.createElement("Frame", {
		BackgroundColor3 = Config.ChatWindowBackgroundColor3,
		BorderSizePixel = 0,
		LayoutOrder = self.props.LayoutOrder,
		Size = self.props.size,
		BackgroundTransparency = self.getTransparencyOrBindingValue(
			Config.ChatWindowBackgroundTransparency,
			self.props.transparencyValue
		),
		[Roact.Event.MouseEnter] = self.props.onChatWindowHovered,
		[Roact.Event.MouseLeave] = self.props.onChatWindowNotHovered,
	}, {
		scrollingView = Roact.createElement(ScrollingView, {
			size = self.props.size,
		}, self.createChildren(
			self.props.messageHistory,
			self.props.messages
		)),
	})
end

return ChatWindow
