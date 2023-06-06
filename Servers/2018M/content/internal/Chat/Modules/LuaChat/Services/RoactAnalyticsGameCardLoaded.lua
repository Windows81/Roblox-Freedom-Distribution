local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Events = Modules.LuaChat.Analytics.Events
local loadGameLinkCardInChat = require(Events.loadGameLinkCardInChat)
local RoactAnalytics = require(Modules.LuaApp.Services.RoactAnalytics)

local GameCardLoadedAnalytics = {}
function GameCardLoadedAnalytics.get(context)
	local analyticsImpl = RoactAnalytics.get(context)

	local analyticsConsumer = {}

	function analyticsConsumer.reportGameCardLoadedInLuaChat(conversationId, placeId)
		loadGameLinkCardInChat(analyticsImpl.EventStream, "luaAppChat", conversationId, placeId)
	end

	return analyticsConsumer
end

return GameCardLoadedAnalytics