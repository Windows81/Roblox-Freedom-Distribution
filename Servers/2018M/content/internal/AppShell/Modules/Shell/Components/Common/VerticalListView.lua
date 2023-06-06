--[[
		Creates a Roact component provides a vertical list view for multiple elements
		Props:
			PaddingTop : UDim - The top padding for the list
			PaddingBottom : UDim - The bottom padding for the list
			Spacing : UDim - The spacing between each item of the list
			HorizontalAlignment : HorizontalAlignment - Determines how grid is placed within
														 it's parent's container in the x direction.
														 Can be Left, Center, or Right.
			ScrollingEnabled : bool - Determines whether or not scrolling is allowed on the frame.
										If false, no scroll bars will be rendered.
			ScrollBarThickness : number - How thick the scroll bar appears.
											This applies to both the horizontal and vertical scroll bars.
											If set to 0, no scroll bars are rendered.
			CanvasPosition : Vector2 - The location within the canvas, in pixels,
										that should be drawn at the top left of the scroll frame.
			CanvasSize : UDim2 - Determines the size of the area that is scrollable.
									The UDim2 is calculated using the parent gui's size,
									similar to the regular Size property on gui objects.
			Items: array<Roact.Component> - The items in the list view
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)


return function(props)
	local paddingTop = props.PaddingTop
	local paddingBottom = props.PaddingBottom
	local spacing = props.Spacing
	local horizontalAlignment = props.HorizontalAlignment
	local scrollBarThickness = props.ScrollBarThickness
	local scrollingEnabled = props.ScrollingEnabled
	local canvasPosition = props.CanvasPosition
	local canvasSize = props.CanvasSize
	local ListItems  = {}
	ListItems["UIPadding"] = Roact.createElement("UIPadding",
	{
		PaddingTop = paddingTop,
		PaddingBottom = paddingBottom,
	})
	ListItems["UIListLayout"] = Roact.createElement("UIListLayout",
	{
		Padding = spacing,
		FillDirection = Enum.FillDirection.Vertical,
		SortOrder = Enum.SortOrder.LayoutOrder,
		HorizontalAlignment = horizontalAlignment,
		VerticalAlignment = Enum.VerticalAlignment.Top,
		CanvasPosition = canvasPosition,
		CanvasSize = canvasSize,
	})
	for k,v in pairs(props.Items) do
		ListItems[k] = v
	end

	return Roact.createElement("ScrollingFrame",
	{
		Size = UDim2.new(1,0,1,0),
		ScrollBarThickness = scrollBarThickness,
		BackgroundTransparency = 1,
		Selectable = false,
		ScrollingEnabled = scrollingEnabled,
	},ListItems)
end