local CorePackages = game:GetService("CorePackages")
local Requests = CorePackages.AppTempCommon.LuaApp.Http.Requests

local ApiFetchUsersData = require(CorePackages.AppTempCommon.LuaApp.Thunks.ApiFetchUsersData)
local ApiFetchUsersFriendCount = require(CorePackages.AppTempCommon.LuaApp.Thunks.ApiFetchUsersFriendCount)
local UsersGetFriends = require(Requests.UsersGetFriends)

local AddUsers = require(CorePackages.AppTempCommon.LuaApp.Actions.AddUsers)
local UserModel = require(CorePackages.AppTempCommon.LuaApp.Models.User)

return function(requestImpl, userId, thumbnailRequests)
	return function(store)
		return store:dispatch(ApiFetchUsersFriendCount(requestImpl)):andThen(function()
			return UsersGetFriends(requestImpl, userId):andThen(function(response)
				local responseBody = response.responseBody

				local userIds = {}
				local newUsers = {}
				for _, userData in pairs(responseBody.data) do
					local id = tostring(userData.id)
					local newUser = UserModel.fromData(id, userData.name, true)

					table.insert(userIds, id)
					newUsers[newUser.id] = newUser
				end
				store:dispatch(AddUsers(newUsers))

				return userIds
			end):andThen(function(userIds)
				store:dispatch(ApiFetchUsersData(requestImpl, userIds, thumbnailRequests))
			end)
		end)
	end
end