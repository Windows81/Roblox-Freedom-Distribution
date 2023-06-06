--
-- ChatGameDrawer
--
-- Contains ChatGameCard objects that represent pinned or in progress games.
-- This lives at the top of a conversation window.
--

local CoreGui = game:GetService("CoreGui")
local GuiService = game:GetService("GuiService")
local HttpService = game:GetService("HttpService")

local Modules = CoreGui.RobloxGui.Modules

local Common = Modules.Common
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local Analytics = require(Common.Analytics)
local ChatGameCard = require(LuaChat.Components.ChatGameCard)
local Constants = require(LuaApp.Constants)
local GameParams = require(LuaChat.Models.GameParams)
local PlayTogetherActions = require(LuaChat.Actions.PlayTogetherActions)
local Roact = require(Common.Roact)
local RoactRodux = require(Common.RoactRodux)
local SortedActivelyPlayedGames = require(LuaChat.SortedActivelyPlayedGames)
local User = require(LuaApp.Models.User)

local ChatGameDrawer = Roact.PureComponent:extend("ChatGameDrawer")

local urlSupportNewGamesAPI = settings():GetFFlag("UrlSupportNewGamesAPI")

-- Drawer properties:
local DRAWER_BACKGROUND_COLOR = Constants.Color.WHITE
local BORDER_SIZE = 12
local DRAWER_SHADOW_IMAGE = "rbxasset://textures/ui/LuaChat/graphic/gr-overlay-shadow.png"
local DRAWER_SHADOW_HEIGHT = 5

-- Pointer up to the image:
local ICON_POINTER_HEIGHT = 6
local ICON_POINTER_WIDTH = 12
local ICON_POINTER_UP = "rbxasset://textures/ui/LuaApp/dropdown/gr-tip-up.png"
local ICON_POINTER_FROMEDGE = 20

-- "Pinned Game" text properties:
local PINNED_ICON = "rbxasset://textures/ui/LuaChat/icons/ic-pin.png"
local PINNED_ICON_SIZE = 12
local PINNED_SPACER = 6

local PINNED_TEXT_COLOR = Constants.Color.GRAY2
local PINNED_TEXT_FONT = Enum.Font.SourceSans
local PINNED_TEXT_SIZE = 15

local PINNED_DIVIDER_COLOR = Constants.Color.GRAY4
local PINNED_BOTTOM_BORDER = Constants.Color.GRAY4
local PINNED_BOTTOM_BACKGROUND = Constants.Color.GRAY6

local SMALL_DIVIDER_OFFSET = 60
local CARD_HEIGHT_SMALL = 60
local CARD_HEIGHT_LARGE = 84

local MORE_TEXT_SIZE = 18
local MORE_TEXT_PADDING = 9
local MORE_TEXT_COLOR = Constants.Color.GRAY1

-- Set up some default state for this control:
function ChatGameDrawer:init()
	self._analytics = Analytics.new()
	self.state = {
		isExpanded = false,
		pointerPosition = UDim2.new(1, -ICON_POINTER_FROMEDGE, 0, 0),
		pointerSet = false,
		renderWidth = 0,
	}

	self.isGameDrawerSized = false
end

function ChatGameDrawer:UnpinGame()
	local playTogetherUnpinGame = self.props.playTogetherUnpinGame
	playTogetherUnpinGame(self.props.conversationId)
end

