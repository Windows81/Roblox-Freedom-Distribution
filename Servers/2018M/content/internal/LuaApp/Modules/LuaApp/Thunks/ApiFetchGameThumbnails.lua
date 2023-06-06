local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Actions = Modules.LuaApp.Actions
local Requests = Modules.LuaApp.Http.Requests
local GamesGetThumbnails = require(Requests.GamesGetThumbnails)
local SetGameThumbnails = require(Actions.SetGameThumbnails)
local Functional = require(Modules.Common.Functional)
local Promise = require(Modules.LuaApp.Promise)

local function subdiveThumbnailTokenArray(thumbnailTokens, tokenLimit)
	local someTokens = {}
	for i = 1, #thumbnailTokens, tokenLimit do
		local subArray = Functional.Take(thumbnailTokens, tokenLimit, i)
		table.insert(someTokens, subArray)
	end

	return someTokens
end

local function fetchThumbnails(networkImpl, thumbnailTokens)
	return function(store)
		-- NOTE : because the size of each thumbnail token, me must limit the number we can fetch at a time.
		-- So break apart the array of tokens we get into smaller, more manageable pieces.
		local fetchPromises = {}
		local someTokens = subdiveThumbnailTokenArray(thumbnailTokens, 20)
		for _, thumbsArr in ipairs(someTokens) do

			local promise = GamesGetThumbnails(networkImpl, thumbsArr, 150, 150):andThen(function(result)
				local thumbnails = {}
				local totalUnfinished = 0
				local unfinalizedThumbnails = {}
				for _,image in pairs(result.responseBody) do
					-- Will update this later when WEBAPP-64 has been fixed
					local universeId = store:getState().PlaceIdsToUniverseIds[image.placeId]
					if image.final == false then
						totalUnfinished = totalUnfinished + 1
						unfinalizedThumbnails[universeId] = image.retryToken
					else
						-- index all of the thumbnails by universeId
						thumbnails[universeId] = image
					end
				end

				store:dispatch(SetGameThumbnails(thumbnails))

				-- refetch the subset of thumbnails that aren't finalized
				if totalUnfinished > 0 then
					print(string.format("%d thumbnails are not ready yet", totalUnfinished))
					return store:dispatch(fetchThumbnails(networkImpl, unfinalizedThumbnails))
				end
			end)

			-- track all of the promises
			table.insert(fetchPromises, promise)
		end

		return Promise.all(fetchPromises)
	end
end

return fetchThumbnails