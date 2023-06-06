local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Immutable = require(Modules.Common.Immutable)
local FetchUserThumbnail = require(Modules.Shell.Actions.FetchUserThumbnail)
local SetUserThumbnail = require(Modules.Shell.Actions.SetUserThumbnail)
local ResetUserThumbnails = require(Modules.Shell.Actions.ResetUserThumbnails)

return function(state, action)
	state = state or {}

	if action.type == FetchUserThumbnail.name then
		local rbxuid = action.rbxuid
		local thumbnailType = action.thumbnailType
		local thumbnailSize = action.thumbnailSize
		local thumbnailId = table.concat{ rbxuid, thumbnailType.Name, thumbnailSize.Name }
		local thumbnailData = state[thumbnailId] or {}
		state = Immutable.Set(state, thumbnailId, Immutable.Set(thumbnailData, "isFetching", true))
	elseif action.type == SetUserThumbnail.name then
		local rbxuid = action.rbxuid
		local thumbnailType = action.thumbnailType
		local thumbnailSize = action.thumbnailSize
		local thumbnailId = table.concat{ rbxuid, thumbnailType.Name, thumbnailSize.Name }
		local thumbnailData = state[thumbnailId] or {}
		--add fetchSuccess as fetchSuccess will indicate the last fetchSuccess or not (We can deduce it from imageUrl and lastUpdated, but it's more clear to have this in store)
		if action.success and action.isFinal then --Only update image if fetch success and is final image
			state = Immutable.Set(state, thumbnailId,
				Immutable.JoinDictionaries(thumbnailData, {
					fetchSuccess = true,
					isFetching = false,
					imageUrl = action.imageUrl,
					lastUpdated = action.timestamp
				})
			)
		else
			state = Immutable.Set(state, thumbnailId,
				Immutable.JoinDictionaries(thumbnailData, {
					fetchSuccess = false,
					isFetching = false,
					--We need lastUpdated time
					lastUpdated = action.timestamp
				})
			)
		end
	elseif action.type == ResetUserThumbnails.name then
		state = {}
	end

	return state
end