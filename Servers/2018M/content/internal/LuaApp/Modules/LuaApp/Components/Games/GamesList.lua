local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local memoize = require(Modules.Common.memoize)
local RoactServices = require(Modules.LuaApp.RoactServices)
local RoactNetworking = require(Modules.LuaApp.Services.RoactNetworking)
local RoactAnalyticsGamesPage = require(Modules.LuaApp.Services.RoactAnalyticsGamesPage)
local RoactAnalyticsHomePage = require(Modules.LuaApp.Services.RoactAnalyticsHomePage)

local Constants = require(Modules.LuaApp.Constants)
local AppPage = require(Modules.LuaApp.AppPage)

local NavigateSideways = require(Modules.LuaApp.Thunks.NavigateSideways)

local DropDownList = require(Modules.LuaApp.Components.DropDownList)
local GameGrid = require(Modules.LuaApp.Components.Games.GameGrid)
local TopBar = require(Modules.LuaApp.Components.TopBar)
local RefreshScrollingFrame = require(Modules.LuaApp.Components.RefreshScrollingFrame)
local ApiFetchGamesData = require(Modules.LuaApp.Thunks.ApiFetchGamesData)
local ApiFetchGamesInSort = require(Modules.LuaApp.Thunks.ApiFetchGamesInSort)

local GAME_GRID_PADDING = Constants.GAME_GRID_PADDING
local DROPDOWN_HEIGHT = 38
local DROPDOWN_SECTION_HEADER_GAP = 12
local SECTION_HEADER_HEIGHT = Constants.SECTION_HEADER_HEIGHT
local SECTION_HEADER_GAME_GRID_GAP = 14
local TOP_SECTION_HEIGHT = DROPDOWN_HEIGHT + DROPDOWN_SECTION_HEADER_GAP +
	SECTION_HEADER_HEIGHT + SECTION_HEADER_GAME_GRID_GAP

local GamesList = Roact.PureComponent:extend("GamesList")

function GamesList:init()
	self.refresh = function()
		return self.props.dispatchRefresh(self.props.networking, self.props.sortName)
	end

	self.loadMoreGames = function(count)
		local loadCount = count or Constants.DEFAULT_GAME_FETCH_COUNT
		local sorts = self.props.sorts
		local selectedSortName = self.props.sortName
		local dispatchLoadMoreGames = self.props.dispatchLoadMoreGames
		local networking = self.props.networking

		local selectedSort = sorts[selectedSortName]

		return dispatchLoadMoreGames(networking, selectedSort, selectedSort.rowsRequested, loadCount,
			selectedSort.nextPageExclusiveStartId)
	end

	self.navigateToSort = function(sort, position)
		self.props.analytics.reportFilterChange(sort.name, position)
		self.props.navigateToSort(sort)
	end

	self.reportGameDetailOpened = function(index)
		local selectedSortName = self.props.sortName
		local sorts = self.props.sorts
		local analytics = self.props.analytics

		local selectedSort = sorts[selectedSortName]
		local entries = selectedSort.entries

		local itemsInSort = #entries
		local entry = entries[index]
		local placeId = entry.placeId
		local isAd = entry.isSponsored

		analytics.reportOpenGameDetail(
			placeId,
			selectedSortName,
			index,
			itemsInSort,
			isAd)
	end
end

