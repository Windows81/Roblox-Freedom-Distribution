local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Url = require(Modules.LuaApp.Http.Url)

--[[
	This endpoint returns a promise that resolves to:

	{
	  "unreadNotifications": 0,
	  "statusMessage": "string"
	}

]]--

return function(requestImpl)
	local url = string.format("%sv2/stream-notifications/unread-count", Url.NOTIFICATION_URL)

	-- return a promise of the result listed above
	return requestImpl(url, "GET")
end