local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)

local NotificationType = require(Modules.LuaApp.Enum.NotificationType)

local AppPage = require(Modules.LuaApp.AppPage)
local AppGuiService = require(Modules.LuaApp.Services.AppGuiService)
local RoactServices = require(Modules.LuaApp.RoactServices)

local FlagSettings = require(Modules.LuaApp.FlagSettings)
local isLoadingHUDOniOSEnabledForGameShare = FlagSettings.IsLoadingHUDOniOSEnabledForGameShare()

-- TODO Once HomePage and GamesHub creates their own ScreenGui,
-- the ScreenGuiWrap should be removed.
local ScreenGuiWrap = Roact.PureComponent:extend("ScreenGuiWrap")

function ScreenGuiWrap:didMount()
	local isVisible = self.props.isVisible
	local pageType = self.props.pageType
	local guiService = self.props.guiService

	if isLoadingHUDOniOSEnabledForGameShare then
		if isVisible and pageType ~= AppPage.ShareGameToChat then
			guiService:BroadcastNotification(pageType, NotificationType.APP_READY)
		end
	else
		if isVisible then
			guiService:BroadcastNotification(pageType, NotificationType.APP_READY)
		end
	end
end

function ScreenGuiWrap:render()
	local component = self.props.component
	local isVisible = self.props.isVisible
	local props = self.props.props

	return Roact.createElement("ScreenGui", {
		Enabled = isVisible,
		ZIndexBehavior = Enum.ZIndexBehavior.Sibling,
	}, {
		Contents = Roact.createElement(component, props),
	})
end

-- Staging broadcasting of APP_READY to accomodate for unpredictable delay on the native side.
-- Once Lua tab bar is integrated, there will be no use for this, as current page information
-- will be propagated instantly within the Roact paradigm.
function ScreenGuiWrap:didUpdate(prevProps, prevState)
	local guiService = self.props.guiService

	if not prevProps.isVisible and self.props.isVisible then
		guiService:BroadcastNotification(self.props.pageType, NotificationType.APP_READY)
	end
end

return RoactServices.connect({
	guiService = AppGuiService
})(ScreenGuiWrap)