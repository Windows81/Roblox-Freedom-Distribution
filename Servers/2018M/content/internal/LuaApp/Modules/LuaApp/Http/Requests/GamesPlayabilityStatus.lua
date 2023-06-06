local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Url = require(Modules.LuaApp.Http.Url)

--[[
	This endpoint returns a promise that resolves to:
	{
		"playabilityStatus": "UnplayableOtherReason"
	}

	requestImpl - (function<promise<HttpResponse>>(url, requestMethod, options))
	universeId - universeId that is passed into the request
]]--

return function(requestImpl, universeId)
	assert(type(universeId) == "string", "GamesPlayabilityStatus request expects universeId to be a string")

	local url = string.format("%s/v1/games/%s/playability-status", Url.GAME_URL, universeId)

	-- return a promise of the result listed above
	return requestImpl(url, "GET")
end