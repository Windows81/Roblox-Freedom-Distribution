local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Requests = Modules.LuaApp.Http.Requests
local UsersGetPresence = require(Requests.UsersGetPresence)
local ReceivedUserPresence = require(Modules.LuaChat.Actions.ReceivedUserPresence)

local User = require(Modules.LuaApp.Models.User)

local webPresenceMap = {
	[0] = User.PresenceType.OFFLINE,
	[1] = User.PresenceType.ONLINE,
	[2] = User.PresenceType.IN_GAME,
	[3] = User.PresenceType.IN_STUDIO
}

return function(networkImpl, userIds)
	return function(store)
		return UsersGetPresence(networkImpl, userIds):andThen(function(result)
			local responseBody = result.responseBody

			for _, presenceModel in pairs(responseBody.userPresences) do
				store:Dispatch(ReceivedUserPresence(
					tostring(presenceModel.userId),
					webPresenceMap[presenceModel.userPresenceType],
					presenceModel.lastLocation,
					presenceModel.placeId
				))
			end
		end)
	end
end