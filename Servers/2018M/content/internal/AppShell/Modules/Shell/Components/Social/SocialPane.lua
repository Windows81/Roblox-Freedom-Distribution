local GuiService = game:GetService("GuiService")
local Modules = game:GetService("CoreGui").RobloxGui.Modules
local ShellModules = Modules:FindFirstChild("Shell")
local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local Strings = require(ShellModules:FindFirstChild("LocalizedStrings"))
local ScreenManager = require(ShellModules.ScreenManager)
local AppState = require(ShellModules.AppState)
local Analytics = require(ShellModules:FindFirstChild("Analytics"))
local Utility = require(ShellModules:FindFirstChild("Utility"))
local Components = ShellModules.Components
local FriendsView = require(Components.Social.FriendsView)
local FriendsData = require(ShellModules.FriendsData)

local function CreateSocialPane(parent)
	local this = {}
	local isPaneFocused = false
	local HubContainer = parent.Parent
	local UpSelector = HubContainer:FindFirstChild("TabContainer")

	local noSelectionObject = Utility.Create"ImageLabel"({
		BackgroundTransparency = 1,
	})

	local SocialPaneContainer = Utility.Create"Frame"({
		Name = "SocialPane",
		Size = UDim2.new(1, 0, 1, 0),
		BackgroundTransparency = 1,
		Visible = false,
		SelectionImageObject = noSelectionObject,
		Parent = parent,
	})

	local FriendsContainer = Utility.Create"Frame"({
		Name = "FriendsContainer",
		Size = UDim2.new(1, 0, 1, 0),
		Position = UDim2.new(0, 0, 0, 23),
		BackgroundTransparency = 1,
		Parent = SocialPaneContainer,
	})

	local friendsScrollerInstance;
	local function ReconcileFriendsScrollerInstance()
		if not friendsScrollerInstance then
			return
		end
		local friendsScroller = Roact.createElement(RoactRodux.StoreProvider, {
			store = AppState.store,
		}, {
			FriendsView = Roact.createElement(FriendsView, {
				inFocus = isPaneFocused,
				hide = not SocialPaneContainer.Visible,
				redirectUp = function()
					Utility.SetSelectedCoreObject(UpSelector)
				end,
			})
		})
		friendsScrollerInstance = Roact.reconcile(friendsScrollerInstance, friendsScroller)
	end

	function this:GetName()
		return Strings:LocalizedString("FriendsWord")
	end

	function this:IsFocused()
		return isPaneFocused
	end

	--[[ Public API ]]--
	function this:GetAnalyticsInfo()
		return {[Analytics.WidgetNames("WidgetId")] = Analytics.WidgetNames("SocialPaneId")}
	end

	function this:Show(fromAppHub)
		SocialPaneContainer.Visible = true
		--Suspend Friends BG Update whenever we are on GamesPane
		FriendsData:SuspendUpdate()

		--We rebuild Friends Scroller only if we navigate from other tabs
		if fromAppHub then
			if friendsScrollerInstance then
				Roact.unmount(friendsScrollerInstance)
			end
			local friendsScroller = Roact.createElement(RoactRodux.StoreProvider, {
				store = AppState.store,
			}, {
				FriendsView = Roact.createElement(FriendsView, {
					hide = not SocialPaneContainer.Visible,
					inFocus = isPaneFocused,
					redirectUp = function()
						Utility.SetSelectedCoreObject(UpSelector)
					end,
				})
			})
			friendsScrollerInstance = Roact.mount(friendsScroller, FriendsContainer, "FriendsViewContainer")
		else
			ReconcileFriendsScrollerInstance()
		end
		ScreenManager:PlayDefaultOpenSound()
	end

	function this:Hide(fromAppHub)
		SocialPaneContainer.Visible = false

		--We destroy Friends Scroller if we navigate to other tabs
		if fromAppHub then
			if friendsScrollerInstance then
				Roact.unmount(friendsScrollerInstance)
			end
			friendsScrollerInstance = nil
			--We resume Friends Update only if we navigate to other tabs
			FriendsData:ResumeUpdate()
		else
			ReconcileFriendsScrollerInstance()
		end
	end

	function this:Focus()
		isPaneFocused = true
		ReconcileFriendsScrollerInstance()
	end

	function this:RemoveFocus()
		isPaneFocused = false
		ReconcileFriendsScrollerInstance()
		local selectedObject = GuiService.SelectedCoreObject
		if selectedObject and selectedObject:IsDescendantOf(SocialPaneContainer) then
			Utility.SetSelectedCoreObject(nil)
		end
	end

	function this:SetPosition(newPosition)
		SocialPaneContainer.Position = newPosition
	end

	function this:SetParent(newParent)
		SocialPaneContainer.Parent = newParent
	end

	function this:IsAncestorOf(object)
		return SocialPaneContainer and SocialPaneContainer:IsAncestorOf(object)
	end

	return this
end

return CreateSocialPane