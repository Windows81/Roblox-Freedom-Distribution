local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local RoactAnalyticsGamesPage = require(Modules.LuaApp.Services.RoactAnalyticsGamesPage)
local RoactNetworking = require(Modules.LuaApp.Services.RoactNetworking)
local RoactServices = require(Modules.LuaApp.RoactServices)

local Constants = require(Modules.LuaApp.Constants)
local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)

local TopBar = require(Modules.LuaApp.Components.TopBar)
local RefreshScrollingFrame = require(Modules.LuaApp.Components.RefreshScrollingFrame)
local ApiFetchGamesData = require(Modules.LuaApp.Thunks.ApiFetchGamesData)
local GameCarousels = require(Modules.LuaApp.Components.GameCarousels)
local TokenRefreshComponent = require(Modules.LuaApp.Components.TokenRefreshComponent)
local LoadingBar = require(Modules.LuaApp.Components.LoadingBar)

local GamesHub = Roact.PureComponent:extend("GamesHub")

function GamesHub:init()
	self.refresh = function()
		return self.props.refresh(self.props.networking)
	end
end

function GamesHub:render()
	local fetchedGamesPageData = self.props.gamesPageDataStatus == RetrievalStatus.Done
	local topBarHeight = self.props.topBarHeight
	local analytics = self.props.analytics

	return Roact.createElement("Frame", {
		Size = UDim2.new(1, 0, 1, 0),
		BorderSizePixel = 0,
	}, {
		TokenRefreshComponent = Roact.createElement(TokenRefreshComponent, {
			sortToRefresh = Constants.GameSortGroups.Games,
		}),
		TopBar = Roact.createElement(TopBar, {
			showBuyRobux = true,
			showNotifications = true,
			showSearch = true,
			ZIndex = 2,
		}),
		Loader = not fetchedGamesPageData and Roact.createElement("Frame", {
			BackgroundTransparency = 0,
			AnchorPoint = Vector2.new(0.5, 0.5),
			Position = UDim2.new(0.5, 0, 0.5, topBarHeight/2),
			Size = UDim2.new(1, 0, 1, -topBarHeight),
			BorderSizePixel = 0,
			BackgroundColor3 = Constants.Color.GRAY4,
		}, {
			LoadingIndicator = Roact.createElement(LoadingBar),
		}),
		Scroller = fetchedGamesPageData and Roact.createElement(RefreshScrollingFrame, {
			Position = UDim2.new(0, 0, 0, topBarHeight),
			Size = UDim2.new(1, 0, 1, -topBarHeight),
			BackgroundColor3 = Constants.Color.GRAY4,
			CanvasSize = UDim2.new(1, 0, 0, 0),
			refresh = self.refresh,
		}, {
			--[[
				Adding UIListLayout to go around the issue with FitChildren wrongly
				calculating when the AbsolutePosition of its only child is negative
			]]
			layout = Roact.createElement("UIListLayout"),
			GameCarousels = Roact.createElement(GameCarousels, {
				gameSortGroup = Constants.GameSortGroups.Games,
				analytics = analytics,
			}),
		}),
	})
end

GamesHub = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			topBarHeight = state.TopBar.topBarHeight,
			gamesPageDataStatus = state.Startup.GamesPageDataStatus,
		}
	end,
	function(dispatch)
		return {
			refresh = function(networking)
				return dispatch(ApiFetchGamesData(networking))
			end,
		}
	end
)(GamesHub)

return RoactServices.connect({
	networking = RoactNetworking,
	analytics = RoactAnalyticsGamesPage,
})(GamesHub)