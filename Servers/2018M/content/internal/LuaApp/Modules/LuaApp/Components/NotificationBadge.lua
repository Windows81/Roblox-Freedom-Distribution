local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)

local Constants = require(Modules.LuaApp.Constants)

local BADGE = "rbxasset://textures/ui/LuaApp/9-slice/gr-search.png"

local BADGE_HEIGHT = 20
local BADGE_WIDTH = 20
local BADGE_WIDTH_3_DIGIT = 24
local BADGE_SLICE_CENTER = Rect.new(9, 9, 9, 9)
local BADGE_SLICE_CENTER_3_DIGIT = Rect.new(9, 9, 9, 16)

local BADGE_Y_OFFSET = BADGE_HEIGHT/2
local BADGE_X_OFFSET = BADGE_HEIGHT/2 - 1

local FONT = Enum.Font.SourceSans

local function NotificationBadge(props)
	local layoutOrder = props.layoutOrder
	local notificationCount = props.notificationCount

	if not notificationCount or tonumber(notificationCount) == 0 then
		return nil
	end

	local badgeWidth = BADGE_WIDTH
	local badgeHeight = BADGE_HEIGHT
	local sliceCenter = BADGE_SLICE_CENTER

	local useExpandedSize = string.len(notificationCount) > 2

	if useExpandedSize then
		badgeWidth = BADGE_WIDTH_3_DIGIT
		sliceCenter = BADGE_SLICE_CENTER_3_DIGIT
	end

	return Roact.createElement("ImageLabel", {
		Size = UDim2.new(0, badgeWidth, 0, badgeHeight),
		AnchorPoint = Vector2.new(1, 0),
		Position = UDim2.new(1, BADGE_X_OFFSET, 0, -BADGE_Y_OFFSET),
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		Image = BADGE,
		LayoutOrder = layoutOrder,
		ScaleType = Enum.ScaleType.Slice,
		SliceCenter = sliceCenter,
		ImageColor3 = Color3.new(255,0,0),
	}, {
		Count = Roact.createElement("TextLabel", {
			Size = UDim2.new(0.6, 0, 0.6, 0),
			AnchorPoint = Vector2.new(0.5, 0.5),
			Position = UDim2.new(0.5, 0, 0.5, -1),
			BackgroundTransparency = 1,
			Font = FONT,
			Text = notificationCount,
			TextColor3 = Constants.Color.WHITE,
			TextSize = 14,
			TextScaled = useExpandedSize,
			TextWrapped = false,
		}),
	})
end

return NotificationBadge