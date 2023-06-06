--
-- ChatGameCard
--
-- This is a game that is shown (and possibly pinned) at the top of a chat
-- conversation.
--

local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local Constants = require(LuaApp.Constants)
local ContextualMenu = require(LuaApp.Components.ContextualMenu)
local FriendCarousel = require(LuaChat.Components.FriendCarousel)
local GetMultiplePlaceInfos = require(LuaChat.Actions.GetMultiplePlaceInfos)
local GetPlaceThumbnail = require(LuaChat.Actions.GetPlaceThumbnail)
local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local RoactAnalyticsGameCardLoaded = require(LuaChat.Services.RoactAnalyticsGameCardLoaded)
local RoactServices = require(LuaApp.RoactServices)

local ChatGameCard = Roact.PureComponent:extend("ChatGameCard")

local ICON_SIZE_SMALL = 36
local ICON_SIZE_LARGE = 60
local ICON_SIZE_SMALL_AMENDED = 48

local CARD_MARGINS = 12
local CARD_HEIGHT_SMALL = ICON_SIZE_SMALL + (CARD_MARGINS * 2)
local CARD_HEIGHT_LARGE = ICON_SIZE_LARGE + (CARD_MARGINS * 2)

local GAME_TEXT_COLOR = Constants.Color.GRAY1
local GAME_TEXT_FONT = Enum.Font.SourceSans
local GAME_TEXT_HEIGHT = 25
local GAME_TEXT_HEIGHT_WITH_SUBTITLE = 20
local GAME_TEXT_SIZE = 23
local GAME_TEXT_SIZE_WITH_SUBTITLE = 20

local SUBTITLE_TEXT_SIZE = 18
local SUBTITLE_TEXT_COLOR = Constants.Color.GRAY2

local CAROUSEL_SMALL_ICON_SIZE = 24
local CAROUSEL_LARGE_ICON_SIZE = 32
local CAROUSEL_SMALL_GAP = 3
local CAROUSEL_LARGE_GAP = 9
local CAROUSEL_SMALL_DOT_SIZE = 8
local CAROUSEL_LARGE_DOT_SIZE = 10

local ACTION_BUTTON_WIDTH = 60
local ACTION_BUTTON_HEIGHT = 32
local ACTION_COLOR_PLAY = Constants.Color.GREEN_PRIMARY
local ACTION_COLOR_TEXT = Constants.Color.WHITE

local DEBUG_OUTLINE = 0
local DEBUG_TRANSPARENCY = 1

local DEFAULT_GAME_ICON = "rbxasset://textures/ui/LuaApp/icons/ic-game.png"
local FADEOUT_MASK_IMAGE = "rbxasset://textures/ui/LuaChat/graphic/friendmask.png"
local FADEOUT_MASK_WIDTH = 10
local GAME_MASK_IMAGE = "rbxasset://textures/ui/LuaChat/9-slice/gr-mask-game-icon.png"
local ROUNDED_BUTTON = "rbxasset://textures/ui/LuaChat/9-slice/input-default.png"

-- Set up some default state for this control:
function ChatGameCard:init()
	self.state = {
		isMenuOpen = false,
	}

	-- Localize strings. Needs to be done in context because of the way the localization object is being passed to us:
	local localization = self.props.Localization
	self.MenuInfoPlayGame = {
		displayIcon = "rbxasset://textures/ui/LuaApp/icons/ic-games.png",
		name = "PlayGameButton",
		displayName = localization:Format("Feature.Chat.Drawer.PlayGame"),
	}
	self.MenuInfoPinGame = {
		displayIcon = "rbxasset://textures/ui/LuaChat/icons/ic-pin.png",
		name = "PinGameButton",
		displayName = localization:Format("Feature.Chat.Drawer.PinGame")
	}
	self.MenuInfoUnpinGame = {
		displayIcon = "rbxasset://textures/ui/LuaChat/icons/ic-unpin-20x20.png",
		name = "UnpinGameButton",
		displayName = localization:Format("Feature.Chat.Drawer.UnpinGame")
	}
	self.MenuItemInfoViewGameDetail = {
		displayIcon = "rbxasset://textures/ui/LuaChat/icons/ic-viewdetails-20x20.png",
		name = "ViewDetailsButton",
		displayName = localization:Format("Feature.Chat.Drawer.ViewDetails"),
	}
end

