local ContentProvider = game:GetService("ContentProvider")

local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Roact = require(Modules.Common.Roact)

local decal = Instance.new("Decal")

local loadedImagesByUri = {}

local LoadableImage = Roact.PureComponent:extend("LoadableImage")

function LoadableImage:init()
	self.imageLabelRef = Roact.createRef()
end

function LoadableImage:render()
	local size = self.props.Size
	local position = self.props.Position
	local borderSizePixel = self.props.BorderSizePixel
	local backgroundColor3 = self.props.BackgroundColor3

	return Roact.createElement("ImageLabel", {
		Position = position,
		BorderSizePixel = borderSizePixel,
		BackgroundColor3 = backgroundColor3,
		Size = size,
		[Roact.Ref] = self.imageLabelRef,
	})
end

function LoadableImage:didUpdate(oldProps)
	self:_loadImage()
end

function LoadableImage:_loadImage()
	local image = self.props.Image

	if not image or image == "" then
		return
	end

	-- Check if the image is already the current GUI image
	if self.imageLabelRef.current.Image == image then
		return
	end

	-- Check if the image URI is already loaded
	if loadedImagesByUri[image] then
		self.imageLabelRef.current.Image = image
		return
	end

	-- Set default loading image
	self.imageLabelRef.current.Image = self.props.loadingImage

	-- Synchronization/Batching work should be done in engine for performance improvements
	-- related ticket: CLIPLAYEREX-1764
	spawn(function()
		decal.Texture = image
		ContentProvider:PreloadAsync({decal})

		loadedImagesByUri[image] = true

		-- Context might be changed when resume, so we should check if roblox object is still valid here
		if self.imageLabelRef.current and self.props.Image == image then
			self.imageLabelRef.current.Image = image
		end
	end)
end

LoadableImage.didMount = LoadableImage._loadImage

function LoadableImage._mockPreloadDone(image)
	loadedImagesByUri[image] = true
end

return LoadableImage