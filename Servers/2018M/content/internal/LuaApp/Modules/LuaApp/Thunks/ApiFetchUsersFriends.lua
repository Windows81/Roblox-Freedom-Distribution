local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Requests = Modules.LuaApp.Http.Requests

local ApiFetchUsersFriendCount = require(Modules.LuaApp.Thunks.ApiFetchUsersFriendCount)
local ApiFetchUsersData = require(Modules.LuaApp.Thunks.ApiFetchUsersData)
local UsersGetFriends = require(Requests.UsersGetFriends)

local UserModel = require(Modules.LuaApp.Models.User)
local AddUsers = require(Modules.LuaApp.Actions.AddUsers)

return function(networkImpl, userId, thumbnailRequests)
	return function(store)
		return store:Dispatch(ApiFetchUsersFriendCount(networkImpl)):andThen(function()
			return UsersGetFriends(networkImpl, userId):andThen(function(response)
				local responseBody = response.responseBody

				local userIds = {}
				local newUsers = {}
				for _, userData in pairs(responseBody.data) do
					local id = tostring(userData.id)
					local newUser = UserModel.fromData(id, userData.name, true)

					table.insert(userIds, id)
					newUsers[newUser.id] = newUser
				end
				store:Dispatch(AddUsers(newUsers))

				return userIds
			end):andThen(function(userIds)
				store:Dispatch(ApiFetchUsersData(networkImpl, userIds, thumbnailRequests))
			end)
		end)
	end
end