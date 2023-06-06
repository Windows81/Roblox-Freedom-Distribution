local CoreGui = game:GetService("CoreGui")
local Players = game:GetService("Players")
local GuiService = game:GetService("GuiService")
local TweenService = game:GetService("TweenService")
local HttpService = game:GetService("HttpService")
local UserInputService = game:GetService("UserInputService")

local Modules = CoreGui.RobloxGui.Modules
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local Constants = require(LuaChat.Constants)
local Create = require(LuaChat.Create)
local FlagSettings = require(LuaChat.FlagSettings)
local GameParams = require(LuaChat.Models.GameParams)
local getInputEvent = require(LuaChat.Utils.getInputEvent)
local GetMultiplePlaceInfos = require(LuaChat.Actions.GetMultiplePlaceInfos)
local GetPlaceThumbnail = require(LuaChat.Actions.GetPlaceThumbnail)
local LoadingIndicator = require(LuaChat.Components.LoadingIndicator)
local NotificationType = require(LuaApp.Enum.NotificationType)
local PlayTogetherActions =  require(LuaChat.Actions.PlayTogetherActions)
local Text = require(LuaChat.Text)

local UseCppTextTruncation = FlagSettings.UseCppTextTruncation()

local BUBBLE_PADDING = 10
local DEFAULT_THUMBNAIL = "rbxasset://textures/ui/LuaChat/icons/share-game-thumbnail.png"
local EXTERIOR_PADDING = 3
local GAME_CARD_BUTTON_CLICKED_EVENT = "clickBtnFromLinkCardInChat"
local GAME_MASK_IMAGE = "rbxasset://textures/ui/LuaChat/9-slice/gr-mask-game-icon.png"
local GAME_PLAY_INTENT = "gamePlayIntent"
local GAME_PLAY_EVENT_CONTEXT = "PlayGameFromLinkCard"
local ICON_SIZE = 64
local INTERIOR_PADDING = 12
local LINK_CARD_CLICKED_EVENT = "clickLinkCardInChat"
local PIN_ICON = "rbxasset://textures/ui/LuaChat/icons/ic-pin.png"
local PIN_ICON_HORIZONTAL_PADDING = 10
local PIN_ICON_SIZE = 20
local PIN_ICON_VERTICAL_PADDING = 8
local PIN_PRESSED_ICON = "rbxasset://textures/ui/LuaChat/icons/ic-pinpressed.png"
local PLACE_INFO_THUMBNAIL_SIZE = 50
local TOUCH_CONTEXT = "touch"

local function isOutgoingMessage(message)
	local localUserId = tostring(Players.LocalPlayer.UserId)
	return message.senderTargetId == localUserId
end

local UrlSupportNewGamesAPI = settings():GetFFlag("UrlSupportNewGamesAPI")
local LuaChatAssetCardsSelfTerminateConnection = settings():GetFFlag("LuaChatAssetCardsSelfTerminateConnection")

local AssetCard = {}
AssetCard.__index = AssetCard

