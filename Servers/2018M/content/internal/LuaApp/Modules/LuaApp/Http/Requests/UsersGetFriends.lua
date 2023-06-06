local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Url = require(Modules.LuaApp.Http.Url)

return function(requestImpl, userId)
	local url = string.format("%s/users/%s/friends",
		Url.FRIEND_URL, userId
	)

	return requestImpl(url, "GET")
end