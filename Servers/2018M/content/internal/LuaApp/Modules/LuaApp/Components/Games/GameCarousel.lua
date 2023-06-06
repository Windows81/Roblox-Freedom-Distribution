local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local RoactServices = require(Modules.LuaApp.RoactServices)
local RoactNetworking = require(Modules.LuaApp.Services.RoactNetworking)

local FitChildren = require(Modules.LuaApp.FitChildren)
local Constants = require(Modules.LuaApp.Constants)
local AppPage = require(Modules.LuaApp.AppPage)
local getGameCardSize = require(Modules.LuaApp.getGameCardSize)

local SectionHeaderWithSeeAll = require(Modules.LuaApp.Components.SectionHeaderWithSeeAll)
local GameCard = require(Modules.LuaApp.Components.Games.GameCard)
local ApiFetchGamesInSort = require(Modules.LuaApp.Thunks.ApiFetchGamesInSort)

local NavigateDown = require(Modules.LuaApp.Thunks.NavigateDown)

local CAROUSEL_MARGIN = Constants.GAME_CAROUSEL_PADDING
local CARD_MARGIN = Constants.GAME_CAROUSEL_CHILD_PADDING
local CAROUSEL_AND_HEADER_HEIGHT = 183

-- We would like to start loading more before user reaches the end.
-- The default distance from the bottom of that would be 1000.
local DEFAULT_PRELOAD_DISTANCE = 1000

local GameCarousel = Roact.PureComponent:extend("GameCarousel")

function GameCarousel:init()
	self.state = {
		cardWindowStart = 1,
		cardsInWindow = 0,
		gameCardSize = Vector2.new(0, 0),
	}

	self.isLoadingMoreGames = false

	self.scrollingFrameRefCallback = function(rbx)
		self.scrollingFrameRef = rbx
	end

	self.onCanvasPositionChanged = function()
		-- Since this function is spawned, it's possible that the component
		-- has been destroyed.
		if not self.scrollingFrameRef then
			return
		end

		local gameSortContents = self.props.gameSortContents
		local loadMoreGames = self.loadMoreGames
		local canLoadMore = gameSortContents.hasMoreRows

		if canLoadMore and not self.isLoadingMoreGames then
			local canvasPosition = self.scrollingFrameRef.CanvasPosition.X
			local windowWidth = self.scrollingFrameRef.AbsoluteWindowSize.X
			local canvasWidth = self.scrollingFrameRef.CanvasSize.X.Offset
			local loadMoreThreshold = canvasWidth - windowWidth - DEFAULT_PRELOAD_DISTANCE

			if canvasPosition > loadMoreThreshold then
				self.isLoadingMoreGames = true

				loadMoreGames():andThen(
					function()
						self.isLoadingMoreGames = false
					end,
					function()
						self.isLoadingMoreGames = false
					end
				)
			end
		end
	end

	self.updateCardWindowBounds = function()
		if not self.scrollingFrameRef then
			return
		end

		local screenSize = self.props.screenSize
		local containerWidth = screenSize.X - CAROUSEL_MARGIN
		local windowOffset = self.scrollingFrameRef.CanvasPosition.X

		local gameCardSize, fractionalCardsPerRow = getGameCardSize(containerWidth, 0, CARD_MARGIN, 0.25)

		local cardWindowStart = math.max(1, math.floor(windowOffset / (gameCardSize.X + CARD_MARGIN)))
		local cardsInWindow = math.ceil(fractionalCardsPerRow) + 2

		local shouldUpdate = cardWindowStart ~= self.state.cardWindowStart
			or cardsInWindow ~= self.state.cardsInWindow
			or gameCardSize ~= self.state.gameCardSize

		if shouldUpdate then
			self:setState({
				cardWindowStart = cardWindowStart,
				cardsInWindow = cardsInWindow,
				gameCardSize = gameCardSize,
			})
		end
	end

	self.onSeeAll = function()
		local navigateToSort = self.props.navigateToSort
		local sort = self.props.sort
		local analytics = self.props.analytics
		local layoutOrder = self.props.LayoutOrder

		-- show the sort
		navigateToSort(self.props.sortName)

		-- report to the server that we've tapped on the SeeAll button
		analytics.reportSeeAll(sort.name, layoutOrder)
	end

	self.reportGameDetailOpened = function(index)
		local sort = self.props.sort
		local gameSortContents = self.props.gameSortContents
		local analytics = self.props.analytics

		local entries = gameSortContents.entries

		local sortName = sort.name
		local itemsInSort = #entries
		local indexInSort = index
		local entry = entries[index]
		local placeId = entry.placeId
		local isAd = entry.isSponsored

		analytics.reportOpenGameDetail(
			placeId,
			sortName,
			indexInSort,
			itemsInSort,
			isAd)
	end

	self.loadMoreGames = function(count)
		local loadCount = count or Constants.DEFAULT_GAME_FETCH_COUNT
		local networking = self.props.networking
		local sort = self.props.sort
		local gameSortContents = self.props.gameSortContents
		local dispatchLoadMoreGames = self.props.dispatchLoadMoreGames

		return dispatchLoadMoreGames(networking, sort, gameSortContents.rowsRequested, loadCount,
			gameSortContents.nextPageExclusiveStartId)
	end
