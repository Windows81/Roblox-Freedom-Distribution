local Modules = script.Parent.Parent

local WebApi = require(Modules.WebApi)
local ThumbnailModel = require(Modules.Models.ThumbnailModel)

local RequestPlaceThumbnail = require(Modules.Actions.RequestPlaceThumbnail)
local ReceivedPlaceThumbnail = require(Modules.Actions.ReceivedPlaceThumbnail)
local FailedToFetchPlaceThumbnail = require(Modules.Actions.FailedToFetchPlaceThumbnail)

local RETRY_COUNT  = 3
local WAIT_TIME  = 2

return function(imageToken, width, height)
	return function(store)
		local state = store:getState()
		if state.ChatAppReducer.PlaceThumbnailsAsync[imageToken] then
			return
		end
		store:dispatch(RequestPlaceThumbnail(imageToken))

		spawn(function()
			local thumbnail = ''
			local retryCount = RETRY_COUNT
			local waitTime = WAIT_TIME

			while (retryCount > 0) do
				local status, result = WebApi.GetPlaceThumbnail(imageToken, width, height)
				if status ~= WebApi.Status.OK then
					warn("WebApi failure in GetPlaceThumbnail")
					store:dispatch(FailedToFetchPlaceThumbnail(imageToken))
					break
				else
					local placeThumbnailData = result[1]
					if placeThumbnailData.final == true then
						thumbnail = placeThumbnailData.url
						break
					end
				end

				retryCount = retryCount - 1
				if retryCount > 0 then
					wait(waitTime)
					waitTime = waitTime * 2
				end
			end

			local thumbnailModel = ThumbnailModel.fromWeb(thumbnail)
			store:dispatch(ReceivedPlaceThumbnail(imageToken, thumbnailModel))

		end)
	end
end
