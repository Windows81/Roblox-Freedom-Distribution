local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local AddUser = require(LuaChat.Actions.AddUser)
local FetchingUser = require(LuaChat.Actions.FetchingUser)
local UserModel = require(LuaApp.Models.User)
local WebApi = require(LuaChat.WebApi)

return function(userId)
	return function(store)
		local oldUser = store:getState().Users[userId]
		if not oldUser or not oldUser.isFetching then
			store:dispatch(FetchingUser(userId, true))

			spawn(function()
				local status, result = WebApi.GetUser(userId)
				store:dispatch(FetchingUser(userId, false))
				if status ~= WebApi.Status.OK then

					warn("WebApi failure in GetUser")
					return
				end

				store:dispatch(AddUser(UserModel.fromData(result.Id, result.Username, false)))
			end)
		end
	end
end