local CoreGui = game:GetService("CoreGui")
local UserInputService = game:GetService("UserInputService")

local Modules = CoreGui.RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local ExternalEventConnection = require(Modules.Common.RoactUtilities.ExternalEventConnection)

local Constants = require(Modules.LuaApp.Constants)
local AppPage = require(Modules.LuaApp.AppPage)
local DeviceOrientationMode = require(Modules.LuaApp.DeviceOrientationMode)
local FlagSettings = require(Modules.LuaApp.FlagSettings)
local getScreenBottomInset = require(Modules.LuaApp.getScreenBottomInset)
local NotificationType = require(Modules.LuaApp.Enum.NotificationType)

local BottomBarButton = require(Modules.LuaApp.Components.BottomBarButton)

local AppGuiService = require(Modules.LuaApp.Services.AppGuiService)
local RoactServices = require(Modules.LuaApp.RoactServices)

local UseLuaBottomBar = FlagSettings.IsLuaBottomBarEnabled()

local HomeButtonDefaultImage = "rbxasset://textures/ui/LuaApp/icons/ic-home.png"
local GamesButtonDefaultImage = "rbxasset://textures/ui/LuaApp/icons/ic-games.png"
local CatalogButtonDefaultImage = "rbxasset://textures/ui/LuaApp/icons/ic-catalog.png"
local AvatarButtonDefaultImage = "rbxasset://textures/ui/LuaApp/icons/ic-avatar.png"
local FriendsButtonDefaultImage = "rbxasset://textures/ui/LuaApp/icons/ic-friend.png"
local ChatButtonDefaultImage = "rbxasset://textures/ui/LuaApp/icons/ic-chat.png"
local MoreButtonDefaultImage = "rbxasset://textures/ui/LuaApp/icons/ic-more.png"

local HomeButtonSelectedImage = "rbxasset://textures/ui/LuaApp/icons/ic-home-on.png"
local GamesButtonSelectedImage = "rbxasset://textures/ui/LuaApp/icons/ic-games-on.png"
local CatalogButtonSelectedImage = "rbxasset://textures/ui/LuaApp/icons/ic-catalog-on.png"
local AvatarButtonSelectedImage = "rbxasset://textures/ui/LuaApp/icons/ic-avatar-on.png"
local FriendsButtonSelectedImage = "rbxasset://textures/ui/LuaApp/icons/ic-friend-on.png"
local ChatButtonSelectedImage = "rbxasset://textures/ui/LuaApp/icons/ic-chat-on.png"
local MoreButtonSelectedImage = "rbxasset://textures/ui/LuaApp/icons/ic-more-on.png"

local BottomBar = Roact.PureComponent:extend("BottomBar")

function BottomBar:init()
	-- Android device might still have BottomBarSize when we HIDE_TAB_BAR
	-- Which is for system virtual navigation bar
	-- BottomBarSize might change while app is running depending on the device
	-- iOS device should fall back to safeZoneOffsets.bottom when we HIDE_TAB_BAR
	self.updateGlobalGuiInset = function()
		self.props.guiService:SetGlobalGuiInset(0, 0, 0, self.luaBottomBarSize + getScreenBottomInset())
	end
end

