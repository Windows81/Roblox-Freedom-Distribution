local CoreGui = game:GetService("CoreGui")
local Players = game:GetService("Players")
local LocalizationService = game:GetService("LocalizationService")
local RunService = game:GetService("RunService")
local Workspace = game:GetService("Workspace")
local UserInputService = game:GetService("UserInputService")
local NotificationService = game:GetService("NotificationService")
local GuiService = game:GetService("GuiService")

local Modules = CoreGui.RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local Rodux = require(Modules.Common.Rodux)
local RoactRodux = require(Modules.Common.RoactRodux)
local ExternalEventConnection = require(Modules.Common.RoactUtilities.ExternalEventConnection)

local Promise = require(Modules.LuaApp.Promise)
local Localization = require(Modules.LuaApp.Localization)
local RoactServices = require(Modules.LuaApp.RoactServices)
local RoactAnalytics = require(Modules.LuaApp.Services.RoactAnalytics)
local RoactLocalization = require(Modules.LuaApp.Services.RoactLocalization)
local RoactNetworking = require(Modules.LuaApp.Services.RoactNetworking)
local AppNotificationService = require(Modules.LuaApp.Services.AppNotificationService)
local AppGuiService = require(Modules.LuaApp.Services.AppGuiService)
local FlagSettings = require(Modules.LuaApp.FlagSettings)
local AppPage = require(Modules.LuaApp.AppPage)

local AppRouter = require(Modules.LuaApp.Components.AppRouter)
local ScreenGuiWrap = require(Modules.LuaApp.Components.ScreenGuiWrap)
local HomePage = require(Modules.LuaApp.Components.Home.HomePage)
local GamesHub = require(Modules.LuaApp.Components.Games.GamesHub)
local GamesList = require(Modules.LuaApp.Components.Games.GamesList)
local SearchPage = require(Modules.LuaApp.Components.Search.SearchPage)
local RoactAvatarEditorWrapper = require(Modules.LuaApp.Components.Avatar.RoactAvatarEditorWrapper)
local RoactChatWrapper = require(Modules.LuaApp.Components.Chat.RoactChatWrapper)
local RoactDummyPageWrap = require(Modules.LuaApp.Components.RoactDummyPageWrap)
local RoactGameShareWrapper = require(Modules.LuaApp.Components.Chat.RoactGameShareWrapper)
local MorePage = require(Modules.LuaApp.Components.More.MorePage)
local BadgeEventReceiver = require(Modules.LuaApp.Components.EventReceivers.BadgeEventReceiver)
local NavigationEventReceiver = require(Modules.LuaApp.Components.EventReceivers.NavigationEventReceiver)

local AppReducer = require(Modules.LuaApp.AppReducer)

local RobloxEventReceiver = require(Modules.LuaApp.RobloxEventReceiver)

local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)
local Constants = require(Modules.LuaApp.Constants)
local SetFormFactor = require(Modules.LuaApp.Actions.SetFormFactor)
local SetPlatform = require(Modules.LuaApp.Actions.SetPlatform)
local DeviceOrientationMode = require(Modules.LuaApp.DeviceOrientationMode)
local SetDeviceOrientation = require(Modules.LuaApp.Actions.SetDeviceOrientation)
local SetLocalUserId = require(Modules.LuaApp.Actions.SetLocalUserId)
local SetHomePageDataStatus = require(Modules.LuaApp.Actions.SetHomePageDataStatus)
local SetScreenSize = require(Modules.LuaApp.Actions.SetScreenSize)
local SetUserMembershipType = require(Modules.LuaApp.Actions.SetUserMembershipType)
local AddUser = require(Modules.LuaApp.Actions.AddUser)
local ApiFetchUsersThumbnail = require(Modules.LuaApp.Thunks.ApiFetchUsersThumbnail)
local Analytics = require(Modules.Common.Analytics)
local request = require(Modules.LuaApp.Http.request)
local ApiFetchSortTokens = require(Modules.LuaApp.Thunks.ApiFetchSortTokens)
local ApiFetchGamesData = require(Modules.LuaApp.Thunks.ApiFetchGamesData)
local ApiFetchUsersFriends = require(Modules.LuaApp.Thunks.ApiFetchUsersFriends)
local BottomBar = require(Modules.LuaApp.Components.BottomBar)
local UserModel = require(Modules.LuaApp.Models.User)
local FormFactor = require(Modules.LuaApp.Enum.FormFactor)
local ApiFetchUnreadNotificationCount = require(Modules.LuaApp.Thunks.ApiFetchUnreadNotificationCount)
local FetchGamesPageData = require(Modules.LuaApp.Thunks.FetchGamesPageData)

local ChatMaster = require(Modules.ChatMaster)

-- flag dependencies
local luaAppLegacyInputDisabledGlobally = settings():GetFFlag('LuaAppLegacyInputDisabledGlobally2')