function AssetCard.new(appState, message, assetId)
	local self = {}
	setmetatable(self, AssetCard)

	local state = appState.store:getState()
	local user = state.Users[message.senderTargetId]
	local username = user and user.name or "unknown user"

	self._analytics = appState.analytics
	self.appState = appState
	self.paddingObject = nil
	self.message = message
	self.bubbleType = "AssetCard"
	self.connections = {}
	self.cardBodyClick = nil
	self.assetId = assetId
	self.conversationId = message.conversationId
	self.universeId = nil
	self.pinButtonClick = nil

	self.luaChatPlayTogetherEnabled = FlagSettings.IsLuaChatPlayTogetherEnabled(
		self.appState.store:getState().FormFactor)

	self.tail = Create.new "ImageLabel" {
		Name = "Tail",
		Size = UDim2.new(0, 6, 0, 6),
		BackgroundTransparency = 1,
	}

	self.actionLabel = Create.new "TextLabel" {
		Name = "ActionLabel",
		BackgroundTransparency = 1,

		AnchorPoint = Vector2.new(0.5, 0.5),
		Size = UDim2.new(0.8, 0, 0.8, 0),
		Position = UDim2.new(0.5, 0, 0.5, 0),
		TextSize = Constants.Font.FONT_SIZE_20,
		TextColor3 = Constants.Color.GRAY1,
		Font = Enum.Font.SourceSans,
		Text = self.appState.localization:Format("Feature.Chat.Action.ViewAssetDetails"),
	}

	self.actionButton = Create.new "ImageButton" {
		Name = "Action",
		BackgroundTransparency = 1,
		AnchorPoint = Vector2.new(0.5, 1),
		Position = UDim2.new(0.5, 0, 1, 0),
		Size = UDim2.new(1, 0, 0, 32),
		ScaleType = Enum.ScaleType.Slice,
		SliceCenter = Rect.new(3,3,4,4),
		Image = "rbxasset://textures/ui/LuaChat/9-slice/input-default.png",
		self.actionLabel,
	}

	local textLabelWidth
	if self.luaChatPlayTogetherEnabled then
		textLabelWidth = -(PIN_ICON_SIZE + (2 * INTERIOR_PADDING) + BUBBLE_PADDING)
	else
		textLabelWidth = -(INTERIOR_PADDING + BUBBLE_PADDING)
	end
	self.Title = Create.new "TextLabel" {
		Name = "Title",
		TextTruncate = UseCppTextTruncation and Enum.TextTruncate.AtEnd or nil,
		BackgroundTransparency = 1,

		AnchorPoint = Vector2.new(0, 0),
		TextSize = Constants.Font.FONT_SIZE_20,
		Size = UDim2.new(1, textLabelWidth, 0, 20),
		Position = UDim2.new(0, 0, 0, 0),

		TextColor3 = Constants.Color.GRAY1,
		Font = Enum.Font.SourceSans,
		TextXAlignment = Enum.TextXAlignment.Left
	}

	self.Icon = Create.new "ImageLabel" {
		Name = "Icon",
		BackgroundTransparency = 1,
		Position = UDim2.new(0, 0, 0, self.Title.TextSize + INTERIOR_PADDING),
		Size = UDim2.new(0, ICON_SIZE, 0, ICON_SIZE),

		Create.new "ImageLabel" {
			Name = "Mask",
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Image = GAME_MASK_IMAGE,
			ImageColor3 = Constants.Color.WHITE,
			ScaleType = Enum.ScaleType.Slice,
			Size = UDim2.new(1, 0, 1, 0),
			SliceCenter = Rect.new(3,3,4,4),
		}
	}

	self.Details = Create.new "TextLabel" {
		Name = "Details",
		BackgroundTransparency = 1,
		Size = UDim2.new(1, - INTERIOR_PADDING -ICON_SIZE, 0, ICON_SIZE),
		Position = self.Icon.Position + UDim2.new(0 , INTERIOR_PADDING + ICON_SIZE, 0, 0),

		TextColor3 = Constants.Color.GRAY2,
		Font = Enum.Font.SourceSans,
		TextSize = Constants.Font.FONT_SIZE_14,
		TextXAlignment = Enum.TextXAlignment.Left,
		TextYAlignment = Enum.TextYAlignment.Top,
		TextWrapped = true,
	}

	self.fadeScreen = Create.new "Frame" {
		Name = "FadeScreen",
		BackgroundTransparency = 0,
		Size = UDim2.new(1, 0, 1, 0),
		BackgroundColor3 = Color3.new(1, 1, 1),
		BorderSizePixel = 0,
	}


	self.Content = Create.new "ImageButton" {
		Name = "Content",
		BackgroundTransparency = 1,
		Size = UDim2.new(1, -BUBBLE_PADDING * 2, 1, -BUBBLE_PADDING * 2),
		AnchorPoint = Vector2.new(0.5, 0.5),
		Position = UDim2.new(0.5, 0, 0.5, 0),
		Visible = false,

		self.actionButton,
		self.Title,
		self.Icon,
		self.Details,
		self.fadeScreen,
	}

	if self.luaChatPlayTogetherEnabled then
		self.PinIcon = Create.new "ImageLabel" {
			Name = "PinIcon",
			BackgroundTransparency = 1,
			AnchorPoint = Vector2.new(0.5, 0.5),
			Position = UDim2.new(0.5, 0, 0.5, 0),
			Size = UDim2.new(0, PIN_ICON_SIZE, 0, PIN_ICON_SIZE),
			Image = PIN_ICON,
		}

		self.PinButton = Create.new "TextButton" {
			Name = "PinButton",
			Text = "",
			BackgroundTransparency = 1,
			AnchorPoint = Vector2.new(1, 0),
			Position = UDim2.new(1, BUBBLE_PADDING, 0, -BUBBLE_PADDING),
			Size = UDim2.new(0, PIN_ICON_SIZE + 2 * PIN_ICON_HORIZONTAL_PADDING,
				0, PIN_ICON_SIZE + 2 * PIN_ICON_VERTICAL_PADDING),

			self.PinIcon
		}
		self.PinButton.Parent = self.Content
	end

	self.bubble = Create.new "ImageLabel" {
		Name = "Bubble",
		BackgroundTransparency = 1,
		AnchorPoint = Vector2.new(1, 0),
		Position = UDim2.new(0, 0, 0, 0),
		Size = UDim2.new(0, 267, 1, 0),
		ScaleType = Enum.ScaleType.Slice,
		SliceCenter = Rect.new(10, 10, 11, 11),
		LayoutOrder = 2,

		self.Content,
		self.tail,
	}

	self.usernameLabel = Create.new "TextLabel" {
		Name = "UsernameLabel",
		Font = Enum.Font.SourceSans,
		TextSize = Constants.Font.FONT_SIZE_12,
		Visible = false,
		BackgroundTransparency = 1,
		Size = UDim2.new(1, -56, 0, 16),
		Position = UDim2.new(0, 56, 0, 0),
		TextColor3 = Constants.Color.GRAY2,
		TextXAlignment = Enum.TextXAlignment.Left,
		TextYAlignment = Enum.TextYAlignment.Top,
		Text = username,
	}

	self.bubbleContainer = Create.new "Frame" {
		Name = "BubbleContainer",
		BackgroundTransparency = 1,
		LayoutOrder = 2,
		Size = UDim2.new(1, 0, 0, 0),

		self.bubble,
		self.usernameLabel,
	}

	self.rbx = Create.new "Frame" {
		Name = "AssetCard",
		BackgroundTransparency = 1,

		Create.new "UIListLayout" {
			SortOrder = Enum.SortOrder.LayoutOrder,
			VerticalAlignment = Enum.VerticalAlignment.Center,
		},

		self.bubbleContainer,
	}

	-- 'isOutgoing' means "is sent by the local user". This function separates the tail position & color
	if isOutgoingMessage(message) then
		self.tail.AnchorPoint = Vector2.new(0, 0)
		self.tail.Position = UDim2.new(1, 0, 0, 0)
		self.tail.ImageColor3 = Color3.new(1, 1, 1)

		self.bubble.ImageColor3 = Color3.new(1, 1, 1)
		self.bubble.AnchorPoint = Vector2.new(1, 0)
		self.bubble.Position = UDim2.new(1, -10, 0, 0)

		self.rbx.UIListLayout.HorizontalAlignment = Enum.HorizontalAlignment.Right
	else
		self.tail.AnchorPoint = Vector2.new(1, 0)
		self.tail.Position = UDim2.new(0, 0, 0, 0)
		self.tail.ImageColor3 = Color3.new(1, 1, 1)

		self.bubble.ImageColor3 = Color3.new(1, 1, 1)
		self.bubble.AnchorPoint = Vector2.new(0, 0)
		self.bubble.Position = UDim2.new(0, 54, 0, 0)

		self.rbx.UIListLayout.HorizontalAlignment = Enum.HorizontalAlignment.Left
	end

	self.appStateConnection = self.appState.store.Changed:Connect(function(state)
		self:Update(state)
	end)
	table.insert(self.connections, self.appStateConnection)

	local connection = self.rbx:GetPropertyChangedSignal("AbsoluteSize"):Connect(function()
		self:Resize()
	end)
	table.insert(self.connections, connection)

	self:Update(state)

	return self
