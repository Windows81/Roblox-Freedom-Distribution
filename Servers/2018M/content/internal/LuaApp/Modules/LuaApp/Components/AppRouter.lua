local CoreGui = game:GetService("CoreGui")
local Modules = CoreGui.RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local RoactServices = require(Modules.LuaApp.RoactServices)
local RoactNetworking = require(Modules.LuaApp.Services.RoactNetworking)
local RoactAnalytics = require(Modules.LuaApp.Services.RoactAnalytics)
local AppNotificationService = require(Modules.LuaApp.Services.AppNotificationService)

local AppPage = require(Modules.LuaApp.AppPage)
local RouterAnalyticsReporter = require(Modules.LuaApp.Components.Analytics.RouterAnalyticsReporter)
local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)
local FetchGamesPageData = require(Modules.LuaApp.Thunks.FetchGamesPageData)

local FlagSettings = require(Modules.LuaApp.FlagSettings)

local AppRouter = Roact.PureComponent:extend("AppRouter")

AppRouter.defaultProps = {
	alwaysRenderedPages = {},
}

local function getPageName(page)
	return page.detail and (page.name .. ":" .. page.detail) or page.name
end

function AppRouter:render()
	local routeHistory = self.props.routeHistory
	local pageConstructors = self.props.pageConstructors
	local alwaysRenderedPages = self.props.alwaysRenderedPages

	local currentRoute = routeHistory[#routeHistory]
	local currentPage = currentRoute[#currentRoute].name
	local pages = {
		RouterAnalyticsReporter = Roact.createElement(RouterAnalyticsReporter, {
			currentPage = currentPage,
		}),
	}

	for index = #routeHistory, 1, -1 do
		local route = routeHistory[index]
		local pageInfo = route[#route]
		local pageName = getPageName(pageInfo)
		local isVisible = index == #routeHistory
		if not pages[pageName] then
			pages[pageName] = pageConstructors[pageInfo.name](isVisible, pageInfo.detail)
		end
	end

	for index = 1, #alwaysRenderedPages do
		local pageInfo = alwaysRenderedPages[index]
		local pageName = getPageName(pageInfo)
		if not pages[pageName] then
			pages[pageName] = pageConstructors[pageInfo.name](false, pageInfo.detail)
		end
	end

	return Roact.createElement("Folder", {}, pages)
end

function AppRouter:didUpdate(prevProps, prevState)
	local notificationService = self.props.NotificationService
	local newRouteHistory = self.props.routeHistory
	local newRoute = newRouteHistory[#newRouteHistory]
	local newPage = newRoute[#newRoute]

	local oldRouteHistory = prevProps.routeHistory
	local oldRoute = oldRouteHistory[#oldRouteHistory]
	local oldPage = oldRoute[#oldRoute]

	local UseLuaGamesPage = FlagSettings.IsLuaGamesPageEnabled(self.props.platform)

	if UseLuaGamesPage and newPage.name == AppPage.Games
		and self.props.gamesPageDataStatus == RetrievalStatus.NotStarted then
		self.props.loadGamesPage(RoactNetworking.get(self._context), RoactAnalytics.get(self._context))
	end

	local fetchedGames = newPage.name == AppPage.Games
		and self.props.gamesPageDataStatus == RetrievalStatus.Done
	local oldFetchedGames = oldPage.name == AppPage.Games
		and prevProps.gamesPageDataStatus == RetrievalStatus.Done
	if fetchedGames and not oldFetchedGames then
		notificationService:ActionEnabled(Enum.AppShellActionType.GamePageLoaded)
	end

	local fetchedHome = newPage.name == AppPage.Home
		and self.props.homePageDataStatus == RetrievalStatus.Done
	local oldFetchedHome = oldPage.name == AppPage.Home
		and prevProps.homePageDataStatus == RetrievalStatus.Done
	if fetchedHome and not oldFetchedHome then
		notificationService:ActionEnabled(Enum.AppShellActionType.HomePageLoaded)
	end
end

AppRouter = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			routeHistory = state.Navigation.history,
			gamesPageDataStatus = state.Startup.GamesPageDataStatus,
			homePageDataStatus = state.Startup.HomePageDataStatus,
			platform = state.Platform,
		}
	end,
	function(dispatch)
		return {
			loadGamesPage = function(networking, analytics)
				return dispatch(FetchGamesPageData(networking, analytics))
			end,
		}
	end
)(AppRouter)

return RoactServices.connect({
	NotificationService = AppNotificationService,
})(AppRouter)