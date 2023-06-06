local CoreGui = game:GetService("CoreGui")
local Action = require(CoreGui.RobloxGui.Modules.Common.Action)

return Action("FetchUserThumbnail", function(thumbnailInfo)
	thumbnailInfo = thumbnailInfo or {}
	return {
		rbxuid = thumbnailInfo.rbxuid,
		thumbnailType = thumbnailInfo.thumbnailType,
		thumbnailSize = thumbnailInfo.thumbnailSize
	}
end)