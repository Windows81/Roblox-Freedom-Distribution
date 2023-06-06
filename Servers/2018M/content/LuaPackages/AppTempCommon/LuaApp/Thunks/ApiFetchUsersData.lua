local CorePackages = game:GetService("CorePackages")

local Promise = require(CorePackages.AppTempCommon.LuaApp.Promise)
local ApiFetchUsersPresences = require(CorePackages.AppTempCommon.LuaApp.Thunks.ApiFetchUsersPresences)
local ApiFetchUsersThumbnail = require(CorePackages.AppTempCommon.LuaApp.Thunks.ApiFetchUsersThumbnail)

--this thunk will fill out users list with thumbnail and presence info
return function(networkImpl, userIds, thumbnailRequest)
	return function(store)
		local fetchedPromises = {}

		table.insert(fetchedPromises, store:dispatch(ApiFetchUsersPresences(networkImpl, userIds)))
		table.insert(fetchedPromises, store:dispatch(ApiFetchUsersThumbnail(networkImpl, userIds, thumbnailRequest)))

		return Promise.all(fetchedPromises)
	end
end