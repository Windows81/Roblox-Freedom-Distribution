local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Actions = Modules.LuaApp.Actions
local Requests = Modules.LuaApp.Http.Requests
local GamesGetSorts = require(Requests.GamesGetSorts)
local AddGameSorts = require(Actions.AddGameSorts)
local SetGameSortsInGroup = require(Actions.SetGameSortsInGroup)
local GameSort = require(Modules.LuaApp.Models.GameSort)
local Promise = require(Modules.LuaApp.Promise)
local SetGameSortTokenFetchingStatus = require(Actions.SetGameSortTokenFetchingStatus)
local SetNextTokenRefreshTime = require(Modules.LuaApp.Actions.SetNextTokenRefreshTime)
local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)

local min = math.min

local function parseSortDataIntoStore(sortCategory, store, result)
	local data = result.responseBody
	if data.sorts then
		local decodedDataSorts = {}
		local gameSorts = {}
		local minExpiryTime = nil
		for _, gameSortJson in ipairs(data.sorts) do
			local gameSort = GameSort.fromJsonData(gameSortJson)
			decodedDataSorts[#decodedDataSorts + 1] = gameSort
			gameSorts[#gameSorts + 1] = gameSortJson.name

			-- get minimum time for the next refresh
			if not minExpiryTime then
				minExpiryTime = gameSortJson.tokenExpiryInSeconds
			else
				minExpiryTime = min(minExpiryTime, gameSortJson.tokenExpiryInSeconds)
			end
		end
		store:Dispatch(AddGameSorts(decodedDataSorts))
		store:Dispatch(SetGameSortsInGroup(sortCategory, gameSorts))
		return minExpiryTime
	end
	return -1
end

--[[
	This function will retry for MAX_RETRY_TIME before it
	fails and reject with false.
	retryTime -- How many time has this request retried
]]
local function fetchToken(networkImpl, store, sortCategory)
	return GamesGetSorts(networkImpl, sortCategory):andThen(function(result)
		local minExpiryTime = parseSortDataIntoStore(sortCategory, store, result)

		-- there is no data in fetching result
		if minExpiryTime < 0 then
			store:Dispatch(SetGameSortTokenFetchingStatus(sortCategory, RetrievalStatus.Failed))
			return Promise.reject("No sort data found in response.")
		end

		store:Dispatch(SetNextTokenRefreshTime(sortCategory, tick() + minExpiryTime))
		store:Dispatch(SetGameSortTokenFetchingStatus(sortCategory, RetrievalStatus.Done))
		return Promise.resolve()
	end,

	-- failure handler for request 'GamesGetSorts'
	function()
		store:Dispatch(SetGameSortTokenFetchingStatus(sortCategory, RetrievalStatus.Failed))
		return Promise.reject("Request failed.")
	end)
end

--[[
	A thunk fetches the tokens for sorts
	networkImpl -- networking object
	sortCategory -- HomeGames/Games
]]
return function(networkImpl, sortCategory)
	return function(store)
		if(store:getState().RequestsStatus.GameSortTokenFetchingStatus[sortCategory] == RetrievalStatus.Fetching) then
			return Promise.reject("Data is fetching.")
		else
			store:Dispatch(SetGameSortTokenFetchingStatus(sortCategory, RetrievalStatus.Fetching))
		end
		return fetchToken(networkImpl, store, sortCategory)
	end
end