function BottomBar:render()
	local deviceOrientation = self.props.deviceOrientation
	local bottomBarVisible = self.props.bottomBarVisible
	local displayOrder = self.props.displayOrder
	local guiService = self.props.guiService
	local isLandscape = deviceOrientation == DeviceOrientationMode.Landscape

	local bottomBarSizeListener = (not _G.__TESTEZ_RUNNING_TEST__) and Roact.createElement(ExternalEventConnection, {
		event = UserInputService:GetPropertyChangedSignal("BottomBarSize"),
		callback = self.updateGlobalGuiInset,
	})

	local safeZoneOffsetsListener = (not _G.__TESTEZ_RUNNING_TEST__) and Roact.createElement(ExternalEventConnection, {
		event = guiService.SafeZoneOffsetsChanged,
		callback = self.updateGlobalGuiInset,
	})

	if not bottomBarVisible or not UseLuaBottomBar then
		return Roact.createElement("Folder", {}, {
			bottomBarSizeListener,
			safeZoneOffsetsListener,
		})
	end

	local homeButton = Roact.createElement(BottomBarButton, {
		defaultImage = HomeButtonDefaultImage,
		selectedImage = HomeButtonSelectedImage,
		associatedPageType = AppPage.Home,
	})

	local gamesButton = Roact.createElement(BottomBarButton, {
		defaultImage = GamesButtonDefaultImage,
		selectedImage = GamesButtonSelectedImage,
		associatedPageType = AppPage.Games,
	})

	local catalogButton = Roact.createElement(BottomBarButton, {
		defaultImage = CatalogButtonDefaultImage,
		selectedImage = CatalogButtonSelectedImage,
		associatedPageType = AppPage.Catalog,
	})

	local avatarButton = Roact.createElement(BottomBarButton, {
		defaultImage = AvatarButtonDefaultImage,
		selectedImage = AvatarButtonSelectedImage,
		associatedPageType = AppPage.AvatarEditor,
	})

	local friendsButton = Roact.createElement(BottomBarButton, {
		defaultImage = FriendsButtonDefaultImage,
		selectedImage = FriendsButtonSelectedImage,
		associatedPageType = AppPage.Friends,
	})

	local chatButton = Roact.createElement(BottomBarButton, {
		defaultImage = ChatButtonDefaultImage,
		selectedImage = ChatButtonSelectedImage,
		associatedPageType = AppPage.Chat,
	})

	local moreButton = Roact.createElement(BottomBarButton, {
		defaultImage = MoreButtonDefaultImage,
		selectedImage = MoreButtonSelectedImage,
		associatedPageType = AppPage.More,
	})

	local uiListLayout = Roact.createElement("UIListLayout", {
		FillDirection = Enum.FillDirection.Horizontal,
		SortOrder = Enum.SortOrder.LayoutOrder,
	})

	local portraitButtons = {
		UIListLayout = uiListLayout,
		HomeButton = homeButton,
		GamesButton = gamesButton,
		AvatarButton = avatarButton,
		ChatButton = chatButton,
		MoreButton = moreButton,
	}

	local landscapeButtons = {
		UIListLayout = uiListLayout,
		HomeButton = homeButton,
		GamesButton = gamesButton,
		CatalogButton = catalogButton,
		AvatarButton = avatarButton,
		FriendsButton = friendsButton,
		ChatButton = chatButton,
		MoreButton = moreButton,
	}

	local children = isLandscape and landscapeButtons or portraitButtons

	return Roact.createElement(Roact.Portal, {
		target = CoreGui,
	}, {
		BottomBar = Roact.createElement("ScreenGui", {
			ZIndexBehavior = Enum.ZIndexBehavior.Sibling,
			DisplayOrder = displayOrder,
		}, {
			TopLine = Roact.createElement("Frame", {
				Position = UDim2.new(0, 0, 1, 0),
				Size = UDim2.new(1, 0, 0, 1),
				BorderSizePixel = 0,
				BackgroundTransparency = 0,
				BackgroundColor3 = Constants.Color.GRAY_SEPARATOR,
				ZIndex = 2,
			}),
			Contents = Roact.createElement("Frame", {
				Position = UDim2.new(0, 0, 1, 0),
				Size = UDim2.new(1, 0, 1, 0),
				BorderSizePixel = 0,
				BackgroundTransparency = 0,
				BackgroundColor3 = Constants.Color.WHITE,
				ZIndex = 1,
			}, {
				Frame = Roact.createElement("Frame", {
					AnchorPoint = Vector2.new(0.5, 0),
					Position = UDim2.new(0.5, 0, 0, 0),
					Size = UDim2.new(isLandscape and 0.92 or 1, 0, 0, Constants.BOTTOM_BAR_SIZE),
					BorderSizePixel = 0,
					BackgroundTransparency = 1,
				}, children)
			})
		}),
		bottomBarSizeListener,
		safeZoneOffsetsListener,
	})
end

function BottomBar:didMount()
	self:updateInset(self.props.bottomBarVisible)
end

function BottomBar:willUpdate(newProps)
	if (self.props.bottomBarVisible ~= newProps.bottomBarVisible) then
		self:updateInset(newProps.bottomBarVisible)
	end
end

function BottomBar:updateInset(visible)
	local guiService = self.props.guiService
	-- Setting the view size to consider bottom bar space.
	-- TODO Needs to be checked if this will be necessary after integrating Lua bottom bar.

	-- self.luaBottomBarSize is not a local variable because BottomBarSize changed signal callback isn't
	-- re-created each time, it could use the old upvalue if luaBottomBarSize is local variable.
	self.luaBottomBarSize = (UseLuaBottomBar and visible) and Constants.BOTTOM_BAR_SIZE or 0
	if UseLuaBottomBar then
		guiService:BroadcastNotification("", NotificationType.HIDE_TAB_BAR)
	end

	self.updateGlobalGuiInset()
end

BottomBar = RoactRodux.connect(function(store)
	local state = store:getState()
	return {
		deviceOrientation = state.DeviceOrientation,
		bottomBarVisible = state.TabBarVisible,
	}
end)(BottomBar)

return RoactServices.connect({
	guiService = AppGuiService
})(BottomBar)