function ChatGameCard:render()
	-- Information about the game is passed in as properties. Action to take
	-- *on* the game should also be passed in, so we have containment and this
	-- module only knows the miniumum necessary.

	local parentLayoutOrder = self.props.LayoutOrder

	-- Visual properties of this game card:
	local isPinnedGame = self.props.isPinnedGame or false
	local isRecommendedGame = self.props.isRecommended or false

	local game = self.props.game
	local getPlaceInfo = self.props.getPlaceInfo
	local getPlaceThumbnail = self.props.getPlaceThumbnail
	local localization = self.props.Localization
	local onGamePin = self.props.onGamePin
	local onGameStart = self.props.onGameStart
	local onGameUnpin = self.props.onGameUnpin
	local onViewDetails = self.props.onViewDetails
	local placeInfos = self.props.placeInfos
	local placeThumbnails = self.props.placeThumbnails or {}
	local renderWidth = self.props.renderWidth or 0

	-- Unpack from our properties:
	local gameFriends = game.friends or {}
	local placeId = game.placeId

	-- Read or retrieve information about our place:
	local placeInfo = placeInfos[placeId]
	local gameName
	local imageToken = nil
	local universeId = nil
	local isPlayable = false
	if (placeInfo == nil) then
		getPlaceInfo(placeId)
		gameName = "(" .. localization:Format("Feature.Chat.Drawer.Loading") .. ")"
	else
		gameName = placeInfo.name
		imageToken = placeInfo.imageToken
		universeId = placeInfo.universeId
		isPlayable = placeInfo.isPlayable
	end

	-- Configure some dimensions based on properties, the GameInfo section in
	-- particular changes for a large (pinned) vs regular size card:
	local cardHeight = CARD_HEIGHT_SMALL
	local carouselItemDotSize = CAROUSEL_SMALL_DOT_SIZE
	local carouselItemGap = CAROUSEL_SMALL_GAP
	local carouselItemHeight = CAROUSEL_SMALL_ICON_SIZE
	local friendAlignment = Enum.HorizontalAlignment.Right
	local gameIconHeight = ICON_SIZE_SMALL
	local gameIconWidth = gameIconHeight
	local gameTextHeight = GAME_TEXT_HEIGHT
	local gameTextSize = GAME_TEXT_SIZE
	local infoFillDirection = Enum.FillDirection.Horizontal
	local subtitle = ""
	local subtitleVisibility = false

	-- If we don't have an action button, zero the reserved width:
	local buttonWidth = ACTION_BUTTON_WIDTH
	if not isPlayable then
		buttonWidth = 0
	end

	-- Scaling of elements:
	local friendsWidthOffset = 0
	local friendsWidthScale = 1
	local textWidthOffset = 0
	local textWidthScale = 1

	if isPinnedGame then
		cardHeight = CARD_HEIGHT_LARGE
		carouselItemDotSize = CAROUSEL_LARGE_DOT_SIZE
		carouselItemGap = CAROUSEL_LARGE_GAP
		carouselItemHeight = CAROUSEL_LARGE_ICON_SIZE
		friendAlignment = Enum.HorizontalAlignment.Left
		gameIconHeight = ICON_SIZE_LARGE
		gameIconWidth = gameIconHeight
		infoFillDirection = Enum.FillDirection.Vertical
	elseif isRecommendedGame then
		carouselItemHeight = 0
		gameTextHeight = GAME_TEXT_HEIGHT_WITH_SUBTITLE
		gameTextSize = GAME_TEXT_SIZE_WITH_SUBTITLE
		infoFillDirection = Enum.FillDirection.Vertical
		subtitle = localization:Format("Feature.Chat.Drawer.Recommended")
		subtitleVisibility = true
	else
		friendsWidthScale = 0.5
		friendsWidthOffset = 0
		textWidthScale = 0.5
		textWidthOffset = 0
	end

	-- This is how much space we have in the center of the card:
	local centerNegativeSpace = CARD_MARGINS + gameIconWidth + CARD_MARGINS + CARD_MARGINS
	local countFriends = #gameFriends

	-- Default is Play if nobody else is in the game, Join if we have friends:
	local actionText
	if isPlayable then
		centerNegativeSpace = centerNegativeSpace + buttonWidth + CARD_MARGINS
		local actionTextKey = "Feature.Chat.Drawer.Play"
		if countFriends > 0 then
			actionTextKey = "Feature.Chat.Drawer.Join"
		end
		actionText = localization:Format(actionTextKey)
	end
	local actionColor = ACTION_COLOR_PLAY
	local actionTextColor = ACTION_COLOR_TEXT

	-- ...and as a last metrics step, adjust the ratio of the game name and friend carousel:
	if not (isPinnedGame or isRecommendedGame) then
		local actualSpace = renderWidth - centerNegativeSpace
		if actualSpace > 0 then
			local friendSpace = carouselItemHeight * countFriends
			local textAdjust = (actualSpace * 0.5) - (friendSpace + CARD_MARGINS)
			if textAdjust > 0 then
				textWidthOffset = textWidthOffset + textAdjust
				friendsWidthOffset = friendsWidthOffset - textAdjust
			end
		end
	end

	-- Obtain the thumbnail for this game:
	local gameIcon = DEFAULT_GAME_ICON
	if placeInfo then
		local thumbnail = placeThumbnails[imageToken]
		if thumbnail == nil then
			if imageToken and imageToken ~= "" then
				if gameIconWidth == ICON_SIZE_SMALL then
					getPlaceThumbnail(imageToken, ICON_SIZE_SMALL_AMENDED, ICON_SIZE_SMALL_AMENDED)
				else
					getPlaceThumbnail(imageToken, gameIconWidth, gameIconHeight)
				end
			end
		elseif thumbnail.image ~= "" then
			gameIcon = thumbnail.image
		end
	end

	-- Build up a horizontal list of items for our card:
	local cardItems = {}
	cardItems["Layout"] = Roact.createElement("UIListLayout", {
		FillDirection = Enum.FillDirection.Horizontal,
		HorizontalAlignment = Enum.HorizontalAlignment.Center,
		SortOrder = Enum.SortOrder.LayoutOrder,
		VerticalAlignment = Enum.VerticalAlignment.Center,
		Padding = UDim.new(0, CARD_MARGINS)
	})

	-- Game icon:
	local layoutOrder = 1
	cardItems["GameIcon"] = Roact.createElement("ImageLabel", {
		BackgroundTransparency = DEBUG_TRANSPARENCY,
		BorderSizePixel = DEBUG_OUTLINE,
		LayoutOrder = layoutOrder,
		Size = UDim2.new(0, gameIconHeight, 0, gameIconHeight),
		Image = gameIcon,
	}, {
		Mask = Roact.createElement("ImageLabel", {
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Image = GAME_MASK_IMAGE,
			ImageColor3 = Constants.Color.WHITE,
			ScaleType = Enum.ScaleType.Slice,
			Size = UDim2.new(1, 0, 1, 0),
			SliceCenter = Rect.new(3,3,4,4),
		}),
	})
	layoutOrder = layoutOrder + 1

	cardItems["GameInfo"] = Roact.createElement("Frame", {
		BackgroundTransparency = DEBUG_TRANSPARENCY,
		BorderSizePixel = DEBUG_OUTLINE,
		ClipsDescendants = true,
		LayoutOrder = layoutOrder,
		Size = UDim2.new(1, -centerNegativeSpace, 1, 0),
	}, {
		Layout = Roact.createElement("UIListLayout", {
			FillDirection = infoFillDirection,
			HorizontalAlignment = Enum.HorizontalAlignment.Left,
			SortOrder = Enum.SortOrder.LayoutOrder,
			VerticalAlignment = Enum.VerticalAlignment.Center,
		}),

		GameName = Roact.createElement("TextLabel", {
			BackgroundTransparency = DEBUG_TRANSPARENCY,
			BorderSizePixel = DEBUG_OUTLINE,
			ClipsDescendants = true,
			Font = GAME_TEXT_FONT,
			LayoutOrder = 1,
			Size = UDim2.new(textWidthScale, textWidthOffset, 0, gameTextHeight),
			Text = gameName,
			TextColor3 = GAME_TEXT_COLOR,
			TextSize = gameTextSize,
			TextXAlignment = Enum.TextXAlignment.Left,
			TextYAlignment = Enum.TextYAlignment.Top
		},{
			MaskRight = Roact.createElement("ImageLabel", {
				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				Image = FADEOUT_MASK_IMAGE,
				Position = UDim2.new(1, -FADEOUT_MASK_WIDTH, 0, 0),
				Size = UDim2.new(0, FADEOUT_MASK_WIDTH, 1, 0),
				ZIndex = 2,
			}),
		}),

		Subtitle = Roact.createElement("TextLabel", {
			BackgroundTransparency = DEBUG_TRANSPARENCY,
			BorderSizePixel = DEBUG_OUTLINE,
			ClipsDescendants = true,
			Font = GAME_TEXT_FONT,
			LayoutOrder = 1,
			Size = UDim2.new(textWidthScale, textWidthOffset, 0, ICON_SIZE_SMALL - gameTextHeight),
			Text = subtitle,
			TextColor3 = SUBTITLE_TEXT_COLOR,
			TextSize = SUBTITLE_TEXT_SIZE,
			TextXAlignment = Enum.TextXAlignment.Left,
			Visible = subtitleVisibility,
		}),

		GameFriends = Roact.createElement(FriendCarousel, {
			dotSize = carouselItemDotSize,
			friends = gameFriends,
			HorizontalAlignment = friendAlignment,
			itemGap = carouselItemGap,
			itemSize = carouselItemHeight,
			LayoutOrder = 2,
			Size = UDim2.new(friendsWidthScale, friendsWidthOffset, 0, carouselItemHeight),
		}),
	})
	layoutOrder = layoutOrder + 1

	if isPlayable then
		cardItems["ActionButton"] = Roact.createElement("ImageButton", {
			AutoButtonColor = false,
			BackgroundTransparency = 1,
			BorderSizePixel = DEBUG_OUTLINE,
			Image = ROUNDED_BUTTON,
			ImageColor3 = actionColor,
			LayoutOrder = layoutOrder,
			ScaleType = Enum.ScaleType.Slice,
			Size = UDim2.new(0, ACTION_BUTTON_WIDTH, 0, ACTION_BUTTON_HEIGHT),
			SliceCenter = Rect.new(3,3,4,4),

			[Roact.Event.Activated] = function(rbx)
				onGameStart()
			end
		},{
			ActionLabel = Roact.createElement("TextLabel", {
				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				Font = GAME_TEXT_FONT,
				LayoutOrder = layoutOrder,
				Size = UDim2.new(1, 0, 1, 0),
				Text = actionText,
				TextColor3 = actionTextColor,
				TextSize = GAME_TEXT_SIZE,
			}),
		})
	end

	if self.state.isMenuOpen then
		local menuItems
		if isPinnedGame then
			menuItems = { self.MenuInfoUnpinGame }
		else
			menuItems = { self.MenuInfoPinGame }
		end

		if isPlayable then
			table.insert(menuItems, 1, self.MenuInfoPlayGame)
		end
		table.insert(menuItems, self.MenuItemInfoViewGameDetail)

		local callbackCancel = function()
			self:setState({ isMenuOpen = false })
		end

		local callbackSelect = function(item)
			if item.name == self.MenuInfoPlayGame.name then
				onGameStart()
			elseif item.name == self.MenuInfoPinGame.name then
				onGamePin(universeId)
			elseif item.name == self.MenuInfoUnpinGame.name then
				onGameUnpin()
			elseif item.name == self.MenuItemInfoViewGameDetail.name then
				onViewDetails()
			end
			callbackCancel()
		end

		cardItems["ContextMenu"] = Roact.createElement(ContextualMenu, {
			callbackCancel = callbackCancel,
			callbackSelect = callbackSelect,
			menuItems = menuItems,
			screenShape = self.state.screenShape,
		})
	end

	-- Put a clickable wrapper around the entire card:
	return Roact.createElement("TextButton", {
		AutoButtonColor = false,
		BackgroundTransparency = DEBUG_TRANSPARENCY,
		BorderSizePixel = DEBUG_OUTLINE,
		LayoutOrder = parentLayoutOrder,
		Size = UDim2.new(1, 0, 0, cardHeight),
		Text = "",
		[Roact.Event.Activated] = function(rbx)
			-- TODO: Move this screen size functionality into a helper component
			-- so that it doesn't get repeated everywhere (see: MOBLUAPP-241).

			-- We need to know the size of the screen, so we can position the
			-- popout component appropriately. So we climb up the object
			-- heirachy until we find the current ScreenGui:
			local screenWidth = 0
			local screenHeight = 0
			local screenGui = rbx:FindFirstAncestorOfClass("ScreenGui")
			if screenGui ~= nil then
				screenWidth = screenGui.AbsoluteSize.X
				screenHeight = screenGui.AbsoluteSize.Y
			end

			self:setState({
				isMenuOpen = true,
				screenShape = {
					x = rbx.AbsolutePosition.X,
					y = rbx.AbsolutePosition.Y,
					width = rbx.AbsoluteSize.X,
					height = rbx.AbsoluteSize.Y,
					parentWidth = screenWidth,
					parentHeight = screenHeight,
				},
			})
		end,

	}, cardItems)
end

function ChatGameCard:didMount()
	-- TODO: tkim has a fix for this in progress, but it's incomplete.
	-- This code needs to be removed for now.
	-- See: https://jira.roblox.com/browse/SOC-2232
	-- local conversationId = tostring(self.props.conversationId)
	-- local placeId = tostring(self.props.game.placeId)
	-- self.props.analytics.reportGameCardLoadedInLuaChat(conversationId, placeId)
end

ChatGameCard = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			placeInfos = state.ChatAppReducer.PlaceInfos,
			placeThumbnails = state.ChatAppReducer.PlaceThumbnails,
		}
	end,
	function(dispatch)
		return {
			getPlaceInfo = function(placeId)
				dispatch(GetMultiplePlaceInfos({placeId}))
			end,
			getPlaceThumbnail = function(imageToken, iconWidth, iconHeight)
				dispatch(GetPlaceThumbnail(imageToken, iconWidth, iconHeight))
			end,
		}
	end
)(ChatGameCard)

ChatGameCard = RoactServices.connect({
	analytics = RoactAnalyticsGameCardLoaded,
})(ChatGameCard)

return ChatGameCard