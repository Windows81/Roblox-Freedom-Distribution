--[[
	Unlike RoactAnalytics, RoactAnalyticsHomePage is merely a consumer of the analytics implementation.
	It does not require its own setter to be called when the RoactServices ServiceProvider is initialized.
]]

local Modules = game:GetService("CoreGui").RobloxGui.Modules

local RoactAnalyticsCommonGameEvents = require(Modules.LuaApp.Services.RoactAnalyticsCommonGameEvents)

local HomePageAnalytics = {}
function HomePageAnalytics.get(context)
	return RoactAnalyticsCommonGameEvents.get(context, {
		pageName = "home",
		createReferralCtx = function(indexInSort, sortId)
			local context = string.format("home_SortFilter<%d>_Position<%d>",
				sortId,
				indexInSort)
			return context
		end
	})
end

return HomePageAnalytics