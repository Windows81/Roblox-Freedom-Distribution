local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Promise = require(Modules.LuaApp.Promise)
local GamesPlayabilityStatus = require(Modules.LuaApp.Http.Requests.GamesPlayabilityStatus)
local SetPlayabilityStatus = require(Modules.LuaApp.Actions.SetPlayabilityStatus)
local PlayabilityStatus = require(Modules.LuaApp.Enum.PlayabilityStatus)

local function fetchPlayabilityStatus(networkImpl, universeId)
	assert(type(universeId) == "string", "ApiFetchPlayabilityStatus thunk expects universeId to be a string")

	return function(store)
		return GamesPlayabilityStatus(networkImpl, universeId):andThen(function(result)
			store:dispatch(SetPlayabilityStatus(universeId, result.responseBody.playabilityStatus))
			return Promise.resolve()
		end,

		-- failure handler for request 'GamesPlayabilityStatus'
		function(err)
			store:dispatch(SetPlayabilityStatus(universeId, PlayabilityStatus.RequestFailed))
			return Promise.reject(err)
		end)
	end
end

return fetchPlayabilityStatus