local GuiService = game:GetService("GuiService")
local Modules = game:GetService("CoreGui").RobloxGui.Modules
local UserInputService = game:GetService("UserInputService")

local Constants = require(Modules.LuaChat.Constants)
local ConversationActions = require(Modules.LuaChat.Actions.ConversationActions)
local formatInteger = require(Modules.LuaChat.Utils.formatInteger)
local LocalizedTextLabel = require(Modules.LuaApp.Components.LocalizedTextLabel)
local Roact = require(Modules.Common.Roact)
local RoactAnalyticsSharedGameItem = require(Modules.LuaChat.Services.RoactAnalyticsSharedGameItem)
local RoactRodux = require(Modules.Common.RoactRodux)
local RoactServices = require(Modules.LuaApp.RoactServices)
local Text = require(Modules.Common.Text)

local DEFAULT_BACKGROUND_COLOR = Constants.Color.WHITE
local DEFAULT_GAME_ADDITIONAL_INFO_LABEL_HEIGHT = 14
local DEFAULT_GAME_ADDITIONAL_INFO_LABEL_TEXT_SIZE = 14
local DEFAULT_GAME_CREATOR_LABEL_BOTTOM_PADDING = 3
local DEFAULT_GAME_CREATOR_LABEL_COLOR = Constants.Color.GRAY2
local DEFAULT_GAME_CREATOR_LABEL_HEIGHT = 14
local DEFAULT_GAME_CREATOR_LABEL_TEXT_SIZE = 15
local DEFAULT_GAME_CREATOR_LABEL_TOP_PADDING = 6
local DEFAULT_GAME_NAME_LABEL_COLOR = Constants.Color.GRAY1
local DEFAULT_GAME_NAME_LABEL_HEIGHT = 20
local DEFAULT_GAME_NAME_LABEL_TEXT_SIZE = 23
local DEFAULT_GAME_ICON_LEFT_PADDING = 15
local DEFAULT_GAME_ICON_RIGHT_PADDING = 12
local DEFAULT_GAME_ICON_SIZE = Constants.SharedGamesConfig.Thumbnail.SHOWN_SIZE
local DEFAULT_GAME_ICON_TOP_PADDING = 12
local DEFAULT_ITEM_HEIGHT = 84
local DEFAULT_ITEM_PRESSED_BACKGROUND_COLOR = Constants.Color.GRAY5
local DEFAULT_PRICE_COLOR = Constants.Color.GREEN_PRIMARY
local DEFAULT_ROBUX_ICON_SIZE = 12
local DEFAULT_SEND_BUTTON_ICON_SIZE = 24
local DEFAULT_SEND_BUTTON_LEFT_PADDING = 12
local DEFAULT_SEND_BUTTON_RIGHT_PADDING = 25
local DEFAULT_SEPARATOR_LINE_COLOR = Constants.Color.GRAY4
local DEFAULT_TEXT_FONT = Enum.Font.SourceSans

local GAME_LOADING_ICON = "rbxasset://textures/ui/LuaApp/icons/ic-game.png"
local GAME_BORDER_ICON = "rbxasset://textures/ui/LuaChat/graphic/gr-game-border-60x60.png"
local ROBUX_ICON = "rbxasset://textures/ui/LuaChat/icons/ic-robux.png"
local SEND_BUTTON_ICON = "rbxasset://textures/ui/LuaChat/icons/icon-share-game-24x24.png"
local SENT_BUTTON_ICON = "rbxasset://textures/ui/LuaChat/icons/icon-share-game-pressed-24x24.png"

local SharedGameItem = Roact.PureComponent:extend("SharedGameItem")

