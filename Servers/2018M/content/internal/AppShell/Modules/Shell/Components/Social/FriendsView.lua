local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Roact = require(Modules.Common.Roact)
local memoize = require(Modules.Common.memoize)
local RoactRodux = require(Modules.Common.RoactRodux)
local CategoryMenuView = require(Modules.Shell.Components.Common.CategoryMenuView)
local SplitViewLR = require(Modules.Shell.Components.Common.SplitViewLR)
local Utility = require(Modules.Shell.Utility)
local SoundManager = require(Modules.Shell.SoundManager)
local Strings = require(Modules.Shell.LocalizedStrings)
local FriendsScrollingView = require(Modules.Shell.Components.Social.FriendsScrollingView)
local NoFriendsView = require(Modules.Shell.Components.Social.NoFriendsView)
local PageKeys = require(Modules.Shell.PageKeys)

local FriendsView = Roact.PureComponent:extend("FriendsView")

local MenuKey = PageKeys.FriendCategories.Key
local FriendCategoriesKeys = {
	OnlineFriends = PageKeys.FriendCategories.OnlineFriends.Key,
	AllFriends = PageKeys.FriendCategories.AllFriends.Key,
}
local FriendCategories = {}
FriendCategories[FriendCategoriesKeys.OnlineFriends] = { Order = 1, StringKey = "OnlineWord" }
FriendCategories[FriendCategoriesKeys.AllFriends] = { Order = 2, StringKey = "AllWord" }

local function onSelectSection(self, key)
	if self.state.currentPage ~= key then
		self:setState({
			currentPage = key,
			selectedPage = MenuKey,
		})
	end
end

function FriendsView:init()
	self.selectedPage = MenuKey
	self.onSelectionGained = function(key)
		onSelectSection(self,key)
	end

	self.state = {
		currentPage = FriendCategoriesKeys.OnlineFriends,
		selectedPage = MenuKey,
	}

	self.enterSection = function()
		SoundManager:Play("OverlayOpen")
		Utility.SetSelectedCoreObject(nil)
		self:setState({
			selectedPage = self.state.currentPage,
		})
	end
	self.exitSection = function()
		SoundManager:Play("PopUp")
		self:setState({
			selectedPage = MenuKey,
		})
	end
end

function FriendsView:render()
	local actionPriority = self.props.actionPriority or 0
	local currentPage = self.state.currentPage
	local friendsViewInFocus = self.props.inFocus
	local friendsViewHide = self.props.hide
	local friendCategoriesMenuInFocus = false
	local friendPagesInFocus = false
	if not friendsViewHide and friendsViewInFocus then
		if self.state.selectedPage == MenuKey then
			friendCategoriesMenuInFocus = true
		end
		if self.state.selectedPage ~= MenuKey then
			friendPagesInFocus = true
		end
	end

	local enterSection = self.enterSection
	if currentPage == PageKeys.FriendCategories.OnlineFriends.Key and #self.props.onlineFriendsData == 0 then
		enterSection = nil
	elseif currentPage == PageKeys.FriendCategories.AllFriends.Key and #self.props.allFriendsData == 0 then
		enterSection = nil
	end

	return Roact.createElement("Frame", {
		Size = UDim2.new(1, -58, 1, 0),
		Position = UDim2.new(0, 58, 0, 0),
		BackgroundTransparency = 1,
	},{
		Mainview = Roact.createElement(SplitViewLR, {
			Bias = 0.265,
			LeftView = Roact.createElement(CategoryMenuView, {
				Key = MenuKey,
				Categories = FriendCategories,
				InFocus = friendCategoriesMenuInFocus,
				DefaultCategoryFocus = FriendCategoriesKeys.OnlineFriends,
				OnSelectSection = self.onSelectionGained,
				EnterSection = enterSection,
				RedirectUp = self.props.redirectUp,
				ActionPriority = actionPriority,
			}),
			RightView = Roact.createElement("Frame", {
				Size = UDim2.new(1, 0, 1, 0),
				BackgroundTransparency = 1,
			},{
				OnlineFriendsView = Roact.createElement(FriendsScrollingView, {
					friendsData = self.props.onlineFriendsData,
					initialized = self.props.initialized,
					hide = currentPage ~= PageKeys.FriendCategories.OnlineFriends.Key,
					inFocus = friendPagesInFocus,
					redirectLeft = self.exitSection,
					redirectBack = self.exitSection,
					redirectUp = self.props.redirectUp,
					redirectRight = self.props.redirectRight,
					size = UDim2.new(0, 440, 0, 770),
					noFriendsView = Roact.createElement(NoFriendsView, {
						text = Strings:LocalizedString("NoFriendsOnlinePhrase"),
					}),
					actionPriority = actionPriority + 1,
				}),
				AllFriendsView = Roact.createElement(FriendsScrollingView, {
					friendsData = self.props.allFriendsData,
					initialized = self.props.initialized,
					hide = currentPage ~= PageKeys.FriendCategories.AllFriends.Key,
					inFocus = friendPagesInFocus,
					redirectLeft = self.exitSection,
					redirectBack = self.exitSection,
					redirectUp = self.props.redirectUp,
					redirectRight = self.props.redirectRight,
					size = UDim2.new(0, 440, 0, 770),
					noFriendsView = Roact.createElement(NoFriendsView, {
						text = Strings:LocalizedString("PlayAndMakeFriendsPhrase"),
					}),
					actionPriority = actionPriority + 1,
				}),
			}),
		}),
	})
end

local filterOnlineFriends = memoize(function(friendsData)
	local onlineFriendsData = {}
	for _, data in ipairs(friendsData) do
		if data.robloxStatus ~= "Offline" or data.xboxStatus == "Online" then
			table.insert(onlineFriendsData, data)
		end
	end
	return onlineFriendsData
end)

local function mapStateToProps(state, props)
	local friendsData = state.RenderedFriends.data
	return {
		allFriendsData = friendsData,
		onlineFriendsData = filterOnlineFriends(friendsData),
		initialized = state.RenderedFriends.initialized
	}
end

return RoactRodux.UNSTABLE_connect2(mapStateToProps)(FriendsView)