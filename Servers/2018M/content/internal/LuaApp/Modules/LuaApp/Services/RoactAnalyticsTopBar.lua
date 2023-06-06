--[[
	Unlike RoactAnalytics, RoactAnalyticsTopBar is merely a consumer of the analytics implementation.
	It does not require its own setter to be called when the RoactServices ServiceProvider is initialized.
]]

local Modules = game:GetService("CoreGui").RobloxGui.Modules

local search = require(Modules.LuaApp.Analytics.Events.search)
local nsOpenContent = require(Modules.LuaApp.Analytics.Events.nsOpenContent)
local buttonClick = require(Modules.LuaApp.Analytics.Events.buttonClick)
local RoactAnalytics = require(Modules.LuaApp.Services.RoactAnalytics)

local TopBarAnalytics = {}
function TopBarAnalytics.get(context)
	local analyticsImpl = RoactAnalytics.get(context)

	local TPA = {}

	local reportSearch = function(eventContext, act, keyword)
		search(analyticsImpl.EventStream, eventContext, act, keyword)
	end

	function TPA.reportSearchFocused(eventContext)
		reportSearch(eventContext, "open", nil)
	end

	function TPA.reportSearched(eventContext, keyword)
		reportSearch(eventContext, "search", keyword)
	end

	function TPA.reportSearchCanceled(eventContext)
		reportSearch(eventContext, "cancel", nil)
	end

	function TPA.reportNSButtonTouch(count)
		nsOpenContent(analyticsImpl.EventStream, "touch", count)
	end

	function TPA.reportRobuxButtonClick(eventContext)
		buttonClick(analyticsImpl.EventStream, eventContext, "robux")
	end

	return TPA
end

return TopBarAnalytics