SharedGameItem.defaultProps = {
	backgroundColor = DEFAULT_BACKGROUND_COLOR,
	gameAdditionalLabelHeight = DEFAULT_GAME_ADDITIONAL_INFO_LABEL_HEIGHT,
	gameAdditionalLabelTextSize = DEFAULT_GAME_ADDITIONAL_INFO_LABEL_TEXT_SIZE,
	gameCreatorLabelBottomPadding = DEFAULT_GAME_CREATOR_LABEL_BOTTOM_PADDING,
	gameCreatorLabelColor = DEFAULT_GAME_CREATOR_LABEL_COLOR,
	gameCreatorLabelHeight = DEFAULT_GAME_CREATOR_LABEL_HEIGHT,
	gameCreatorLabelTopPadding = DEFAULT_GAME_CREATOR_LABEL_TOP_PADDING,
	gameCreatorLabelTextSize = DEFAULT_GAME_CREATOR_LABEL_TEXT_SIZE,
	gameIconSize = DEFAULT_GAME_ICON_SIZE,
	gameIconLeftPadding = DEFAULT_GAME_ICON_LEFT_PADDING,
	gameIconRightPadding = DEFAULT_GAME_ICON_RIGHT_PADDING,
	gameIconTopPadding = DEFAULT_GAME_ICON_TOP_PADDING,
	gameNameLabelColor = DEFAULT_GAME_NAME_LABEL_COLOR,
	gameNameLabelHeight = DEFAULT_GAME_NAME_LABEL_HEIGHT,
	gameNameLabelTextSize = DEFAULT_GAME_NAME_LABEL_TEXT_SIZE,
	itemPressedBackgroundColor = DEFAULT_ITEM_PRESSED_BACKGROUND_COLOR,
	itemHeight = DEFAULT_ITEM_HEIGHT,
	priceColor = DEFAULT_PRICE_COLOR,
	robuxIconSize = DEFAULT_ROBUX_ICON_SIZE,
	sendButtonIconSize = DEFAULT_SEND_BUTTON_ICON_SIZE,
	sendButtonLeftPadding = DEFAULT_SEND_BUTTON_LEFT_PADDING,
	sendButtonRightPadding = DEFAULT_SEND_BUTTON_RIGHT_PADDING,
	separatorLineColor = DEFAULT_SEPARATOR_LINE_COLOR,
	textFont = DEFAULT_TEXT_FONT
}

function SharedGameItem:init()
    self.state = {
        gameItemDown = false,
		gameItemActivated = false,
		sendButtonDown = false,
		sendButtonActivated = false,
    }

	self.creatorName = nil
	self.gameNameTextLabel = nil
	self.gameCreatorTextLabel = nil

    self.onGameButtonActivated = function()
        self:openGameDetails()
    end

	self.onSendButtonInputBegan = function(_, inputObject)
		if (inputObject.UserInputType == Enum.UserInputType.Touch or
				inputObject.UserInputType == Enum.UserInputType.MouseButton1) and
					inputObject.UserInputState == Enum.UserInputState.Begin then
			self:onSendButtonDown()
		end
	end

	self.onSendButtonInputEnded = function(_, inputObject)
		self:onSendButtonUp()
	end

	self.onGameItemInputBegan = function(_, inputObject)
		if (inputObject.UserInputType == Enum.UserInputType.Touch or
				inputObject.UserInputType == Enum.UserInputType.MouseButton1) and
				 inputObject.UserInputState == Enum.UserInputState.Begin then
			self:onGameItemDown()
		end
	end

	self.onGameItemInputEnded = function(_, inputObject)
		self:onGameItemUp()
	end
end

function SharedGameItem:onSendButtonDown()
	if not self.state.sendButtonDown then
		self:eventDisconnect()

		self.userInputServiceCon = UserInputService.InputEnded:Connect(function()
			self:onSendButtonUp()
		end)

		self:setState({
			sendButtonDown = true,
			sendButtonActivated = false,
		})
	end
end

function SharedGameItem:onSendButtonUp(buttonActivated)
	if self.state.sendButtonDown or self.state.sendButtonActivated ~= buttonActivated then
		self:setState({
			sendButtonDown = false,
			sendButtonActivated = buttonActivated,
		})
	end

	self:eventDisconnect()
end

function SharedGameItem:onGameItemDown()
	if not self.state.gameItemDown then
		self:eventDisconnect()

		self.userInputServiceCon = UserInputService.InputEnded:Connect(function()
			self:onGameItemUp()
		end)

		self:setState({
			gameItemDown = true,
			gameItemActivated = false,
		})
	end
end

function SharedGameItem:onGameItemUp(buttonActivated)
	if self.state.gameItemDown or self.state.gameItemActivated ~= buttonActivated then
		self:setState({
			gameItemDown = false,
			gameItemActivated = buttonActivated,
		})
	end

	self:eventDisconnect()
end

