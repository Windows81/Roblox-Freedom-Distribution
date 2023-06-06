local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)

local Constants = require(Modules.LuaApp.Constants)
local FitChildren = require(Modules.LuaApp.FitChildren)
local FormFactor = require(Modules.LuaApp.Enum.FormFactor)

local GameGrid = require(Modules.LuaApp.Components.Games.GameGrid)
local SectionHeader = require(Modules.LuaApp.Components.SectionHeader)

local FTUE_NUMBER_OF_ROWS_FOR_GRID = {
	[FormFactor.PHONE] = 4,
	[FormFactor.TABLET] = 2,
}

local GAME_GRID_PADDING = Constants.GAME_GRID_PADDING
local SECTION_HEADER_HEIGHT = Constants.SECTION_HEADER_HEIGHT
local SECTION_HEADER_GAME_GRID_GAP = 12
local TOP_SECTION_HEIGHT = SECTION_HEADER_HEIGHT + SECTION_HEADER_GAME_GRID_GAP

local HomeFTUEGameGrid = Roact.PureComponent:extend("HomeFTUEGameGrid")

function HomeFTUEGameGrid:init()
	self.reportGameDetailOpened = function(index)
		local sort = self.props.sort
		local gameSortContents = self.props.gameSortContents
		local analytics = self.props.analytics

		local entries = gameSortContents.entries

		local itemsInSort = #entries
		local entry = entries[index]
		local placeId = entry.placeId
		local isAd = entry.isSponsored

		analytics.reportOpenGameDetail(
			placeId,
			sort.name,
			index,
			itemsInSort,
			isAd)
	end
end

function HomeFTUEGameGrid:render()
	local sort = self.props.sort
	local gameSortContents = self.props.gameSortContents
	local formFactor = self.props.formFactor
	local screenSize = self.props.screenSize
	local layoutOrder = self.props.LayoutOrder
	local hasTopPadding = self.props.hasTopPadding

	local paddingTop = hasTopPadding and GAME_GRID_PADDING or 0;

	return Roact.createElement(FitChildren.FitFrame, {
		Size = UDim2.new(1, 0, 1, 0),
		BackgroundTransparency = 1,
		fitFields = {
			Size = FitChildren.FitAxis.Height
		},
		LayoutOrder = layoutOrder,
	},{
		Layout = Roact.createElement("UIListLayout", {
			FillDirection = Enum.FillDirection.Vertical,
			HorizontalAlignment = Enum.HorizontalAlignment.Center,
			SortOrder = Enum.SortOrder.LayoutOrder,
		}),
		Padding = Roact.createElement("UIPadding", {
			PaddingLeft = UDim.new(0, GAME_GRID_PADDING),
			PaddingRight = UDim.new(0, GAME_GRID_PADDING),
			PaddingTop = UDim.new(0, paddingTop),
		}),
		SectionHeader = Roact.createElement("Frame", {
			BackgroundTransparency = 1,
			LayoutOrder = 1,
			Size = UDim2.new(1, 0, 0, TOP_SECTION_HEIGHT),
		}, {
			Title = Roact.createElement(SectionHeader, {
				text = sort.displayName,
			}),
		}),
		["GameGrid " .. sort.name] = Roact.createElement(GameGrid, {
			LayoutOrder = 2,
			entries = gameSortContents.entries,
			reportGameDetailOpened = self.reportGameDetailOpened,
			numberOfRowsToShow = FTUE_NUMBER_OF_ROWS_FOR_GRID[formFactor],
			windowSize = Vector2.new(screenSize.X - 2 * GAME_GRID_PADDING, screenSize.Y),
		}),
	})
end

local selectFTUESortName = function(sortGroups)
	local homeSortGroup = Constants.GameSortGroups.HomeGames
	local sorts = sortGroups[homeSortGroup].sorts

	-- This isn't the cleanest thing, but I can't figure out a better way
	return sorts[1]
end

return RoactRodux.UNSTABLE_connect2(
	function(state, props)
		local sortName = selectFTUESortName(state.GameSortGroups)

		return {
			sort = state.GameSorts[sortName],
			gameSortContents = state.GameSortsContents[sortName],
			formFactor = state.FormFactor,
			screenSize = state.ScreenSize,
		}
	end
)(HomeFTUEGameGrid)