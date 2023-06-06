local Modules = game:GetService("CoreGui").RobloxGui.Modules

local GetUnreadNotificationCount = require(Modules.LuaApp.Http.Requests.GetUnreadNotificationCount)
local SetNotificationCount = require(Modules.LuaApp.Actions.SetNotificationCount)

return function(networkImpl)
	return function(store)
		return GetUnreadNotificationCount(networkImpl):andThen(function(response)
			local responseBody = response.responseBody
			local notificationCount = responseBody.unreadNotifications

			store:Dispatch(SetNotificationCount(notificationCount))

			return notificationCount
		end)
	end
end