function SharedGameItem:openGameDetails()
    local notificationType = GuiService:GetNotificationTypeList().VIEW_GAME_DETAILS_ANIMATED
    GuiService:BroadcastNotification(string.format("%d", self.props.game.placeId), notificationType)
end

function SharedGameItem:render()
	local activeConversationId = self.props.activeConversationId
	local analytics = self.props.analytics
	local backgroundColor = self.props.backgroundColor
	local gameAdditionalLabelHeight = self.props.gameAdditionalLabelHeight
	local gameAdditionalLabelTextSize = self.props.gameAdditionalLabelTextSize
	local gameCreatorLabelBottomPadding = self.props.gameCreatorLabelBottomPadding
	local gameCreatorLabelColor = self.props.gameCreatorLabelColor
	local gameCreatorLabelHeight = self.props.gameCreatorLabelHeight
	local gameCreatorLabelTextSize = self.props.gameCreatorLabelTextSize
	local gameCreatorLabelTopPadding = self.props.gameCreatorLabelTopPadding
	local gameIconLeftPadding = self.props.gameIconLeftPadding
	local gameIconRightPadding = self.props.gameIconRightPadding
	local gameIconSize = self.props.gameIconSize
	local gameIconTopPadding = self.props.gameIconTopPadding
	local gameIconWidth = gameIconSize + gameIconLeftPadding + gameIconRightPadding
	local gameNameLabelHeight = self.props.gameNameLabelHeight
	local gameNameLabelColor = self.props.gameNameLabelColor
	local gameNameLabelTextSize = self.props.gameNameLabelTextSize
	local gameThumbnails = self.props.gameThumbnails
	local gameUrl =  self.props.game.url
	local itemHeight = self.props.itemHeight
	local itemPressedBackgroundColor = self.props.itemPressedBackgroundColor
	local isSharing = self.props.isSharing
	local placeId = tostring(self.props.game.placeId)
	local playable = self.props.game.isPlayable
	local priceColor = self.props.priceColor
	local robuxIconSize = self.props.robuxIconSize
	local sendButtonIconSize = self.props.sendButtonIconSize
	local sendButtonLeftPadding = self.props.sendButtonLeftPadding
	local sendButtonRightPadding = self.props.sendButtonRightPadding
	local sendButtonWidth = sendButtonIconSize + sendButtonLeftPadding + sendButtonRightPadding
	local separatorLineColor = self.props.separatorLineColor
	local textFont = self.props.textFont

	local additionalInfoFrameHeight = gameAdditionalLabelHeight + gameCreatorLabelBottomPadding
	local showPrice = self.props.game.price ~= nil and playable
	local showAdditionalInfo = showPrice or (not playable)
	local gameIcon = gameThumbnails[placeId] or GAME_LOADING_ICON
	local gameInfoHeight = showAdditionalInfo and
			(gameNameLabelHeight + gameCreatorLabelHeight + 2 * gameCreatorLabelBottomPadding + gameAdditionalLabelHeight) or
			(gameNameLabelHeight + gameCreatorLabelHeight + gameCreatorLabelBottomPadding)


	return Roact.createElement("Frame", {
		BackgroundColor3 = self.state.gameItemDown and itemPressedBackgroundColor or backgroundColor,
		BorderSizePixel = 0,
		Size = UDim2.new(1, 0, 0, itemHeight),
	},{
		Separator = Roact.createElement("Frame", {
			AnchorPoint = Vector2.new(0, 1),
			BackgroundColor3 = separatorLineColor,
			BorderSizePixel = 0,
			Position = UDim2.new(0, gameIconWidth, 1, 0),
			Size = UDim2.new(1, -gameIconWidth, 0, 1),
		}),

		Game = Roact.createElement("Frame", {
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Size = UDim2.new(1, 0, 0, itemHeight),
		}, {
			Layout = Roact.createElement("UIListLayout", {
				FillDirection = Enum.FillDirection.Horizontal,
				SortOrder = Enum.SortOrder.LayoutOrder,
				VerticalAlignment = Enum.VerticalAlignment.Center,
			}),

			GameButtonContainer = Roact.createElement("TextButton", {
				BackgroundTransparency = 1,
				LayoutOrder = 1,
				Size = UDim2.new(1, -sendButtonWidth, 1, 0),
				Text = "",

				[Roact.Event.Activated] = self.onGameButtonActivated,
				[Roact.Event.InputBegan] = self.onGameItemInputBegan,
				[Roact.Event.InputEnded] = self.onGameItemInputEnded,
			},{
				Icon = Roact.createElement("ImageLabel", {
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
					Image = gameIcon,
					Position = UDim2.new(0, gameIconLeftPadding, 0, gameIconTopPadding),
					Size = UDim2.new(0, gameIconSize, 0, gameIconSize),
				}, {
					RoundCornerOverlay = Roact.createElement("ImageLabel", {
						BackgroundTransparency = 1,
						BorderSizePixel = 0,
						Image = GAME_BORDER_ICON,
						Size = UDim2.new(0, gameIconSize, 0, gameIconSize),
					}),
				}),

				GameInfo = Roact.createElement("Frame", {
					AnchorPoint = Vector2.new(0, 0.5),
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
					Position = UDim2.new(0, gameIconWidth, 0.5, 0),
					Size = UDim2.new(1, -gameIconWidth, 0, gameInfoHeight),
				}, {
					Layout = Roact.createElement("UIListLayout", {
						FillDirection = Enum.FillDirection.Vertical,
						SortOrder = Enum.SortOrder.LayoutOrder,
						VerticalAlignment = Enum.VerticalAlignment.Center,
					}),

					Name = Roact.createElement("TextLabel", {
						BackgroundTransparency = 1,
						BorderSizePixel = 0,
						Font = textFont,
						LayoutOrder = 1,
						Size = UDim2.new(1, 0, 0, gameNameLabelHeight),
						Text = self.props.game.name,
						TextColor3 = gameNameLabelColor,
						TextSize = gameNameLabelTextSize,
						TextXAlignment = Enum.TextXAlignment.Left,
						TextYAlignment = Enum.TextYAlignment.Center,
						[Roact.Ref] = function(rbx)
							if rbx then
								self.gameNameTextLabel = rbx
							end
						end,
					}),

					Creator = Roact.createElement(LocalizedTextLabel, {
						BackgroundTransparency = 1,
						BorderSizePixel = 0,
						Font = textFont,
						LayoutOrder = 2,
						Size = UDim2.new(1, 0, 0, gameCreatorLabelHeight + gameCreatorLabelTopPadding),
						Text = {"Feature.Chat.ShareGameToChat.By", creatorName = self.props.game.creatorName},
						TextColor3 = gameCreatorLabelColor,
						TextSize = gameCreatorLabelTextSize,
						TextXAlignment = Enum.TextXAlignment.Left,
						TextYAlignment = Enum.TextYAlignment.Bottom,

						[Roact.Ref] = function(rbx)
							if rbx then
								self.gameCreatorTextLabel = rbx
								self.creatorName = rbx.Text
							end
						end
					}),

					NotAvailableTip = not playable and Roact.createElement(LocalizedTextLabel, {
						BackgroundTransparency = 1,
						BorderSizePixel = 0,
						Font = textFont,
						LayoutOrder = 3,
						Size = UDim2.new(1, 0, 0, additionalInfoFrameHeight),
						Text = "Feature.Chat.ShareGameToChat.GameNotAvailable",
						TextColor3 = gameCreatorLabelColor,
						TextSize = gameAdditionalLabelTextSize,
						TextXAlignment = Enum.TextXAlignment.Left,
						TextYAlignment = Enum.TextYAlignment.Bottom,
					}),

					GamePrice = showPrice and Roact.createElement("Frame", {
						BackgroundTransparency = 1,
						BorderSizePixel = 0,
						LayoutOrder = 3,
						Size = UDim2.new(1, 0, 0, additionalInfoFrameHeight),
					}, {
						Layout = Roact.createElement("UIListLayout", {
							FillDirection = Enum.FillDirection.Horizontal,
							SortOrder = Enum.SortOrder.LayoutOrder,
							VerticalAlignment = Enum.VerticalAlignment.Bottom,
							Padding = UDim.new(0, 3),
						}),

						RobuxIcon = Roact.createElement("ImageLabel", {
							BackgroundTransparency = 1,
							BorderSizePixel = 0,
							Image = ROBUX_ICON,
							LayoutOrder = 1,
							ScaleType = Enum.ScaleType.Fit,
							Size = UDim2.new(0, robuxIconSize, 0, robuxIconSize),
						}),

						Price = Roact.createElement("TextLabel",{
							BackgroundTransparency = 1,
							Size = UDim2.new(1, -15, 1, 0),
							Font = DEFAULT_TEXT_FONT,
							LayoutOrder = 2,
							Text = formatInteger(self.props.game.price),
							TextColor3 = priceColor,
							TextSize = gameAdditionalLabelTextSize,
							TextXAlignment = Enum.TextXAlignment.Left,
							TextYAlignment = Enum.TextYAlignment.Bottom,
						}, {
							padding = Roact.createElement("UIPadding", {
								PaddingLeft = UDim.new(3, 0),
							}),
						}),
					}),
				})
			}),

			SendButtonContainer = Roact.createElement("TextButton", {
				Active = not isSharing,
				BackgroundTransparency = 1,
				ClipsDescendants = true,
				LayoutOrder = 2,
				Position = UDim2.new(1, -sendButtonWidth, 0, 0),
				Size = UDim2.new(0, sendButtonWidth, 1, 0),
				Text = "",

				[Roact.Event.InputBegan] = self.onSendButtonInputBegan,
				[Roact.Event.InputEnded] = self.onSendButtonInputEnded,
				[Roact.Event.Activated] = function()
					if not isSharing then
						self.props.shareGameToChat(activeConversationId, analytics, placeId, gameUrl)
					end
				end,
			},{
				SendButton = Roact.createElement("ImageLabel", {
					AnchorPoint = Vector2.new(0, 0.5),
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
					ClipsDescendants = false,
					Image = self.state.sendButtonDown and SENT_BUTTON_ICON or SEND_BUTTON_ICON,
					Position = UDim2.new(0, sendButtonLeftPadding, 0.5, 0),
					Size = UDim2.new(0, sendButtonIconSize, 0, sendButtonIconSize),
				}),
			}),
		})
	})