-- Games are pinned by universeId (but they're accessed using placeId elsewhere):
function ChatGameDrawer:PinGame(universeId)
	local playTogetherPinGame = self.props.playTogetherPinGame
	playTogetherPinGame(self.props.conversationId, universeId)
end

function ChatGameDrawer:ViewGameDetails(placeId)
	GuiService:BroadcastNotification(placeId, GuiService:GetNotificationTypeList().VIEW_GAME_DETAILS_ANIMATED)
end

function ChatGameDrawer:GameStart(placeId)
	-- Report player join game via play together
	self:ReportPlayerJoinInAGame(placeId)
	-- Start a game here.
	local gameParams = GameParams.fromPlaceId(placeId)
	local payload = HttpService:JSONEncode(gameParams)
	GuiService:BroadcastNotification(payload, GuiService:GetNotificationTypeList().LAUNCH_GAME)
end

function ChatGameDrawer:GetGamesFromConversation(conversationId)
	local conversations = self.props.conversations
	local mostRecentlyPlayedGames = self.props.mostRecentlyPlayedGames
	local users = self.props.users

	-- Don't know if this is necessary:
	if not urlSupportNewGamesAPI then
		error("Server doesn't support new games API.")
		return { countFriendsInGames = 0, games = {}, }
	end

	-- Early out if we have no conversation:
	if conversationId == nil or conversationId == "nil" then
		return { countFriendsInGames = 0, games = {}, }
	end

	-- Find the specific conversation we're interested in:
	if not conversations then
		return { countFriendsInGames = 0, games = {}, }
	end

	local conversation = conversations[conversationId]
	if not conversation then
		warn("ChatGameDrawer - Can't find conversation, id:" .. conversationId .. " t:" .. type(conversationId))
		return { countFriendsInGames = 0, games = {}, }
	end

	local pinnedGameRootPlaceId = conversation.pinnedGame.rootPlaceId
	local inGameParticipants = {}
	local mostRecentPlayedPlayableGamePlaceId = mostRecentlyPlayedGames.playableGamePlaceId

	for _, userId in pairs(conversation.participants) do
		local user = users[userId]
		if user ~= nil then
			if (user.presence == User.PresenceType.IN_GAME) and user.placeId then
				table.insert(inGameParticipants, user)
			end
		end
	end

	local countFriendsInGames = #inGameParticipants
	if countFriendsInGames > 0 then
		return {
			countFriendsInGames = countFriendsInGames,
			games = SortedActivelyPlayedGames.getSortedGamesPlusEmptyPinned(pinnedGameRootPlaceId, inGameParticipants),
		}
	end

	if pinnedGameRootPlaceId then
		return {
			countFriendsInGames = 0,
			games = {
				{
					friends = {},
					pinned = true,
					placeId = pinnedGameRootPlaceId,
					recommended = false,
				}
			}
		}
	end

	if mostRecentPlayedPlayableGamePlaceId then
		return {
			countFriendsInGames = 0,
			games = {
				{
					friends = {},
					pinned = false,
					placeId = mostRecentPlayedPlayableGamePlaceId,
					recommended = true,
				}
			}
		}
	end

	return {
		countFriendsInGames = 0,
		games = {}
	}
end

function ChatGameDrawer:ReportPlayerJoinInAGame(placeId)
	local conversationId = self.props.conversationId
	local eventContext = "touch"
	local eventName = "playTogether"

	local PlayerService = game:GetService("Players")
	local player = PlayerService.LocalPlayer
	local userId = "UNKNOWN"
	if player then
		userId = tostring(player.UserId)
	end

	local additionalArgs = {
		uid = userId,
		cid = conversationId,
		placeId = placeId
	}
	self._analytics.EventStream:setRBXEventStream(eventContext, eventName, additionalArgs)
end

function ChatGameDrawer:render()
	local anchorPoint = self.props.AnchorPoint
	local conversationId = self.props.conversationId
	local localization = self.props.Localization
	local onSize = self.props.onSize
	local parentLayoutOrder = self.props.layoutOrder
	local position = self.props.Position

	local isExpanded = self.state.isExpanded
	local pointerPosition = self.state.pointerPosition or UDim2.new(1, -ICON_POINTER_FROMEDGE, 0, 0)
	local pointerSet = self.state.pointerSet
	local pointerTransparency = 1
	if pointerSet then
		pointerTransparency = 0
	end

	local gameInfo = self:GetGamesFromConversation(conversationId)
	local countGames = #gameInfo.games

	-- Early exit if we have nothing to display in the drawer:
	if countGames == 0 then
		spawn(function()
			onSize(0, false)
		end)
		return nil
	end

	local hasFriendsActive = gameInfo.countFriendsInGames > 0

	-- If we have active friends and this is the first time rendering, expand:
	if hasFriendsActive and not self.isGameDrawerSized then
		self.isGameDrawerSized = true
		if not isExpanded then
			spawn(function()
				self:setState({ isExpanded = true })
			end)
			return nil
		end
	end

	-- Build up our drop-down items here for display inside our main element:
	local gameItems = {}
	local drawerHeight = 0
	gameItems["Layout"] = Roact.createElement("UIListLayout", {
		FillDirection = Enum.FillDirection.Vertical,
		HorizontalAlignment = Enum.HorizontalAlignment.Center,
		SortOrder = Enum.SortOrder.LayoutOrder,
		VerticalAlignment = Enum.VerticalAlignment.Top,
	})

	-- Display our pinned game (if we have one):
	local layoutOrder = 1
	local hasPinnedGame = false

	for _, game in ipairs(gameInfo.games) do
		if game.pinned then
			hasPinnedGame = true
			local placeId = game.placeId

			gameItems["PinnedTitle"] = Roact.createElement("TextButton", {
				AutoButtonColor = false,
				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				LayoutOrder = layoutOrder,
				Size = UDim2.new(1, 0, 0, PINNED_ICON_SIZE + (BORDER_SIZE * 2)),
				Text = "",
			}, {
				Icon = Roact.createElement("ImageLabel", {
					AnchorPoint = Vector2.new(0, 0.5),
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
					Image = PINNED_ICON,
					Position = UDim2.new(0, BORDER_SIZE, 0.5, 0),
					Size = UDim2.new(0, PINNED_ICON_SIZE, 0, PINNED_ICON_SIZE),
				}),

				Text = Roact.createElement("TextLabel", {
					AnchorPoint = Vector2.new(0, 0.5),
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
					Font = PINNED_TEXT_FONT,
					Position = UDim2.new(0, BORDER_SIZE + PINNED_ICON_SIZE + PINNED_SPACER, 0.5, 0),
					Size = UDim2.new(1, -(PINNED_ICON_SIZE + PINNED_SPACER + (BORDER_SIZE * 2)), 1, 0),
					Text = localization:Format("Feature.Chat.Drawer.PinnedGame"),
					TextColor3 = PINNED_TEXT_COLOR,
					TextSize = PINNED_TEXT_SIZE,
					TextXAlignment = Enum.TextXAlignment.Left,
					TextYAlignment = Enum.TextYAlignment.Center,
				}),
			})
			layoutOrder = layoutOrder + 1
			drawerHeight = drawerHeight + PINNED_ICON_SIZE + (BORDER_SIZE * 2)

			gameItems["Divider"] = Roact.createElement("Frame", {
				BackgroundColor3 = PINNED_DIVIDER_COLOR,
				BorderSizePixel = 0,
				LayoutOrder = layoutOrder,
				Size = UDim2.new(1, -(BORDER_SIZE * 2), 0, 1),
			})
			layoutOrder = layoutOrder + 1
			drawerHeight = drawerHeight + 1

			-- Index by pinned status and placeId:
			gameItems["Pinned" .. placeId] = Roact.createElement(ChatGameCard, {
				game = game,
				conversationId = self.conversationId,
				isPinnedGame = true,
				LayoutOrder = layoutOrder,
				Localization = localization,
				renderWidth = self.state.renderWidth,
				onGameStart = function()
					self:GameStart(placeId)
				end,
				onGameUnpin = function()
					self:UnpinGame()
				end,
				onViewDetails = function()
					self:ViewGameDetails(placeId)
				end,
			})
			layoutOrder = layoutOrder + 1
			drawerHeight = drawerHeight + CARD_HEIGHT_LARGE

			-- If we have more games to display, add a spacer between the pinned and regular games:
			if (countGames > 1) then
				gameItems["Spacer"] = Roact.createElement("Frame", {
					BackgroundColor3 = PINNED_BOTTOM_BACKGROUND,
					BackgroundTransparency = 0,
					BorderColor3 = PINNED_BOTTOM_BORDER,
					BorderSizePixel = 1,
					LayoutOrder = layoutOrder,
					Size = UDim2.new(1, 0, 0, PINNED_SPACER),
				})
				layoutOrder = layoutOrder + 1
				drawerHeight = drawerHeight + PINNED_SPACER
			end

			-- Done, we found our pinned game in the list:
			break
		end
	end

	-- Display all the other games in progress - but only if we don't have a
	-- pinned game or we're expanded:
	if (not hasPinnedGame) or isExpanded then
		local hasRegularGame = false
		for _, game in ipairs(gameInfo.games) do
			if not game.pinned then
				-- If we've already added a regular game, insert a spacer before the next:
				if hasRegularGame then
					gameItems[layoutOrder] = Roact.createElement("Frame", {
						BackgroundTransparency = 1,
						BorderSizePixel = 0,
						LayoutOrder = layoutOrder,
						Size = UDim2.new(1, 0, 0, 1),
					},{
						divider = Roact.createElement("Frame", {
							AnchorPoint = Vector2.new(1, 0),
							BorderSizePixel = 0,
							BackgroundColor3 = PINNED_DIVIDER_COLOR,
							Position = UDim2.new(1, 0, 0, 0),
							Size = UDim2.new(1, -SMALL_DIVIDER_OFFSET, 0, 1),
						}),
					})
					layoutOrder = layoutOrder + 1
					drawerHeight = drawerHeight + 1
				end

				local placeId = game.placeId
				-- Index as an unpinned game and placeId:
				gameItems["Game" .. placeId] = Roact.createElement(ChatGameCard, {
					game = game,
					conversationId = self.conversationId,
					isPinnedGame = false,
					isRecommended = game.recommended,
					LayoutOrder = layoutOrder,
					Localization = self.props.Localization,
					renderWidth = self.state.renderWidth,
					onGameStart = function()
						self:GameStart(placeId)
					end,
					onGamePin = function(universeId)
						self:PinGame(universeId)
					end,
					onViewDetails = function()
						self:ViewGameDetails(placeId)
					end,
				})
				layoutOrder = layoutOrder + 1
				drawerHeight = drawerHeight + CARD_HEIGHT_SMALL

				-- If we're not expanded, we've hit our limit:
				if not isExpanded then
					break
				end

				-- Next card will have a spacer before it.
				hasRegularGame = true
			end
		end
	end

	-- The final item in the list should be the text to either show more or hide:
	local endTextDivider = false
	local endTextShow = false
	local endLocalizeText = ""
	if countGames == 0 then
		endTextShow = true
		endLocalizeText = localization:Format("Feature.Chat.Drawer.NoGames")
	elseif countGames > 1 then
		if isExpanded then
			endLocalizeText = localization:Format("Feature.Chat.Drawer.ShowLess")
		else
			endLocalizeText = localization:Format("Feature.Chat.Drawer.ShowMore") .. " (+" .. (countGames - 1) .. ")"
		end
		endTextDivider = true
		endTextShow = true
	end

	if endTextShow then
		if endTextDivider then
			gameItems["DividerBottom"] = Roact.createElement("Frame", {
				BorderSizePixel = 0,
				BackgroundColor3 = PINNED_DIVIDER_COLOR,
				LayoutOrder = layoutOrder,
				Size = UDim2.new(1, 0, 0, 1),
			})
			layoutOrder = layoutOrder + 1
			drawerHeight = drawerHeight + PINNED_SPACER
		end

		gameItems["ShowButton"] = Roact.createElement("TextButton", {
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Font = PINNED_TEXT_FONT,
			LayoutOrder = layoutOrder,
			Size = UDim2.new(1, 0, 0, MORE_TEXT_SIZE + (MORE_TEXT_PADDING * 2)),
			Text = endLocalizeText,
			TextColor3 = MORE_TEXT_COLOR,
			TextSize = MORE_TEXT_SIZE,
			[Roact.Event.Activated] = function()
				self:setState({ isExpanded = not self.state.isExpanded })
			end
		})
		drawerHeight = drawerHeight + MORE_TEXT_SIZE + (MORE_TEXT_PADDING * 2)
	end

	-- Define the shadow component to hang off the bottom of the list:
	-- Note: Do not count the height since this isn't inside the frame.
	local shadow = Roact.createElement("ImageLabel", {
		BackgroundTransparency = 1,
		Image = DRAWER_SHADOW_IMAGE,
		Size = UDim2.new(1, 0, 0, DRAWER_SHADOW_HEIGHT),
		Position = UDim2.new(0, 0, 1, 0),
	})

	spawn(function()
		onSize(drawerHeight, hasFriendsActive)
	end)

	-- Create and return the main control itself:
	return Roact.createElement("Frame", {
		AnchorPoint = anchorPoint,
		BackgroundColor3 = DRAWER_BACKGROUND_COLOR,
		BackgroundTransparency = 0,
		BorderSizePixel = 0,
		ClipsDescendants = false,
		LayoutOrder = parentLayoutOrder,
		Position = position,
		Size = UDim2.new(1, 0, 1, 0),
		[Roact.Ref] = function(rbx)
			if not rbx then
				return
			end
			spawn(function()
				self:resolveMetrics(rbx)
			end)
		end,
	}, {
		Pointer = Roact.createElement("ImageLabel", {
			AnchorPoint = Vector2.new(0.5, 1),
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Image = ICON_POINTER_UP,
			ImageTransparency = pointerTransparency,
			Position = pointerPosition,
			Size = UDim2.new(0, ICON_POINTER_WIDTH, 0, ICON_POINTER_HEIGHT),
		}),
		Shadow = shadow,

		Frame = Roact.createElement("Frame", {
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			ClipsDescendants = true,
			Size = UDim2.new(1, 0, 1, 0),
		},
			gameItems
		)
	})
end

function ChatGameDrawer:resolveMetrics(rbx)
	-- This function finds the ActiveGameIcon and positions an arrow pointing
	-- at it from our open drawer. The position of the icon can change depending
	-- on a number of factors so it can't be hardcoded.
	--
	-- Also retrieves the actual width of our drawer to pass to child components
	-- which need to be width-aware to render properly.
	--
	-- Note 1: I didn't want to attach this on the icon because it needs to line
	-- up with the edge of the drawer.)
	--
	-- Note 2: we can't examine the GameDrawer position here because on the
	-- initial pass through it is invisible with a position of 0,0 on screen.

	-- Find the conversation header:
	local header = rbx:FindFirstAncestor("HeaderFrame")
	if header == nil then
		warn("Couldn't find header.")
		return
	end

	-- Find the "Play Together" icon:
	local iconPlayTogether = header:FindFirstChild("TopGameIcon", true)
	if iconPlayTogether == nil then
		warn("Couldn't find Play Together icon.")
		return
	end

	-- Figure out where on the screen iconPlayTogether is, so
	-- we can position our pointer directly underneath it:
	local iconFromEdge = (header.AbsolutePosition.X + header.AbsoluteSize.X) -
		(iconPlayTogether.AbsolutePosition.X + (iconPlayTogether.AbsoluteSize.X * 0.5))

	-- Track our drawer's width for content-aware scaling:
	local renderWidth = rbx.AbsoluteSize.X

	-- Prevent updating metrics if we already have the correct values:
	if (not self.state.pointerSet) or
		(self.state.renderWidth ~= renderWidth) or
		(self.state.pointerPosition.X.Offset ~= -iconFromEdge) then
		-- Update the pointer position state so it will render in the correct location:
		-- Yes, we're using another spawn call here - but we need the 1-frame delay.
		spawn(function()
			self:setState({
				pointerPosition = UDim2.new(1, -iconFromEdge, 0, 0),
				pointerSet = true,
				renderWidth = renderWidth,
			})
		end)
	end
end

ChatGameDrawer = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			conversations = state.ChatAppReducer.Conversations,
			mostRecentlyPlayedGames = state.ChatAppReducer.MostRecentlyPlayedGames,
			users = state.Users,
		}
	end,
	function(dispatch)
		return {
			playTogetherUnpinGame = function(conversationId)
				dispatch(PlayTogetherActions.UnpinGame(conversationId))
			end,
			playTogetherPinGame = function(conversationId, universeId)
				dispatch(PlayTogetherActions.PinGame(conversationId, universeId))
			end,
		}
	end
)(ChatGameDrawer)

return ChatGameDrawer