local function getDevicePlatform()
	if _G.__TESTEZ_RUNNING_TEST__ then
		return Enum.Platform.None
	end

	return UserInputService:GetPlatform()
end

local App = Roact.Component:extend("App")

function App:init()
	self.state = {
		store = Rodux.Store.new(AppReducer)
	}

	self._analytics = Analytics.new()
	self._networkRequest = request
	self._localization = Localization.new(LocalizationService.RobloxLocaleId)
	self._robloxEventReceiver = RobloxEventReceiver.new(NotificationService)

	self.updateLocalization = function(newLocale)
		self._localization:SetLocale(newLocale)
	end

	self._chatMaster = ChatMaster.new(self.state.store)

	local function wrapPageInScreenGui(component, pageType, visible, props)
		return Roact.createElement(ScreenGuiWrap, {
			component = component,
			pageType = pageType,
			isVisible = visible,
			props = props,
		})
	end

	self.pageConstructors = {
		[AppPage.None] = function()
			return nil
		end,
		[AppPage.Home] = function(visible)
			if FlagSettings.IsLuaHomePageEnabled(getDevicePlatform()) then
				return wrapPageInScreenGui(HomePage, AppPage.Home, visible)
			end
			return nil
		end,
		[AppPage.Games] = function(visible)
			if FlagSettings.IsLuaGamesPageEnabled(getDevicePlatform()) then
				return wrapPageInScreenGui(GamesHub, AppPage.Games, visible)
			end
			return nil
		end,
		[AppPage.GamesList] = function(visible, detail)
			return wrapPageInScreenGui(GamesList, AppPage.GamesList, visible, { sortName = detail })
		end,
		[AppPage.SearchPage] = function(visible, detail)
			local parameters = detail and { searchUuid = detail } or nil
			return wrapPageInScreenGui(SearchPage, AppPage.SearchPage, visible, parameters)
		end,
		[AppPage.AvatarEditor] = function(visible)
			return Roact.createElement(RoactAvatarEditorWrapper, {
				isVisible = visible,
			})
		end,
		[AppPage.Chat] = function(visible, detail)
			return Roact.createElement(RoactChatWrapper, {
				chatMaster = self._chatMaster,
				isVisible = visible,
				pageType = AppPage.Chat,
				parameters = detail and { conversationId = detail } or nil
			})
		end,
		[AppPage.ShareGameToChat] = function(visible, detail)
			local parameters = {
				chatMaster = self._chatMaster,
			}
			if detail then
				parameters.placeId = detail
			end
			return wrapPageInScreenGui(RoactGameShareWrapper, AppPage.ShareGameToChat, visible, parameters)
		end,
		[AppPage.Catalog] = function(visible)
			return Roact.createElement(RoactDummyPageWrap, {
				isVisible = visible,
				pageType = "Catalog",
			})
		end,
		[AppPage.Friends] = function(visible)
			return Roact.createElement(RoactDummyPageWrap, {
				isVisible = visible,
				pageType = "Friends",
			})
		end,
		[AppPage.More] = function(visible)
			return wrapPageInScreenGui(MorePage, AppPage.More, visible)
		end,
	}

	self.alwaysRenderedPages = {
		{ name = AppPage.Home },
		{ name = AppPage.Games },
		{ name = AppPage.AvatarEditor },
		{ name = AppPage.Chat },
	}

	self.updateDeviceOrientation = function(viewportSize)
		local deviceOrientation = viewportSize.x > viewportSize.y and
			DeviceOrientationMode.Landscape or DeviceOrientationMode.Portrait

		if self._deviceOrientation ~= deviceOrientation then
			self._deviceOrientation = deviceOrientation
			self.state.store:dispatch(SetDeviceOrientation(self._deviceOrientation))
		end
	end

	self.updateDeviceFormFactor = function(viewportSize)
		local formFactor = FormFactor.TABLET

		if viewportSize.Y > viewportSize.X then
			formFactor = FormFactor.PHONE
		end

		self.state.store:dispatch(SetFormFactor(formFactor))
	end

	self.updateViewport = function()
		local viewportSize = Workspace.CurrentCamera.ViewportSize

		-- Hacky code awaits underlying mechanism fix.
		-- Viewport will get a 0,0,1,1 rect before it is properly set.
		if viewportSize.X > 1 and viewportSize.Y > 1 then
			self.state.store:dispatch(SetScreenSize(viewportSize))
			self.updateDeviceOrientation(viewportSize)

			if FlagSettings.IsLuaAppDeterminingFormFactorAndPlatform() then
				self.updateDeviceFormFactor(viewportSize)
			end
		end
	end

	self.updateLocalPlayerMembership = function()
		local localPlayer = Players.LocalPlayer
		local userId = tostring(localPlayer.UserId)

		self.state.store:dispatch(SetUserMembershipType(userId, localPlayer.MembershipType))
	end

	self.updateDevicePlatform = function()
		-- Have to filter this to handle studio testing plugin which runs in a
		-- downgraded security context
		local platform = getDevicePlatform()
		self.state.store:dispatch(SetPlatform(platform))
	end

	self.onClose = function()
		-- there is currently a bug with the EventStream, where the stream is not released
		-- by the game engine. This call is a temporary work around until a new api is available.
		self._analytics.EventStream:releaseRBXEventStream()
	end

	-- the BindToClose function does not play nicely with Studio.
	if not RunService:IsStudio() then
		game:BindToClose(self.onClose)
	end

	if FlagSettings.IsLuaAppDeterminingFormFactorAndPlatform() then
		self.updateDevicePlatform()
	end
