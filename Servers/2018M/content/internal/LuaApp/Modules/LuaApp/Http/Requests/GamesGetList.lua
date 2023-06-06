local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Url = require(Modules.LuaApp.Http.Url)

--[[
	This endpoint returns a promise that resolves to:

	{
		"games": [
		{
			"creatorId": 0,
			"creatorName": "string",
			"creatorType": "string",
			"totalUpVotes": 0,
			"totalDownVotes": 0,
			"universeId": 0,
			"name": "string",
			"placeId": 0,
			"playerCount": 0,
			"imageToken": "string",
			"imageTokenExpiryInSeconds": 0,
			"users": [
			{
				"userId": 0,
				"gameId": "string"
			}, {...}, ... ],
			"isSponsored": true,
			"nativeAdData": "string"
		}, {...}, ... ],
		"suggestedKeyword": "string",
		"correctedKeyword": "string",
		"filteredKeyword": "string",
		"hasMoreRows": true,
		"nextPageExclusiveStartId": number / nil
	}

	requestImpl - (function<promise<HttpResponse>>(url, requestMethod, options))
	argTable - (Table) of argument that is passed into the request

	A sample argTable:
	{
		sortToken = "SOME_SORT_TOKEN",
		gameFilter = "SOME_GAME_FILTER",
		timeFilter = "SOME_TIMER_FILTER",
		genreFilter = "SOME_GENRE_FILTER",

		-- This value has to be filled for the featured sort to work properly.
		exclusiveStartId = 1298471975,
		sortOrder = 1,
		keyword = "WHAT_YOU_SEARCH_FOR",

		-- When specifying startRows, the number doesn't include sponsored games.
		-- And games start counting from 0.
		startRows = 10,

		-- Must be aware that the games returned might be less than (filtered content)
		-- or even more than (sponsored games) the number specified in maxRows.
		-- When not specified, Api defaults this to 40.
		maxRows = 100,

		isKeywordSuggestionEnabled = true,
		contextCountryRegionId = 50,
		contextUniverseId = 192146914,
	}
]]--
return function(requestImpl, argTable)

	-- construct the url
	local args = Url:makeQueryString(argTable)
	local url = string.format("%sv1/games/list?%s", Url.GAME_URL, args)

	-- return a promise of the result listed above
	return requestImpl(url, "GET")
end