end

function AssetCard:Resize()
	local formFactor = self.appState.store:getState().FormFactor
	local bubbleSizeOffsetY = Constants:GetFormFactorSpecific(formFactor).ASSET_CARD_HORIZONTAL_MARGIN
	self.bubble.Size = UDim2.new(1, -bubbleSizeOffsetY, 0, 92 + ICON_SIZE)

	local containerHeight = self.bubble.AbsoluteSize.Y

	if self.usernameLabel.Visible then
		containerHeight = containerHeight + self.usernameLabel.AbsoluteSize.Y
	end

	self.bubbleContainer.Size = UDim2.new(1, 0, 0, containerHeight)

	local height = 0
	for _, child in ipairs(self.rbx:GetChildren()) do
		if child:IsA("GuiObject") then
			height = height + child.AbsoluteSize.Y
		end
	end

	if not UseCppTextTruncation then
		Text.TruncateTextLabel(self.Title, "...")
	end
	self.rbx.Size = UDim2.new(1, 0, 0, height + EXTERIOR_PADDING*2)
end

function AssetCard:onPinPressed()
	self.PinIcon.Image = PIN_PRESSED_ICON
	self.userInputServiceCon = UserInputService.InputEnded:Connect(function()
		self:onPinRelease()
	end)
end

function AssetCard:onPinRelease()
	if self.userInputServiceCon then
		self.userInputServiceCon:Disconnect()
		self.userInputServiceCon = nil
	end
	self.PinIcon.Image = PIN_ICON