end

function GameCarousel:render()
	local sort = self.props.sort
	local gameSortContents = self.props.gameSortContents
	local layoutOrder = self.props.LayoutOrder

	local entries = gameSortContents.entries

	local gameCardSize = self.state.gameCardSize
	local cardWindowStart = self.state.cardWindowStart
	local cardsInWindow = self.state.cardsInWindow

	local cardWindowEnd = math.min(#entries, cardWindowStart + cardsInWindow - 1)

	local canvasWidth = math.max(0, #entries * (CARD_MARGIN + gameCardSize.X))
	local leftPadding = (cardWindowStart - 1) * (gameCardSize.X + CARD_MARGIN)

	local gameCards = {}

	gameCards.Layout = Roact.createElement("UIListLayout", {
		SortOrder = Enum.SortOrder.LayoutOrder,
		FillDirection = Enum.FillDirection.Horizontal,
		Padding = UDim.new(0, CARD_MARGIN),
		HorizontalAlignment = Enum.HorizontalAlignment.Left,
	})

	gameCards.Padding = Roact.createElement("UIPadding", {
		PaddingLeft = UDim.new(0, leftPadding),
	})

	for index = cardWindowStart, cardWindowEnd do
		local entry = entries[index]
		local key = index % cardsInWindow

		gameCards[key] = Roact.createElement(GameCard, {
			entry = entry,
			layoutOrder = index,
			size = gameCardSize,
			reportGameDetailOpened = self.reportGameDetailOpened,
			index = index,
		})
	end

	return Roact.createElement(FitChildren.FitFrame, {
		LayoutOrder = layoutOrder,
		BackgroundTransparency = 1,
		Size = UDim2.new(1, 0, 0, CAROUSEL_AND_HEADER_HEIGHT),
		fitFields = {
			Size = FitChildren.FitAxis.Height,
		},
	}, {
		Layout = Roact.createElement("UIListLayout", {
			SortOrder = Enum.SortOrder.LayoutOrder,
			FillDirection = Enum.FillDirection.Vertical,
		}),
		Title = Roact.createElement(SectionHeaderWithSeeAll, {
			LayoutOrder = 1,
			text = sort.displayName,
			value = sort,
			onSelected = self.onSeeAll,
		}),
		Carousel = Roact.createElement("ScrollingFrame", {
			LayoutOrder = 2,
			Size = UDim2.new(1, CAROUSEL_MARGIN, 0, gameCardSize.Y),
			ScrollBarThickness = 0,
			BackgroundTransparency = 1,
			ClipsDescendants = false, -- Needed to display drop shadows
			CanvasSize = UDim2.new(0, canvasWidth, 0, gameCardSize.Y),
			ScrollingDirection = Enum.ScrollingDirection.X,

			[Roact.Change.CanvasPosition] = function()
				self.onCanvasPositionChanged()
				spawn(self.updateCardWindowBounds)
			end,
			[Roact.Ref] = self.scrollingFrameRefCallback,
		}, gameCards),
	})
end

function GameCarousel:didMount()
	self.updateCardWindowBounds()
end

function GameCarousel:didUpdate(prevProps)
	if self.props.screenSize ~= prevProps.screenSize then
		self.updateCardWindowBounds()
	end
end

GameCarousel = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			sort = state.GameSorts[props.sortName],
			gameSortContents = state.GameSortsContents[props.sortName],
			screenSize = state.ScreenSize,
		}
	end,
	function(dispatch)
		return {
			navigateToSort = function(sortName)
				dispatch(NavigateDown({ name = AppPage.GamesList, detail = sortName }))
			end,
			dispatchLoadMoreGames = function(networking, sort, startRows, maxRows, nextPageExclusiveStartId)
				return dispatch(ApiFetchGamesInSort(networking, sort, true, {
					startRows = startRows,
					maxRows = maxRows,
					exclusiveStartId = nextPageExclusiveStartId
				}))
			end
		}
	end
)(GameCarousel)

return RoactServices.connect({
	networking = RoactNetworking,
})(GameCarousel)