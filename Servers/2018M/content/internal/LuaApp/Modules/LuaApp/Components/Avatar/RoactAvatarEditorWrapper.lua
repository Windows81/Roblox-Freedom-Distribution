local CoreGui = game:GetService("CoreGui")
local Modules = CoreGui.RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)

local AppPage = require(Modules.LuaApp.AppPage)
local TopBar = require(Modules.LuaApp.Components.TopBar)
local NotificationType = require(Modules.LuaApp.Enum.NotificationType)
local AvatarEditorSetup = require(Modules.Mobile.AvatarEditorSetup)

local RoactAvatarEditorWrapper = Roact.PureComponent:extend("RoactAvatarEditorWrapper")

local AppGuiService = require(Modules.LuaApp.Services.AppGuiService)
local RoactServices = require(Modules.LuaApp.RoactServices)

function RoactAvatarEditorWrapper:init()
	local function notifyAppReady()
		-- Staging broadcasting of APP_READY to accomodate for unpredictable
		-- delay on the native side.
		-- Once Lua tab bar is integrated, there will be no use for this
		self.props.guiService:BroadcastNotification(AppPage.AvatarEditor, NotificationType.APP_READY)
	end

	AvatarEditorSetup:Initialize(notifyAppReady, true)
	self.isPageOpen = false
	self.topBarHeight = 0
end

function RoactAvatarEditorWrapper:render()
	local isVisible = self.props.isVisible

	return Roact.createElement(Roact.Portal, {
		target = CoreGui,
	}, {
		AvatarEditor = Roact.createElement("ScreenGui", {
			Enabled = isVisible,
			ZIndexBehavior = Enum.ZIndexBehavior.Sibling,
			DisplayOrder = 3, -- This is because AvatarEditor ScreenGui DisplayOrder is 2
		}, {
			TopBar = Roact.createElement(TopBar, {
				showBuyRobux = true,
				showNotifications = true,
			})
		})
	})
end

function RoactAvatarEditorWrapper:didMount()
	self:updateAvatarEditor()
end

function RoactAvatarEditorWrapper:didUpdate(prevProps, prevState)
	self:updateAvatarEditor()
end

function RoactAvatarEditorWrapper:willUnmount()
	AvatarEditorSetup:Close()
end

function RoactAvatarEditorWrapper:updateAvatarEditor()
	if not self.isPageOpen and self.props.isVisible then
		AvatarEditorSetup:Open()
		self.isPageOpen = true
	elseif self.isPageOpen and not self.props.isVisible then
		AvatarEditorSetup:Close()
		self.isPageOpen = false
	end

	if self.topBarHeight ~= self.props.topBarHeight then
		AvatarEditorSetup:UpdateTopBarHeight(self.props.topBarHeight)
		self.topBarHeight = self.props.topBarHeight
	end
end

RoactAvatarEditorWrapper = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			topBarHeight = state.TopBar.topBarHeight,
		}
	end
)(RoactAvatarEditorWrapper)

return RoactServices.connect({
	guiService = AppGuiService
})(RoactAvatarEditorWrapper)