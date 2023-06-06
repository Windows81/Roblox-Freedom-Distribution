local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)

local SHADOW_SPREAD_TOP = 5
local SHADOW_SPREAD_BOTTOM = 6
local SHADOW_SPREAD_LEFT = 6
local SHADOW_SPREAD_RIGHT = 6
local SHADOW_SLICE_CENTER = Rect.new(11, 11, 12, 12)

local function DropshadowFrame(props)
	local anchorPoint = props.AnchorPoint
	local layoutOrder = props.LayoutOrder
	local position = props.Position
	local size = props.Size
	local backgroundColor3 = props.BackgroundColor3
	local children = props[Roact.Children]

	return Roact.createElement("Frame", {
		AnchorPoint = anchorPoint,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		LayoutOrder = layoutOrder,
		Position = position,
		Size = size,
	}, {
		Shadow = Roact.createElement("ImageLabel", {
			Size = UDim2.new(1, SHADOW_SPREAD_LEFT + SHADOW_SPREAD_RIGHT, 1, SHADOW_SPREAD_TOP + SHADOW_SPREAD_BOTTOM),
			Position = UDim2.new(0, -SHADOW_SPREAD_LEFT, 0, -SHADOW_SPREAD_TOP),
			Image = "rbxasset://textures/ui/LuaApp/9-slice/gr-shadow.png",
			ScaleType = "Slice",
			SliceCenter = SHADOW_SLICE_CENTER,
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
		}),
		MainFrame = Roact.createElement("Frame", {
			AnchorPoint = Vector2.new(0.5, 0.5),
			Position = UDim2.new(0.5, 0, 0.5, 0),
			Size = UDim2.new(1, 0, 1, 0),
			BackgroundColor3 = backgroundColor3,
			BorderSizePixel = 0,
			ZIndex = 2,
		}, children),
	})
end

return DropshadowFrame