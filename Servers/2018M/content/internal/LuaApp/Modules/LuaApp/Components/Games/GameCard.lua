local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local Text = require(Modules.Common.Text)
local memoize = require(Modules.Common.memoize)

local Constants = require(Modules.LuaApp.Constants)
local RoactMotion = require(Modules.LuaApp.RoactMotion)
local NotificationType = require(Modules.LuaApp.Enum.NotificationType)

local UIScaler = require(Modules.LuaApp.Components.UIScaler)
local GameVoteBar = require(Modules.LuaApp.Components.Games.GameVoteBar)
local GameThumbnail = require(Modules.LuaApp.Components.GameThumbnail)
local LocalizedTextLabel = require(Modules.LuaApp.Components.LocalizedTextLabel)

local AppGuiService = require(Modules.LuaApp.Services.AppGuiService)
local RoactServices = require(Modules.LuaApp.RoactServices)

local FlagSettings = require(Modules.LuaApp.FlagSettings)

local useCppTextTruncation = FlagSettings.UseCppTextTruncation()

-- Define static positions on the card:
local DEFAULT_ICON_SCALE = 1
local PRESSED_ICON_SCALE = 0.9
local BUTTON_DOWN_STIFFNESS = 1000
local BUTTON_DOWN_DAMPING = 50
local BUTTON_DOWN_SPRING_PRECISION = 0.5

local OUTER_MARGIN = 6
local INNER_MARGIN = 3
local TITLE_HEIGHT = 15
local PLAYER_COUNT_HEIGHT = 15
local THUMB_ICON_SIZE = 12
local VOTE_FRAME_HEIGHT = THUMB_ICON_SIZE
local SPONSOR_HEIGHT = 13

local VOTE_BAR_HEIGHT = 4
local VOTE_BAR_TOP_MARGIN = 5
local VOTE_BAR_LEFT_MARGIN = THUMB_ICON_SIZE + 3

local TITLE_COLOR = Constants.Color.GRAY1
local COUNT_COLOR = Constants.Color.GRAY2
local SPONSOR_COLOR = Constants.Color.GRAY2
local SPONSOR_TEXT_COLOR = Constants.Color.WHITE

local SHADOW_SPREAD_TOP = 5
local SHADOW_SPREAD_BOTTOM = 6
local SHADOW_SPREAD_LEFT = 6
local SHADOW_SPREAD_RIGHT = 6
local SHADOW_SLICE_CENTER = Rect.new(11, 11, 12, 12)

local defaultGameIcon = "rbxasset://textures/ui/LuaApp/icons/ic-game.png"
local thumbUpImage = "rbxasset://textures/ui/LuaApp/voteBar/thumbup.png"

local function FormatInteger(num, sep, sepCount)
	assert(type(num) == "number", "FormatInteger expects a number; was given type: " .. type(num))

	sep = sep or ","
	sepCount = sepCount or 3

	local parsedInt = string.format("%.0f", math.abs(num))
	local firstSeperatorIndex = #parsedInt % sepCount
	if firstSeperatorIndex == 0 then
		firstSeperatorIndex = sepCount
	end

	local seperatorPattern = "(" .. string.rep("%d", sepCount) .. ")"
	local seperatorReplacement = sep .. "%1"
	local result = parsedInt:sub(1, firstSeperatorIndex) ..
		parsedInt:sub(firstSeperatorIndex+1):gsub(seperatorPattern, seperatorReplacement)
	if num < 0 then
		result = "-" .. result
	end

	return result
end

local GameCard = Roact.PureComponent:extend("GameCard")

function GameCard:eventDisconnect()
	if self.onAbsolutePositionChanged then
		self.onAbsolutePositionChanged:Disconnect()
		self.onAbsolutePositionChanged = nil
	end
end

function GameCard:onButtonUp(buttonActivated)
	if self.state.buttonDown or self.state.buttonActivated ~= buttonActivated then
		self:setState({
			buttonDown = false,
			buttonActivated = buttonActivated,
		})
	end
	self:eventDisconnect()
end

function GameCard:onButtonDown()
	if not self.state.buttonDown then
		self:eventDisconnect()
		self.onAbsolutePositionChanged = self.ref:GetPropertyChangedSignal("AbsolutePosition"):Connect(function()
			self:onButtonUp(false)
		end)
		self:setState({
			buttonDown = true,
			buttonActivated = false,
		})
	end
end