end

function SharedGameItem:didMount()
	local function resizeGameName()
		self.gameNameTextLabel.Text = Text.Truncate(self.props.game.name, self.props.textFont,
				self.gameNameTextLabel.TextSize, self.gameNameTextLabel.AbsoluteSize.X, "...")
	end

	local function resizeGameCreator()
		self.gameCreatorTextLabel.Text = Text.Truncate(self.creatorName, self.props.textFont,
				self.gameCreatorTextLabel.TextSize, self.gameCreatorTextLabel.AbsoluteSize.X, "...")
	end

	resizeGameName()
	resizeGameCreator()

	self.connections = {}
	table.insert(self.connections, self.gameNameTextLabel:GetPropertyChangedSignal("Text"):Connect(resizeGameName))
	table.insert(self.connections, self.gameNameTextLabel:GetPropertyChangedSignal("AbsoluteSize"):Connect(resizeGameName))
	table.insert(self.connections, self.gameCreatorTextLabel:GetPropertyChangedSignal("Text"):Connect(resizeGameCreator))
	table.insert(
		self.connections,
		self.gameCreatorTextLabel:GetPropertyChangedSignal("AbsoluteSize"):Connect(resizeGameCreator)
	)
end

function SharedGameItem:willUnmount()
	for _, connection in pairs(self.connections) do
		connection:Disconnect()
	end

	self:eventDisconnect()
end

function SharedGameItem:eventDisconnect()
	if self.userInputServiceCon then
		self.userInputServiceCon:Disconnect()
		self.userInputServiceCon = nil
	end
end

SharedGameItem = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			activeConversationId = state.ChatAppReducer.ActiveConversationId,
			gameThumbnails = state.GameThumbnails,
			isSharing = state.ChatAppReducer.ShareGameToChatAsync.sharingGame,
		}
	end,
	function(dispatch)
		return {
			shareGameToChat = function(activeConversationId, analytics, placeId, url)
				analytics.reportShareGameToChatFromChat(activeConversationId, tostring(placeId))
				return dispatch(ConversationActions.ShareGame(activeConversationId, url))
			end,
		}
	end
)(SharedGameItem)

SharedGameItem = RoactServices.connect({
	analytics = RoactAnalyticsSharedGameItem,
})(SharedGameItem)

return SharedGameItem