end

function App:didMount()
	local platform = self.state.store:getState().Platform

	RunService:setThrottleFramerateEnabled(true)
	UserInputService.LegacyInputEventsEnabled = (not luaAppLegacyInputDisabledGlobally)

	-- Set the device orientation for the 1st time
	-- TODO: this should be put in a seperate file.
	self.updateViewport()

	-- Add the local player info to the store for the 1st time
	-- TODO: this should be put in a seperate file.
	local localPlayer = Players.LocalPlayer
	local userId = tostring(localPlayer.UserId)

	self.state.store:dispatch(AddUser(UserModel.fromData(userId, localPlayer.Name, false)))
	self.state.store:dispatch(ApiFetchUsersThumbnail(
		self._networkRequest, {userId}, Constants.AvatarThumbnailRequests.HOME_HEADER_USER
	))
	self.state.store:dispatch(SetLocalUserId(userId))
	self.updateLocalPlayerMembership()

	self.state.store:dispatch(ApiFetchUnreadNotificationCount(self._networkRequest))

	-- start loading information for Home Page
	if FlagSettings.IsLuaHomePageEnabled(platform) then

		self.state.store:dispatch(SetHomePageDataStatus(RetrievalStatus.Fetching))
		Promise.all({
			self.state.store:dispatch(ApiFetchUsersFriends(
				self._networkRequest, userId, Constants.AvatarThumbnailRequests.USER_CAROUSEL
			)),
			self.state.store:dispatch(ApiFetchSortTokens(self._networkRequest, Constants.GameSortGroups.HomeGames)
			):andThen(
				function(result)
					return self.state.store:dispatch(ApiFetchGamesData(self._networkRequest, Constants.GameSortGroups.HomeGames))
				end
			),
		}):andThen(
			function()
				self.state.store:dispatch(SetHomePageDataStatus(RetrievalStatus.Done))

				-- start loading information for the Games Page
				local status = self.state.store:getState().Startup.GamesPageDataStatus
				if FlagSettings.IsLuaGamesPageEnabled(platform) and status == RetrievalStatus.NotStarted then
					self.state.store:dispatch(FetchGamesPageData(self._networkRequest, self._analytics))
				end
			end
		)
	end
end

function App:render()
	return Roact.createElement(RoactRodux.StoreProvider, {
		store = self.state.store,
	}, {
		services = Roact.createElement(RoactServices.ServiceProvider, {
			services = {
				[RoactAnalytics] = self._analytics,
				[RoactLocalization] = self._localization,
				[RoactNetworking] = self._networkRequest,
				[AppNotificationService] = NotificationService,
				[AppGuiService] = GuiService,
			}
		}, {
			PageWrapper = Roact.createElement("Folder", {}, {
				NavigationEventReceiver = Roact.createElement(NavigationEventReceiver,{
					RobloxEventReceiver = self._robloxEventReceiver,
				}),
				BadgeEventReceiver = Roact.createElement(BadgeEventReceiver, {
					RobloxEventReceiver = self._robloxEventReceiver,
				}),
				BottomBar = Roact.createElement(BottomBar, {
					displayOrder = 10,
				}),
				AppRouter = Roact.createElement(AppRouter, {
					pageConstructors = self.pageConstructors,
					alwaysRenderedPages = self.alwaysRenderedPages,
				}),
				localizationListener = Roact.createElement(ExternalEventConnection, {
					event = LocalizationService:GetPropertyChangedSignal("RobloxLocaleId"),
					callback = self.updateLocalization,
				}),
				viewportSizeListener = Roact.createElement(ExternalEventConnection, {
					event = Workspace.CurrentCamera:GetPropertyChangedSignal("ViewportSize"),
					callback = self.updateViewport,
				}),
				playerMembershipListener = Roact.createElement(ExternalEventConnection, {
					event = Players.LocalPlayer:GetPropertyChangedSignal("MembershipType"),
					callback = self.updateLocalPlayerMembership,
				}),
			})
		}),
	})
end

function App:willUnmount()
	RunService:setThrottleFramerateEnabled(false)
	self._chatNotificationBroadcaster:Destruct()
end

return App