function GamesList:render()
	local topBarHeight = self.props.topBarHeight
	local selectedSortName = self.props.sortName
	local sorts = self.props.sorts
	local screenSize = self.props.screenSize

	local selectedSort = sorts[selectedSortName]

	-- Build up the outer frame of the page, to include our components:
	return Roact.createElement("Frame", {
		Size = UDim2.new(1, 0, 1, 0),
		BorderSizePixel = 0,
	},{
		TopBar = Roact.createElement(TopBar, {
			ZIndex = 2,
			showBackButton = true,
			showBuyRobux = true,
			showNotifications = true,
			showSearch = true,
		}),
		Scroller = Roact.createElement(RefreshScrollingFrame, {
			Position = UDim2.new(0, 0, 0, topBarHeight),
			Size = UDim2.new(1, 0, 1, -topBarHeight),
			BackgroundColor3 = Constants.Color.GRAY4,
			CanvasSize = UDim2.new(1, 0, 0, 0),
			refresh = self.refresh,
			onLoadMore = selectedSort.hasMoreRows and self.loadMoreGames,
			-- If there're no more games, create an end section.
			createEndOfScrollElement = not selectedSort.hasMoreRows,
		}, {
			Layout = Roact.createElement("UIListLayout", {
				FillDirection = Enum.FillDirection.Vertical,
				HorizontalAlignment = Enum.HorizontalAlignment.Center,
				SortOrder = Enum.SortOrder.LayoutOrder,
			}),
			Padding = Roact.createElement("UIPadding", {
				PaddingLeft = UDim.new(0, GAME_GRID_PADDING),
				PaddingRight = UDim.new(0, GAME_GRID_PADDING),
				PaddingTop = UDim.new(0, GAME_GRID_PADDING),
			}),
			TopSection = Roact.createElement("Frame", {
				BackgroundTransparency = 1,
				LayoutOrder = 1,
				Size = UDim2.new(1, 0, 0, TOP_SECTION_HEIGHT),
			}, {
				DropDown = Roact.createElement(DropDownList, {
					size = UDim2.new(1, 0, 0, DROPDOWN_HEIGHT),
					position = UDim2.new(0, 0, 0, 0),
					itemSelected = selectedSort,
					items = sorts,
					onSelected = self.navigateToSort,
				}),
				Title = Roact.createElement("TextLabel", {
					Text = selectedSort.displayName,
					Position = UDim2.new(0, 0, 0, DROPDOWN_HEIGHT + DROPDOWN_SECTION_HEADER_GAP),
					TextSize = SECTION_HEADER_HEIGHT,
					Font = Enum.Font.SourceSansLight,
					TextXAlignment = Enum.TextXAlignment.Left,
					TextYAlignment = Enum.TextYAlignment.Top,
					BackgroundTransparency = 1,
					TextTruncate = Enum.TextTruncate.AtEnd,
					Size = UDim2.new(1, 0, 0, SECTION_HEADER_HEIGHT)
				}),
			}),
			["GameGrid " .. selectedSortName] = Roact.createElement(GameGrid, {
				LayoutOrder = 2,
				entries = selectedSort.entries,
				reportGameDetailOpened = self.reportGameDetailOpened,
				windowSize = Vector2.new(screenSize.X - 2 * GAME_GRID_PADDING, screenSize.Y),
			}),
		}),
	})
end

local function sortSorts(a, b)
	return a.displayName < b.displayName
end

local selectSorts = memoize(function(gameSorts, gameSortsContents)
	local sorts = {}

	for _, sortInfo in pairs(gameSorts) do
		local sort = sortInfo
		local gameSortContents = gameSortsContents[sort.name]

		-- These fields are used for infinite scroll.
		sort.entries = gameSortContents.entries
		sort.rowsRequested = gameSortContents.rowsRequested
		sort.hasMoreRows = gameSortContents.hasMoreRows
		sort.nextPageExclusiveStartId = gameSortContents.nextPageExclusiveStartId

		table.insert(sorts, sort)
		sorts[sort.name] = sort
	end

	table.sort(sorts, sortSorts)
	return sorts
end)

local selectAnalytics = function(appRoutes, gamesAnalytics, homeAnalytics)
	local currentRoute = appRoutes[#appRoutes]
	local currentPage = currentRoute[1].name
	if currentPage == AppPage.Games then
		return gamesAnalytics
	elseif currentPage == AppPage.Home then
		return homeAnalytics
	else
		assert(false, string.format("Can not provide GamesList analytics for current page %s.", currentPage))
	end
end

GamesList = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			sorts = selectSorts(state.GameSorts, state.GameSortsContents),
			topBarHeight = state.TopBar.topBarHeight,
			analytics = selectAnalytics(state.Navigation.history, props.gamesAnalytics, props.homeAnalytics),
			screenSize = state.ScreenSize,
		}
	end,
	function(dispatch)
		return {
			dispatchRefresh = function(networking, sortName)
				return dispatch(ApiFetchGamesData(networking, nil, sortName))
			end,
			navigateToSort = function(sort)
				dispatch(NavigateSideways({ name = AppPage.GamesList, detail = sort.name }))
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
)(GamesList)

return RoactServices.connect({
	networking = RoactNetworking,
	gamesAnalytics = RoactAnalyticsGamesPage,
	homeAnalytics = RoactAnalyticsHomePage,
})(GamesList)