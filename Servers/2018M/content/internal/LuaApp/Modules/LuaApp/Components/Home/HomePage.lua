local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Common = Modules.Common
local LuaApp = Modules.LuaApp

local Roact = require(Common.Roact)
local RoactRodux = require(Common.RoactRodux)
local RoactAnalyticsHomePage = require(Modules.LuaApp.Services.RoactAnalyticsHomePage)
local RoactNetworking = require(Modules.LuaApp.Services.RoactNetworking)
local AppGuiService = require(Modules.LuaApp.Services.AppGuiService)
local RoactServices = require(Modules.LuaApp.RoactServices)

local Promise = require(Modules.LuaApp.Promise)
local RefreshScrollingFrame = require(Modules.LuaApp.Components.RefreshScrollingFrame)
local UserCarouselEntry = require(LuaApp.Components.Home.UserCarouselEntry)
local HomeHeaderUserInfo = require(LuaApp.Components.Home.HomeHeaderUserInfo)
local MyFeedButton = require(LuaApp.Components.Home.MyFeedButton)
local DropshadowFrame = require(LuaApp.Components.DropshadowFrame)
local Carousel = require(LuaApp.Components.Carousel)
local TopBar = require(LuaApp.Components.TopBar)
local GameCarousels = require(LuaApp.Components.GameCarousels)
local LoadingBar = require(LuaApp.Components.LoadingBar)
local HomeFTUEGameGrid = require(LuaApp.Components.Home.HomeFTUEGameGrid)
local LocalizedSectionHeaderWithSeeAll = require(Modules.LuaApp.Components.LocalizedSectionHeaderWithSeeAll)
local User = require(LuaApp.Models.User)
local Constants = require(LuaApp.Constants)
local FitChildren = require(LuaApp.FitChildren)
local Functional = require(Common.Functional)
local Immutable = require(Common.Immutable)
local memoize = require(Common.memoize)
local TokenRefreshComponent = require(Modules.LuaApp.Components.TokenRefreshComponent)
local NotificationType = require(LuaApp.Enum.NotificationType)

local Url = require(Modules.LuaApp.Http.Url)
local ApiFetchGamesData = require(Modules.LuaApp.Thunks.ApiFetchGamesData)
local ApiFetchUsersFriends = require(Modules.LuaApp.Thunks.ApiFetchUsersFriends)
local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)

local MAX_FRIENDS_IN_CAROUSEL = tonumber(settings():GetFVariable("LuaHomeMaxFriends")) or 0

local SIDE_PADDING = 15
local SECTION_PADDING = 15
local CAROUSEL_PADDING = Constants.GAME_CAROUSEL_PADDING
local CAROUSEL_PADDING_DIM = UDim.new(0, CAROUSEL_PADDING)

local FRIEND_SECTION_MARGIN = 15 - UserCarouselEntry.horizontalPadding()

local FEED_SECTION_PADDING = 60
local FEED_SECTION_PADDING_TOP = FEED_SECTION_PADDING - CAROUSEL_PADDING
local FEED_SECTION_PADDING_BOTTOM = FEED_SECTION_PADDING
local FEED_BUTTON_HEIGHT = 32
local FEED_SECTION_HEIGHT = FEED_SECTION_PADDING_TOP + FEED_BUTTON_HEIGHT + FEED_SECTION_PADDING_BOTTOM

local PRESENCE_WEIGHTS = {
	[User.PresenceType.IN_GAME] = 3,
	[User.PresenceType.ONLINE] = 2,
	[User.PresenceType.IN_STUDIO] = 1,
	[User.PresenceType.OFFLINE] = 0,
}

local function Spacer(props)
	local height = props.height
	local layoutOrder = props.LayoutOrder

	return Roact.createElement("Frame", {
		Size = UDim2.new(1, 0, 0, height),
		BackgroundTransparency = 1,
		LayoutOrder = layoutOrder,
	})
end


local HomePage = Roact.PureComponent:extend("HomePage")

function HomePage:init()
	self.refresh = function()
		return self.props.refresh(self.props.networking, self.props.localUserModel)
	end

	self.onSeeAllFriends = function()
		local url = string.format("%susers/friends", Url.BASE_URL)
		self.props.guiService:BroadcastNotification(url, NotificationType.VIEW_PROFILE)
	end