end

function AssetCard:Update(newState)
	local placeInfo = newState.ChatAppReducer.PlaceInfos[self.assetId]
	if placeInfo == nil then
		self:ShowLoadingIndicator(true)
		self.appState.store:dispatch(GetMultiplePlaceInfos({self.assetId}))
	else
		self.placeInfo = placeInfo
		self.Title.Text = placeInfo.name

		local description = placeInfo.description:gsub("%s", " ")
		if description:gsub("^%s+$", "") == "" then
			description = self.appState.localization:Format("Feature.Chat.Label.NoDescriptionYet")
		end
		self.Details.Text = description
		self.universeId = placeInfo.universeId

		if self.luaChatPlayTogetherEnabled then
			if self.pinButtonClick then self.pinButtonClick:Disconnect() end
			if self.pinButtonInputBegin then self.pinButtonInputBegin:Disconnect() end

			self.pinButtonClick = self.PinButton.Activated:Connect(function()
				self.appState.store:dispatch(PlayTogetherActions.PinGame(self.conversationId, self.universeId))
			end)
			self.pinButtonInputBegin = self.PinButton.InputBegan:Connect(function()
				self:onPinPressed()
			end)
		end

		if UrlSupportNewGamesAPI then
			local thumbnail = newState.ChatAppReducer.PlaceThumbnails[placeInfo.imageToken]
			if thumbnail == nil then
				self.appState.store:dispatch(GetPlaceThumbnail(
					placeInfo.imageToken, PLACE_INFO_THUMBNAIL_SIZE, PLACE_INFO_THUMBNAIL_SIZE
				))
			else
				if thumbnail.image == '' then
					self.thumbnail = DEFAULT_THUMBNAIL
				else
					self.thumbnail = thumbnail.image
				end
				self:FillThumbnail()
				self:Show()
			end
		else
			self.thumbnail = DEFAULT_THUMBNAIL
			self:Show()
		end
	end
	if self.cardBodyClick then self.cardBodyClick:Disconnect() end
	if self.detailsButtonClick then self.detailsButtonClick:Disconnect() end

	self:StyleViewDetailsAsPlay(self.placeInfo ~= nil and self.placeInfo.isPlayable)

	self.cardBodyClick = getInputEvent(self.Content):Connect(function()
		self:ReportAnEvent(LINK_CARD_CLICKED_EVENT, TOUCH_CONTEXT)
		if self.placeInfo then
			GuiService:BroadcastNotification(self.assetId,
				NotificationType.VIEW_GAME_DETAILS)
		end
	end)

	self.detailsButtonClick = getInputEvent(self.actionButton):Connect(function()
		self:ReportAnEvent(GAME_CARD_BUTTON_CLICKED_EVENT, TOUCH_CONTEXT)
		if self.placeInfo then
			if self.placeInfo.isPlayable then
				self:ReportAnEvent(GAME_PLAY_INTENT, GAME_PLAY_EVENT_CONTEXT)
				local gameParams = GameParams.fromPlaceId(self.assetId)
				local payload = HttpService:JSONEncode(gameParams)

				GuiService:BroadcastNotification(payload,
					NotificationType.LAUNCH_GAME)
			else
				GuiService:BroadcastNotification(self.assetId,
					NotificationType.VIEW_GAME_DETAILS)
			end
		end
	end)

	self:Resize()