function GameCard:init()
	-- Truncating the title is really slow so lets memoize it for later use
	-- We need to memoize per instance because memoize only saves the last input
	self.makeTitle = memoize(Text.Truncate)

	self.state = {
		buttonDown = false,
		buttonActivated = false,
	}

	local openGameDetails = self.openGameDetails
	self.openGameDetails = function(...)
		openGameDetails(self, ...)
	end

	self.onButtonInputBegan = function(_, inputObject)
		if inputObject.UserInputState == Enum.UserInputState.Begin and
			(inputObject.UserInputType == Enum.UserInputType.Touch or
			inputObject.UserInputType == Enum.UserInputType.MouseButton1) then
			self:onButtonDown()
		end
	end

	self.onButtonActivated = function()
		self:onButtonUp(true)
	end

	self.onButtonInputEnded = function()
		self:onButtonUp(false)
	end

	self.onRef = function(rbx)
		self.ref = rbx
	end
end

local lastGameDetailsOpenTime = 0

function GameCard:openGameDetails()
	-- This is a temporary fix to debounce when the user taps two GameCards at once.
	-- Otherwise, it opens two web overlays.
	-- The proper solution is in MOBLUAPP-435, and this code should be removed when that is done.
	local currentTime = tick()
	if currentTime < (lastGameDetailsOpenTime + 1) then
		return
	end
	lastGameDetailsOpenTime = currentTime

	local notificationType = NotificationType.VIEW_GAME_DETAILS
	self.props.guiService:BroadcastNotification(string.format("%d", self.props.game.placeId), notificationType)

	-- fire some analytics
	local index = self.props.index
	local reportGameDetailOpened = self.props.reportGameDetailOpened
	reportGameDetailOpened(index)
end

