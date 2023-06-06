local Modules = game:GetService("CoreGui").RobloxGui.Modules
local ShellModules = Modules:FindFirstChild("Shell")
local MakeSafeAsyncRodux = require(ShellModules:FindFirstChild("SafeAsyncRodux"))
local PlayersService = game:GetService("Players")
local FetchUserThumbnail = require(ShellModules.Actions.FetchUserThumbnail)
local SetUserThumbnail = require(ShellModules.Actions.SetUserThumbnail)
local ContentProvider = game:GetService("ContentProvider")

local TEMPLATE_DECAL = Instance.new("Decal")
local function preloadThumbnailAsync(assetId)
	TEMPLATE_DECAL.Texture = assetId
	ContentProvider:PreloadAsync({ TEMPLATE_DECAL })
end

local GetUserThumbnailAsync = function(store, rbxuid, thumbnailType, thumbnailSize, retryTime)
	MakeSafeAsyncRodux({
		asyncFunc = function(store, rbxuid, thumbnailType, thumbnailSize)
			local imageUrl = nil
			local isFinal = nil
			local success = pcall(function()
				imageUrl, isFinal = PlayersService:GetUserThumbnailAsync(rbxuid, thumbnailType, thumbnailSize)
			end)
			if success and isFinal and imageUrl then
				preloadThumbnailAsync(imageUrl)
			else
				imageUrl = nil
			end
			return {
				success = success,
				rbxuid = rbxuid,
				thumbnailType = thumbnailType,
				thumbnailSize = thumbnailSize,
				imageUrl = imageUrl,
				isFinal = isFinal,
				timestamp = tick()
			}
		end,
		callback = function(store, result)
			store:dispatch(SetUserThumbnail(result))
		end,
		retries = retryTime,
		retryFunc = function(store, result)
			return not (result.success and result.isFinal)
		end,
		userRelated = true
	})(store, rbxuid, thumbnailType, thumbnailSize)
end

return function(rbxuid, thumbnailType, thumbnailSize, retryTime, forceUpdate)
	return function(store)
		local state = store:getState()
		local userThumbnailsState = state.UserThumbnails
		local thumbnailId = table.concat{ rbxuid, thumbnailType.Name, thumbnailSize.Name }
		local thumbnailData = userThumbnailsState[thumbnailId]
		--TODO: may use lastUpdated timestamp to determine whether to refetch
		if thumbnailData then
			if thumbnailData.isFetching then
				return
			end
			if thumbnailData.imageUrl and not forceUpdate then
				return
			end
		end
		store:dispatch(FetchUserThumbnail({ rbxuid = rbxuid, thumbnailType = thumbnailType, thumbnailSize = thumbnailSize }))
		spawn(function()
			GetUserThumbnailAsync(store, rbxuid, thumbnailType, thumbnailSize, retryTime)
		end)
	end
end