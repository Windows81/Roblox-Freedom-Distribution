--[[
	Unlike RoactAnalytics, RoactAnalyticsAppStageLoaded is merely a consumer of the analytics implementation.
	It does not require its own setter to be called when the RoactServices ServiceProvider is initialized.
]]

local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Events = Modules.LuaApp.Analytics.Events
local appStageLoaded = require(Events.appStageLoaded)
local RoactAnalytics = require(Modules.LuaApp.Services.RoactAnalytics)

local AppStageLoadedAnalytics = {}
function AppStageLoadedAnalytics.get(context)
	local analyticsImpl = RoactAnalytics.get(context)

	local analyticsConsumer = {}

	function analyticsConsumer.reportAppReady(eventContext)
		appStageLoaded(analyticsImpl.EventStream, eventContext, "appReady")
	end

	return analyticsConsumer
end

return AppStageLoadedAnalytics