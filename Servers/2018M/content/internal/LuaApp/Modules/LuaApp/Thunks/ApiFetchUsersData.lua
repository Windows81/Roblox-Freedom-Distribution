local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Promise = require(Modules.LuaApp.Promise)
local ApiFetchUsersPresences = require(Modules.LuaApp.Thunks.ApiFetchUsersPresences)
local ApiFetchUsersThumbnail = require(Modules.LuaApp.Thunks.ApiFetchUsersThumbnail)

--this thunk will fill out users list with thumbnail and presence info
return function(networkImpl, userIds, thumbnailRequest)
	return function(store)
		local fetchedPromises = {}

		table.insert(fetchedPromises, store:Dispatch(ApiFetchUsersPresences(networkImpl, userIds)))
		table.insert(fetchedPromises, store:Dispatch(ApiFetchUsersThumbnail(networkImpl, userIds, thumbnailRequest)))

		return Promise.all(fetchedPromises)
	end
end