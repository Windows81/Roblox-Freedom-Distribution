local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Actions = Modules.LuaApp.Actions
local Requests = Modules.LuaApp.Http.Requests
local UsersGetThumbnail = require(Requests.UsersGetThumbnail)
local SetUserThumbnail = require(Actions.SetUserThumbnail)
local Promise = require(Modules.LuaApp.Promise)

local function fetchThumbnailsBatch(networkImpl, userIds, thumbnailRequest)
	local fetchedPromises = {}

	for _, userId in pairs(userIds) do
		table.insert(fetchedPromises,
			UsersGetThumbnail(userId, thumbnailRequest.thumbnailType, thumbnailRequest.thumbnailSize)
		)
	end

	return Promise.all(fetchedPromises)
end

return function(networkImpl, userIds, thumbnailRequests)
	return function(store)
		return Promise.new(function()
			-- We currently cannot batch request user avatar thumbnails,
			-- so each thumbnailRequest has to be processed individually.

			local fetchedPromises = {}
			for _, thumbnailRequest in pairs(thumbnailRequests) do
				table.insert(fetchedPromises,
					fetchThumbnailsBatch(networkImpl, userIds, thumbnailRequest):andThen(function(result)
						for _, data in pairs(result) do
							store:Dispatch(SetUserThumbnail(data.id, data.image, data.thumbnailType, data.thumbnailSize))
						end
					end)
				)
			end

			return Promise.all(fetchedPromises)
		end)
	end
end