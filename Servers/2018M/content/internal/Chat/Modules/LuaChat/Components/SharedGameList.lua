local Modules = game:GetService("CoreGui").RobloxGui.Modules
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local Constants = require(LuaChat.Constants)
local LocalizedTextLabel = require(LuaApp.Components.LocalizedTextLabel)
local LoadingIndicator = require(LuaApp.Components.LoadingIndicator)
local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local SharedGameItem = require(LuaChat.Components.SharedGameItem)
local ShareGameToChatThunks = require(LuaChat.Actions.ShareGameToChatFromChat.ShareGameToChatFromChatThunks)

local DEFAULT_BACKGROUND_COLOR = Constants.Color.GRAY6
local DEFAULT_ITEM_HEIGHT = 84
local DEFAULT_TIPS_LABEL_COLOR = Constants.Color.GRAY2
local DEFAULT_TIPS_LABEL_FONT = Enum.Font.SourceSans
local DEFAULT_TIPS_LABEL_HEIGHT = 25
local DEFAULT_TIPS_LABEL_TEXT_SIZE = 20
local DEFAULT_TIPS_LABEL_TOP_MARGIN = 30

local SCROLLING_FRAME_IMAGE = "rbxasset://textures/ui/LuaChat/9-slice/scroll-bar.png"

local SharedGameList = Roact.PureComponent:extend("SharedGameList")

SharedGameList.defaultProps = {
	backgroundColor = DEFAULT_BACKGROUND_COLOR,
	itemHeight = DEFAULT_ITEM_HEIGHT,
	tipsLabelColor = DEFAULT_TIPS_LABEL_COLOR,
	tipsLabelFont = DEFAULT_TIPS_LABEL_FONT,
	tipsLabelHeight = DEFAULT_TIPS_LABEL_HEIGHT,
	tipsLabelTextSize = DEFAULT_TIPS_LABEL_TEXT_SIZE,
	tipsLabelTopMargin = DEFAULT_TIPS_LABEL_TOP_MARGIN,
}

function SharedGameList:init()
	self.gamesList = nil
	self.isLoading = false

	self.onScrollingFrameRef = function(rbx)
		if rbx then
			self.gamesList = rbx
		else
			warn("can not capture scrolling frame")
		end
	end

	self:ShouldFetchGames(self.props)
end

function SharedGameList:render()
	local backgroundColor = self.props.backgroundColor
	local frameHeight = self.props.frameHeight
	local gamesDetailInfos = self.props.gamesInfo
	local gameSorts = self.props.gameSorts
	local itemHeight = self.props.itemHeight
	local sortName = self.props.gameSort
	local tipsLabelColor = self.props.tipsLabelColor
	local tipsLabelHeight = self.props.tipsLabelHeight
	local tipsLabelFont = self.props.tipsLabelFont
	local tipsLabelTextSize = self.props.tipsLabelTextSize
	local tipsLabelTopMargin = self.props.tipsLabelTopMargin

	local itemsCount = 0
	local gamesListItems = {}

	if not self.isLoading then
		gamesListItems["Layout"] = Roact.createElement("UIListLayout", {
			FillDirection = Enum.FillDirection.Vertical,
			VerticalAlignment = Enum.VerticalAlignment.Center,
		})

		local games = gameSorts[sortName]
		itemsCount = #games.placeIds
		for index, placeId in ipairs(games.placeIds) do
			gamesListItems[index] = Roact.createElement(SharedGameItem, {
				itemHeight = itemHeight,
				game = gamesDetailInfos[placeId],
			})
		end
	end

	local contentHeight = itemsCount * itemHeight

	return Roact.createElement("Frame", {
		BackgroundColor3 = backgroundColor,
		BorderSizePixel = 0,
		Size = UDim2.new(1, 0, 1, 0),
	}, {
		GamesList = itemsCount ~= 0 and Roact.createElement("ScrollingFrame", {
			BackgroundTransparency = 1,
			BottomImage = SCROLLING_FRAME_IMAGE,
			BorderSizePixel = 0,
			CanvasSize = UDim2.new(1, 0, 0, contentHeight),
			MidImage = SCROLLING_FRAME_IMAGE,
			Size = contentHeight > frameHeight and UDim2.new(1, 0, 1, 0) or UDim2.new(1, 0, 0, contentHeight),
			ScrollBarThickness = 5,
			ScrollingDirection = Enum.ScrollingDirection.Y,
			TopImage = SCROLLING_FRAME_IMAGE,

			[Roact.Ref] = self.onScrollingFrameRef,
		}, gamesListItems),

		Indicator = self.isLoading and Roact.createElement(LoadingIndicator, {
			AnchorPoint = Vector2.new(0.5, 0),
			Position = UDim2.new(0.5, 0, 0, tipsLabelTopMargin),
		}),

		NoGamesTip = ((not self.isLoading) and itemsCount == 0) and Roact.createElement(LocalizedTextLabel, {
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Font = tipsLabelFont,
			Position = UDim2.new(0, 0, 0, tipsLabelTopMargin),
			Size = UDim2.new(1, 0, 0, tipsLabelHeight),
			Text = Constants.SharedGamesConfig.SortsAttribute[sortName].ERROR_TIP_LOCALIZATION_KEY,
			TextColor3 = tipsLabelColor,
			TextSize = tipsLabelTextSize,
		}),
	})
end

function SharedGameList:didUpdate()
	if self.gamesList then
		self.gamesList.CanvasPosition = Vector2.new(0, 0)
	end
end

function SharedGameList:willUpdate(newProps)
	self:ShouldFetchGames(newProps)
end

function SharedGameList:ShouldFetchGames(props)
	local gameSorts = props.gameSorts
	local sortName = props.gameSort
	local games = gameSorts[sortName]

	self.isLoading = false
	if games == nil or games.placeIds == nil then
		if not ShareGameToChatThunks.HasGameFetchRequestCompleted(sortName, props.shareGameToChatAsync) then
			self.isLoading = true
			self.props.fetchGames(sortName, Constants.SharedGamesConfig.Thumbnail.FETCHED_SIZE)
		end
	end
end

return RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			gamesInfo = state.ChatAppReducer.SharedGamesInfo,
			gameSorts = state.ChatAppReducer.SharedGameSorts,
			shareGameToChatAsync = state.ChatAppReducer.ShareGameToChatAsync,
		}
	end,
	function(dispatch)
		return {
			fetchGames = function(gameSortName, fetchedThumbnailSize)
				return dispatch(ShareGameToChatThunks.FetchGames(gameSortName, fetchedThumbnailSize))
			end,
		}
	end
)(SharedGameList)