end

function AssetCard:ReportAnEvent(eventName, eventContext)
	local additionalArgs
	if eventName == GAME_PLAY_INTENT then
		additionalArgs = {
			conversationId = self.conversationId,
			rootPlaceId = self.assetId
		}
	else
		additionalArgs = {
			conversationId = self.conversationId,
			placeId = self.assetId
		}
	end

	self._analytics.EventStream:setRBXEventStream(eventContext, eventName, additionalArgs)
end

function AssetCard:StyleViewDetailsAsPlay(isShowingAsPlay)
	if isShowingAsPlay then
		self.actionButton.ImageColor3 = Constants.Color.GREEN_PRIMARY
		self.actionLabel.Text = self.appState.localization:Format("Common.VisitGame.Label.Play")
		self.actionLabel.TextColor3 = Constants.Color.WHITE
	else
		self.actionButton.ImageColor3 = Constants.Color.WHITE
		self.actionLabel.Text = self.appState.localization:Format("Feature.Chat.Action.ViewAssetDetails")
		self.actionLabel.TextColor3 = Constants.Color.GRAY1
	end
end

function AssetCard:Show()
	self.Content.Visible = true
	spawn(function()
		while (not self.Icon.IsLoaded) do wait() end

		self:ShowLoadingIndicator(false)
		local fadeInTween = TweenService:Create(
			self.fadeScreen,
			TweenInfo.new(0.4),
			{BackgroundTransparency = 1}
		)
		fadeInTween:Play()
	end)

	if LuaChatAssetCardsSelfTerminateConnection then
		if self.appStateConnection then
			self.appStateConnection:Disconnect()
		end
	end
end

function AssetCard:FillThumbnail()
	self.Icon.Image = self.thumbnail or ""
end

function AssetCard:ShowLoadingIndicator(isVisible)
	if isVisible then
		if not self.loadingIndicator then
			local loadingIndicator = LoadingIndicator.new(self.appState)
			loadingIndicator.rbx.AnchorPoint = Vector2.new(0.5, 0.5)
			loadingIndicator.rbx.Position = UDim2.new(0.5, 0, 0.5, 0)
			loadingIndicator.rbx.Size = UDim2.new(0.5, 0, 0.25, 0)
			loadingIndicator.rbx.Parent = self.bubble
			loadingIndicator:SetVisible(true)
			self.loadingIndicator = loadingIndicator
		end
	else
		if self.loadingIndicator then
			self.loadingIndicator:Destroy()
		end
	end
end

if not LuaChatAssetCardsSelfTerminateConnection then
	function AssetCard:DisconnectUpdate()
		if self.Content.Visible then
			if self.appStateConnection then
				self.appStateConnection:Disconnect()
				self.appStateConnection = nil
			end
		end
	end
end

function AssetCard:Destruct()
	for _, connection in pairs(self.connections) do
		connection:Disconnect()
	end
	self.connections = {}
	if self.pinButtonClick then self.pinButtonClick:Disconnect() end
	if self.pinButtonInputBegin then self.pinButtonInputBegin:Disconnect() end
	self.rbx:Destroy()
end

return AssetCard