end

function HomePage:render()
	local fetchedHomePageData = self.props.homePageDataStatus == RetrievalStatus.Done
	local topBarHeight = self.props.topBarHeight
	local friends = self.props.friends
	local localUserModel = self.props.localUserModel
	local formFactor = self.props.formFactor
	local friendCount = self.props.friendCount
	local isFTUE = self.props.isFTUE
	local analytics = self.props.analytics

	local hasFriends = #friends > 0
	local friendSectionHeight = UserCarouselEntry.height(formFactor)

	local function createUserEntry(user, count)
		return Roact.createElement(UserCarouselEntry, {
			user = user,
			formFactor = formFactor,
			count = count,
			highlightColor = Constants.Color.WHITE,
			thumbnailType = Constants.AvatarThumbnailTypes.AvatarThumbnail,
		})
	end

	return Roact.createElement("Frame", {
		Size = UDim2.new(1, 0, 1, 0),
		BorderSizePixel = 0,
	}, {
		TokenRefreshComponent = Roact.createElement(TokenRefreshComponent, {
			sortToRefresh = Constants.GameSortGroups.HomeGames,
		}),
		TopBar = Roact.createElement(TopBar, {
			showBuyRobux = true,
			showNotifications = true,
			showSearch = true,
			ZIndex = 2,
		}),
		Loader = not fetchedHomePageData and Roact.createElement("Frame", {
			BackgroundTransparency = 0,
			AnchorPoint = Vector2.new(0.5, 0.5),
			Position = UDim2.new(0.5, 0, 0.5, topBarHeight/2),
			Size = UDim2.new(1, 0, 1, -topBarHeight),
			BorderSizePixel = 0,
			BackgroundColor3 = Constants.Color.GRAY4,
		}, {
			LoadingIndicator = Roact.createElement(LoadingBar),
		}),
		Scroller = fetchedHomePageData and Roact.createElement(RefreshScrollingFrame, {
			Position = UDim2.new(0, 0, 0, topBarHeight),
			Size = UDim2.new(1, 0, 1, -topBarHeight),
			CanvasSize = UDim2.new(1, 0, 0, 0),
			BackgroundColor3 = Constants.Color.GRAY4,
			BorderSizePixel = 0,
			ScrollBarThickness = 0,
			refresh = self.refresh,
		}, {
			Layout = Roact.createElement("UIListLayout", {
				SortOrder = Enum.SortOrder.LayoutOrder,
			}),
			TitleSection = localUserModel and Roact.createElement(HomeHeaderUserInfo, {
				sidePadding = SIDE_PADDING,
				sectionPadding = SECTION_PADDING,
				LayoutOrder = 2,
				localUserModel = localUserModel,
				formFactor = formFactor,
			}),
			FriendSection = hasFriends and Roact.createElement(FitChildren.FitFrame, {
				Size = UDim2.new(1, 0, 0, 0),
				fitAxis = FitChildren.FitAxis.Height,
				BackgroundTransparency = 1,
				LayoutOrder = 4,
			}, {
				Layout = Roact.createElement("UIListLayout", {
					SortOrder = Enum.SortOrder.LayoutOrder,
				}),
				Container = Roact.createElement(FitChildren.FitFrame, {
					Size = UDim2.new(1, 0, 0, 0),
					BackgroundTransparency = 1,
					fitFields = {
						Size = FitChildren.FitAxis.Height,
					},
				}, {
					SidePadding = Roact.createElement("UIPadding", {
						PaddingLeft = CAROUSEL_PADDING_DIM,
						PaddingRight = CAROUSEL_PADDING_DIM,
					}),
					Header = Roact.createElement(LocalizedSectionHeaderWithSeeAll, {
						text = {
							"Feature.Home.HeadingFriends",
							friendCount = friendCount,
						},
						LayoutOrder = 1,
						onSelected = self.onSeeAllFriends
					}),
				}),
				CarouselFrame = Roact.createElement(DropshadowFrame, {
					Size = UDim2.new(1, 0, 0, friendSectionHeight),
					BackgroundColor3 = Constants.Color.WHITE,
					LayoutOrder = 2,
				}, {
					Carousel = Roact.createElement(Carousel, {
						childPadding = 0,
					}, Immutable.JoinDictionaries(Functional.Map(friends, createUserEntry), {
						leftAlignSpacer = Roact.createElement("UIPadding", {
							PaddingRight = UDim.new(0, FRIEND_SECTION_MARGIN),
							PaddingLeft = UDim.new(0, FRIEND_SECTION_MARGIN),
						})
					}))
				}),
			}),
			GameDisplay = isFTUE and Roact.createElement(HomeFTUEGameGrid, {
				LayoutOrder = 5,
				analytics = analytics,
				hasTopPadding = hasFriends,
			}) or Roact.createElement(GameCarousels, {
				gameSortGroup = Constants.GameSortGroups.HomeGames,
				LayoutOrder = 5,
				analytics = analytics,
			}),
			FeedSection = Roact.createElement("Frame", {
				Size = UDim2.new(1, 0, 0, FEED_SECTION_HEIGHT),
				BackgroundTransparency = 1,
				LayoutOrder = 6,
			}, {
				Layout = Roact.createElement("UIListLayout", {
					SortOrder = Enum.SortOrder.LayoutOrder,
				}),
				MyFeedPadding1 = Roact.createElement(Spacer, {
					height = FEED_SECTION_PADDING_TOP,
					LayoutOrder = 1,
				}),
				MyFeedButton = Roact.createElement(MyFeedButton, {
					Size = UDim2.new(1, 0, 0, FEED_BUTTON_HEIGHT),
					LayoutOrder = 2,
				}),
				MyFeedPadding2 = Roact.createElement(Spacer, {
					height = FEED_SECTION_PADDING_BOTTOM,
					LayoutOrder = 3,
				}),
			}),
		}),
	})
