local Modules = game:GetService("CoreGui").RobloxGui.Modules

local RoactAnalytics = require(Modules.LuaApp.Services.RoactAnalytics)
local shareGameToChatFromChat = require(Modules.LuaChat.Analytics.Events.shareGameToChatFromChat)

local RoactAnalyticsSharedGameItem = {}
function RoactAnalyticsSharedGameItem.get(context)
	local analyticsImpl = RoactAnalytics.get(context)

	local AnalyticsObj = {}

	function AnalyticsObj.reportShareGameToChatFromChat(cid, pid)
		shareGameToChatFromChat(analyticsImpl.EventStream, "touch", cid, pid)
	end

	return AnalyticsObj
end

return RoactAnalyticsSharedGameItem