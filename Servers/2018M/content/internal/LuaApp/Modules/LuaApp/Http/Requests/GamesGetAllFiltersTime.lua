local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Url = require(Modules.LuaApp.Http.Url)

--[[
	This endpoint returns a promise that resolves to:

	[
		{
			"token": "string",
			"name": "string"
		}, {...}, ...
	]

]]--

-- requestImpl - (function<promise<HttpResponse>>(url, requestMethod, options))
return function(requestImpl)
	local url = string.format("%sv1/games/all-time-filters", Url.GAME_URL)

	-- return a promise of the result listed above
	return requestImpl(url, "GET")
end