function GameCard:render()
	local entry = self.props.entry
	local size = self.props.size
	local layoutOrder = self.props.layoutOrder
	local game = self.props.game

	local name = game.name
	local universeId = game.universeId
	local totalDownVotes = game.totalDownVotes
	local totalUpVotes = game.totalUpVotes

	local playerCount = entry.playerCount
	local isSponsored = entry.isSponsored

	local totalVotes = totalUpVotes + totalDownVotes
	local votePercentage
	if totalVotes == 0 then
		votePercentage = 0
	else
		votePercentage = totalUpVotes / totalVotes
	end

	return Roact.createElement("Frame", {
		Size = UDim2.new(0, size.X, 0, size.Y),
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		LayoutOrder = layoutOrder,

		[Roact.Ref] = self.onRef,
	}, {
		GameButton = Roact.createElement("TextButton", {
			AnchorPoint = Vector2.new(0.5, 0.5),
			Position = UDim2.new(0.5, 0, 0.5, 0),
			Size = UDim2.new(1, 0, 1, 0),
			BackgroundTransparency = 1,
			AutoButtonColor = false,
			ZIndex = 2,

			[Roact.Event.InputBegan] = self.onButtonInputBegan,
			[Roact.Event.InputEnded] = self.onButtonInputEnded,
			[Roact.Event.Activated] = self.onButtonActivated,
		}, {
			UIScaler = Roact.createElement(UIScaler, {
				scaleValue = RoactMotion.spring(self.state.buttonDown and PRESSED_ICON_SCALE or
						DEFAULT_ICON_SCALE, BUTTON_DOWN_STIFFNESS, BUTTON_DOWN_DAMPING, BUTTON_DOWN_SPRING_PRECISION),
				onRested = self.state.buttonActivated and self.openGameDetails or nil,
			}),
			Shadow = Roact.createElement("ImageLabel", {
				Size = UDim2.new(1, SHADOW_SPREAD_LEFT + SHADOW_SPREAD_RIGHT, 1, SHADOW_SPREAD_TOP + SHADOW_SPREAD_BOTTOM),
				Position = UDim2.new(0, -SHADOW_SPREAD_LEFT, 0, -SHADOW_SPREAD_TOP),
				Image = "rbxasset://textures/ui/LuaApp/9-slice/gr-shadow.png",
				ScaleType = "Slice",
				SliceCenter = SHADOW_SLICE_CENTER,
				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				ZIndex = 1,
			}),
			Icon = Roact.createElement(GameThumbnail, {
				Size = UDim2.new(0, size.X, 0, size.X),
				universeId = universeId,
				BorderSizePixel = 0,
				BackgroundColor3 = Constants.Color.GRAY5,
				loadingImage = defaultGameIcon,
				ZIndex = 2,
			}),

			GameInfo = Roact.createElement("Frame", {
				Size = UDim2.new(1, 0, 0, size.Y - size.X),
				Position = UDim2.new(0, 0, 0, size.X),
				BackgroundTransparency = 0,
				BorderSizePixel = 0,
				BackgroundColor3 = Constants.Color.WHITE,
				ZIndex = 2,
			}, {
				Layout = Roact.createElement("UIListLayout", {
					SortOrder = Enum.SortOrder.LayoutOrder,
					Padding = UDim.new(0, INNER_MARGIN),
				}),

				Padding = Roact.createElement("UIPadding", {
					PaddingLeft = UDim.new(0, OUTER_MARGIN),
					PaddingRight = UDim.new(0, OUTER_MARGIN),
					PaddingTop = UDim.new(0, OUTER_MARGIN),
				}),

				Title = Roact.createElement("TextLabel", {
					LayoutOrder = 1,
					Size = UDim2.new(1, 0, 0, TITLE_HEIGHT),
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
					TextSize = TITLE_HEIGHT,
					TextColor3 = TITLE_COLOR,
					Font = Enum.Font.SourceSans,
					Text = useCppTextTruncation and name
							or self.makeTitle(name, Enum.Font.SourceSans, TITLE_HEIGHT, size.X-OUTER_MARGIN*2, "..."),
					TextTruncate = Enum.TextTruncate.AtEnd,
					TextXAlignment = Enum.TextXAlignment.Left,
					TextYAlignment = Enum.TextYAlignment.Top, -- Center sinks the text down by 2 pixels
				}),
				PlayerCount = not isSponsored and Roact.createElement(LocalizedTextLabel, {
					LayoutOrder = 2,
					Size = UDim2.new(1, 0, 0, PLAYER_COUNT_HEIGHT),
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
					TextSize = PLAYER_COUNT_HEIGHT,
					TextColor3 = COUNT_COLOR,
					Font = Enum.Font.SourceSans,
					Text = { "Feature.GamePage.LabelPlayingPhrase", playerCount = FormatInteger(playerCount) },
					TextXAlignment = Enum.TextXAlignment.Left,
					TextYAlignment = Enum.TextYAlignment.Top, -- Center sinks the text down by 2 pixels
				}),
				VoteFrame = not isSponsored and Roact.createElement("Frame", {
					LayoutOrder = 3,
					Size = UDim2.new(1, 0, 0, VOTE_FRAME_HEIGHT),
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
				}, {
					ThumbUpIcon = Roact.createElement("ImageLabel", {
						Size = UDim2.new(0, THUMB_ICON_SIZE, 0, THUMB_ICON_SIZE),
						BackgroundTransparency = 1,
						BorderSizePixel = 0,
						Image = thumbUpImage,
					}),
					VoteBar = Roact.createElement(GameVoteBar, {
						Size = UDim2.new(1, -THUMB_ICON_SIZE, 0, VOTE_BAR_HEIGHT),
						Position = UDim2.new(0, VOTE_BAR_LEFT_MARGIN, 0, VOTE_BAR_TOP_MARGIN),
						votePercentage = votePercentage,
					})
				}),
			}),
			Sponsor = isSponsored and Roact.createElement("Frame", {
				Size = UDim2.new(1, 0, 0, SPONSOR_HEIGHT+OUTER_MARGIN*2),
				Position = UDim2.new(0, 0, 1, 0),
				AnchorPoint = Vector2.new(0, 1),
				BackgroundColor3 = SPONSOR_COLOR,
				BorderSizePixel = 0,
				ZIndex = 3,
			}, {
				SponsorText = Roact.createElement(LocalizedTextLabel, {
					Size = UDim2.new(1, -OUTER_MARGIN*2, 0, SPONSOR_HEIGHT),
					Position = UDim2.new(0, OUTER_MARGIN, 0, OUTER_MARGIN),
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
					TextSize = SPONSOR_HEIGHT,
					TextColor3 = SPONSOR_TEXT_COLOR,
					Font = Enum.Font.SourceSans,
					Text = "Feature.GamePage.Label.Sponsored",
				})
			}),
		})
	})
end

function GameCard:willUnmount()
	self:eventDisconnect()
end

GameCard = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			game = state.Games[props.entry.universeId],
		}
	end
)(GameCard)

return RoactServices.connect({
	guiService = AppGuiService
})(GameCard)