end

local selectFriends = memoize(function(users)
	local allFriends = {}
	local function friendPreference(friend1, friend2)
		local friend1Weight = PRESENCE_WEIGHTS[friend1.presence]
		local friend2Weight = PRESENCE_WEIGHTS[friend2.presence]

		if friend1Weight == friend2Weight then
			return friend1.name < friend2.name
		else
			return friend1Weight > friend2Weight
		end
	end

	for _, user in pairs(users) do
		if user.isFriend then
			allFriends[#allFriends + 1] = user
		end
	end

	table.sort(allFriends, friendPreference)

	local filteredFriends = {}
	for index, user in ipairs(allFriends) do
		filteredFriends[index] = user
		if index >= MAX_FRIENDS_IN_CAROUSEL then
			break
		end
	end

	return filteredFriends
end)

local selectLocalUser = memoize(function(users, id)
	return users[id]
end)

local selectIsFTUE = function(sortGroups)
	local homeSortGroup = Constants.GameSortGroups.HomeGames
	local sorts = sortGroups[homeSortGroup].sorts

	return #sorts == 1
end

HomePage = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			friends = selectFriends(
				state.Users
			),
			localUserModel = selectLocalUser(state.Users, state.LocalUserId),
			isFTUE = selectIsFTUE(state.GameSortGroups),
			formFactor = state.FormFactor,
			friendCount = state.FriendCount,
			topBarHeight = state.TopBar.topBarHeight,
			homePageDataStatus = state.Startup.HomePageDataStatus,
		}
	end,
	function(dispatch)
		return {
			refresh = function(networking, localUserModel)
				local fetchPromises = {}
				table.insert(fetchPromises, dispatch(ApiFetchUsersFriends(
					networking,
					localUserModel.id,
					Constants.AvatarThumbnailRequests.USER_CAROUSEL
				)))
				table.insert(fetchPromises, dispatch(ApiFetchGamesData(networking, Constants.GameSortGroups.HomeGames)))
				return Promise.all(fetchPromises)
			end,
		}
	end
)(HomePage)

return RoactServices.connect({
	networking = RoactNetworking,
	analytics = RoactAnalyticsHomePage,
	guiService = AppGuiService
})(HomePage)