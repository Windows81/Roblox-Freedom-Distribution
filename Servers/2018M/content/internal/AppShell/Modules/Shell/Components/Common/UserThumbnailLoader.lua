--[[
		Creates a Image Loader
		Props:
			rbxuid : int - Roblox user id.
			thumbnailType : Enum.ThumbnailType - Describes the type of user thumbnail that should be returned by GetUserThumbnailAsync.
			thumbnailSize : Enum.ThumbnailSize - Describes the resolution of a user thumbnail being returned by GetUserThumbnailAsync.
			Size : UDim2 - The thumbnail image size.
			Position : UDim2 - The thumbnail image position.
			BackgroundTransparency : float - Transparency of the thumbnail image background.
			BackgroundColor3 : Color3 - Color of the thumbnail image background.
			hasThumbnailData : bool - Whether we have the corresponding thumbnail data in store.
			imageUrl : string - The imageUrl for the thumbnail.
			isFetching : bool - Whether we are fetching the thumbnail.
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Components = Modules.Shell.Components
local Roact = require(Modules.Common.Roact)
local GlobalSettings = require(Modules.Shell.GlobalSettings)
local RoactRodux = require(Modules.Common.RoactRodux)
local ApiFetchUserThumbnail = require(Modules.Shell.Thunks.ApiFetchUserThumbnail)
local Spinner = require(Components.Common.Spinner)
local memoize = require(Modules.Common.memoize)
local RETRIES = 6

local UserThumbnailLoader = Roact.PureComponent:extend("UserThumbnailLoader")

function UserThumbnailLoader:render()
	local props = self.props
	local rbxuid = props.rbxuid
	local children = {}

	local imageUrl = ""
	if rbxuid and rbxuid > 0 then
		local hasThumbnailData = props.hasThumbnailData
		--TODO: Try refetch if last fetched failed after some interval
		if hasThumbnailData and props.imageUrl then
			imageUrl = props.imageUrl
		else
			props.fetchImage(rbxuid, props.thumbnailType, props.thumbnailSize)
		end

		if props.showSpinner then
			children.Spinner = props.isFetching and Roact.createElement(Spinner)
		end
	else
		children.XboxDefaultProfileImage = Roact.createElement("ImageLabel", {
			Size = UDim2.new(0.5, 0, 0.5, 0),
			Position = UDim2.new(0.25, 0, 0.25, 0),
			BackgroundTransparency = 1,
			Image = GlobalSettings.Images.DefaultProfile,
		})
	end

	return Roact.createElement("ImageLabel", {
		Image = imageUrl,
		Size = props.size or UDim2.new(1, 0, 1, 0),
		Position = props.position or UDim2.new(0, 0, 0, 0),
		BackgroundTransparency = props.backgroundTransparency or 0,
		BorderSizePixel = 0,
		BackgroundColor3 = props.backgroundColor3 or GlobalSettings.Colors.CharacterBackground,
	}, children)
end

local getThumbnailData = memoize(function(thumbnailData)
	return {
		hasThumbnailData = thumbnailData ~= nil,
		isFetching = thumbnailData and thumbnailData.isFetching,
		imageUrl = thumbnailData and thumbnailData.imageUrl,
	}
end)

local function mapStateToProps(state, props)
	local rbxuid = props.rbxuid
	local thumbnailType = props.thumbnailType
	local thumbnailSize = props.thumbnailSize
	local thumbnailData;
	if rbxuid and rbxuid > 0 and thumbnailType and thumbnailSize then
		local thumbnailId = table.concat{ rbxuid, thumbnailType.Name, thumbnailSize.Name }
		thumbnailData = state.UserThumbnails[thumbnailId]
	end
	return getThumbnailData(thumbnailData)
end

local function mapDispatchToProps(dispatch)
	return {
		fetchImage = function(rbxuid, thumbnailType, thumbnailSize)
			return dispatch(ApiFetchUserThumbnail(rbxuid, thumbnailType, thumbnailSize, RETRIES))
		end
	}
end

return RoactRodux.UNSTABLE_connect2(mapStateToProps, mapDispatchToProps)(UserThumbnailLoader)
