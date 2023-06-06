local CoreGui = game:GetService("CoreGui")
local Action = require(CoreGui.RobloxGui.Modules.Common.Action)

return Action("SetUserThumbnail", function(thumbnailInfo)
	thumbnailInfo = thumbnailInfo or {}
	return {
		success = thumbnailInfo.success,
		rbxuid = thumbnailInfo.rbxuid,
		imageUrl = thumbnailInfo.imageUrl,
		thumbnailType = thumbnailInfo.thumbnailType,
		thumbnailSize = thumbnailInfo.thumbnailSize,
		isFinal = thumbnailInfo.isFinal,
		timestamp = thumbnailInfo.timestamp
	}
end)