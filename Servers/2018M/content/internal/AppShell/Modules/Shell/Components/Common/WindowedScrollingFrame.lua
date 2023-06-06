--[[
		Creates a Roact component for inifinite scrolling
		Props:
			scrollingFrameProps : dictionary - props for the scrolling frame
				.Selectable : bool - Whether or not this object should be selectable using joysticks (controller).
				.ClipsDescendants : bool - Determines whether Roblox will render any portions of its GUI descendants that are outside of its own borders.
			items : Array - An array of the input item data which is used to construct item component.
			itemSize : Vector2 - The size for each item in the scrolling frame.
			itemsPaddingOffset : int - The padding between each item.
			scrollingDirection : Enum.ScrollingDirection - The scrolling direction of the scrolling frame, can't be Enum.ScrollingDirection.XY.
			itemOffsetStart: int - The minimum distance of the selected guiobject to the window start border.
			itemOffsetEnd: int - The minimum distance of the selected guiobject to the window end border.
			customScrollDist: dictionary - Custom distances to trigger the scroll.
			generateKey : function() - Used to generate a name for the item.
			renderItem : function() -
				Input: item data, item index and an onSelectionGained callback
				Output: a Roact Component
		State:
			viewStart: int - The item start index.
			viewSize: int - The number of items can be put in the window.
			paddingStart: int - The padding to apply on the top / left side of the scrolling frame.
]]

local GuiService = game:GetService("GuiService")
local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Utility = require(Modules.Shell.Utility)
local Roact = require(Modules.Common.Roact)
local WindowedScrollingFrame = Roact.PureComponent:extend("WindowedScrollingFrame")


local function clipCanvasPosition(scrollingFrame, canvasPos)
	local canvasPosX = canvasPos.X
	local canvasPosY = canvasPos.Y
	canvasPosX = math.min(canvasPosX, scrollingFrame.CanvasSize.X.Offset - scrollingFrame.AbsoluteWindowSize.X)
	canvasPosX = math.max(0, canvasPosX)
	canvasPosY = math.min(canvasPosY, scrollingFrame.CanvasSize.Y.Offset - scrollingFrame.AbsoluteWindowSize.Y)
	canvasPosY = math.max(0, canvasPosY)
	return Vector2.new(canvasPosX, canvasPosY)
end

function WindowedScrollingFrame:init()
	self.state = {
		viewStart = 0,
		viewSize = 0,
		paddingStart = 0,
	}

	self.scrollingFrameRef = function(rbx)
		self.scrollingFrame = rbx
	end
end

function WindowedScrollingFrame:onSelectionChanged(selectedItem)
	if not self.scrollingFrame then
		return
	end
	if selectedItem == nil or selectedItem == self.savedSelectedObject or not selectedItem:IsDescendantOf(self.scrollingFrame) then
		return
	end
	self.savedSelectedObject = selectedItem

	local scrollingFrame = self.scrollingFrame
	local scrollingDirection = self.props.scrollingDirection or Enum.ScrollingDirection.Y
	local absoluteWindowSize = scrollingFrame.AbsoluteWindowSize
	local canvasPosition = scrollingFrame.CanvasPosition

	local axisKey = "X"
	if scrollingDirection == Enum.ScrollingDirection.Y then
		axisKey = "Y"
	end

	-- If our scrolling frame has zero height / width, let's not bother trying to
	-- recompute our sizing
	if absoluteWindowSize[axisKey] == 0 then
		return
	end

	local itemOffsetStart = self.props.itemOffsetStart or 0
	local itemOffsetEnd = self.props.itemOffsetEnd or 0
	local customScrollDist = self.props.customScrollDist or {}
	--If the selected guiobject is off-window, we move it back into the window instantly
	--Then make the motion
	local instantPos;
	local tweenTargetPos;
	if scrollingDirection == Enum.ScrollingDirection.Y then
		local topDistance = selectedItem.AbsolutePosition.Y - scrollingFrame.AbsolutePosition.Y
		local bottomDistance = (scrollingFrame.AbsolutePosition + scrollingFrame.AbsoluteWindowSize - selectedItem.AbsolutePosition - selectedItem.AbsoluteSize).Y

		local minDistTop = itemOffsetStart
		local minDistBottom = itemOffsetEnd

		if topDistance < (customScrollDist.Top or minDistTop) then
			if topDistance < 0 then
				instantPos = Vector2.new(canvasPosition.X, canvasPosition.Y + topDistance)
			end
			tweenTargetPos = Vector2.new(canvasPosition.X, canvasPosition.Y - (minDistTop - topDistance))
		elseif bottomDistance < (customScrollDist.Bottom or minDistBottom) then
			if bottomDistance < 0 then
				instantPos = Vector2.new(canvasPosition.X, canvasPosition.Y - bottomDistance)
			end
			tweenTargetPos = Vector2.new(canvasPosition.X, canvasPosition.Y + minDistBottom - bottomDistance)
		end
	elseif scrollingDirection == Enum.ScrollingDirection.X then
		local leftDistance = selectedItem.AbsolutePosition.X - scrollingFrame.AbsolutePosition.X
		local rightDistance = (scrollingFrame.AbsolutePosition + scrollingFrame.AbsoluteWindowSize - selectedItem.AbsolutePosition - selectedItem.AbsoluteSize).X

		local minDistLeft = itemOffsetStart
		local minDistRight = itemOffsetEnd

		if leftDistance < (customScrollDist.Left or minDistLeft) then
			if leftDistance < 0 then
				instantPos = Vector2.new(canvasPosition.X + leftDistance, canvasPosition.Y)
			end
			tweenTargetPos = Vector2.new(canvasPosition.X - (minDistLeft - leftDistance), canvasPosition.Y)
		elseif rightDistance < (customScrollDist.Right or minDistRight) then
			if rightDistance < 0 then
				instantPos = Vector2.new(canvasPosition.X - rightDistance, canvasPosition.Y)
			end
			tweenTargetPos = Vector2.new(canvasPosition.X + minDistRight - rightDistance, canvasPosition.Y)
		end
	end
	if instantPos then
		instantPos = clipCanvasPosition(scrollingFrame, instantPos)
		Utility.PropertyTweener(scrollingFrame, "CanvasPosition", instantPos, instantPos, 0, Utility.EaseOutQuad, true, function()
			if tweenTargetPos then
				tweenTargetPos = clipCanvasPosition(scrollingFrame, tweenTargetPos)
				Utility.PropertyTweener(scrollingFrame, "CanvasPosition", instantPos, tweenTargetPos, 0.2, Utility.EaseOutQuad, true)
			end
		end)
	end
	if not instantPos and tweenTargetPos then
		tweenTargetPos = clipCanvasPosition(scrollingFrame, tweenTargetPos)
		Utility.PropertyTweener(scrollingFrame, "CanvasPosition", canvasPosition, tweenTargetPos, 0.2, Utility.EaseOutQuad, true)
	end
end

function WindowedScrollingFrame:updateViewBounds()
	if not self.scrollingFrame then
		return
	end

	local scrollingFrame = self.scrollingFrame
	local itemSize = self.props.itemSize
	local itemsPaddingOffset = self.props.itemsPaddingOffset or 0
	local scrollingDirection = self.props.scrollingDirection or Enum.ScrollingDirection.Y
	local absoluteWindowSize = scrollingFrame.AbsoluteWindowSize
	local canvasPosition = scrollingFrame.CanvasPosition

	local axisKey = "X"
	if scrollingDirection == Enum.ScrollingDirection.Y then
		axisKey = "Y"
	end

	-- If our scrolling frame has zero height / width, let's not bother trying to
	-- recompute our sizing
	if absoluteWindowSize[axisKey] == 0 then
		return
	end

	canvasPosition = clipCanvasPosition(scrollingFrame, canvasPosition)
	local itemTotalSize = (itemSize[axisKey] + itemsPaddingOffset)
	local viewSize = math.ceil(absoluteWindowSize[axisKey] / itemTotalSize) + 1
	local viewStart = math.floor(canvasPosition[axisKey] / itemTotalSize)
	local paddingStart = math.max(0, (viewStart - 1) * itemTotalSize)
	local shouldUpdate = viewSize ~= self.state.viewSize or viewStart ~= self.state.viewStart or paddingStart ~= self.state.paddingStart
	if shouldUpdate then
		self:setState({
			viewStart = viewStart,
			viewSize = viewSize,
			paddingStart = paddingStart,
		})
	end
end

function WindowedScrollingFrame:render()
	local items = self.props.items
	local generateKey = self.props.generateKey
	local renderItem = self.props.renderItem
	local itemSize = self.props.itemSize
	local itemsPaddingOffset = self.props.itemsPaddingOffset or 0
	local scrollingDirection = self.props.scrollingDirection or Enum.ScrollingDirection.Y
	assert(scrollingDirection ~= Enum.ScrollingDirection.XY, "Can't set ScrollingDirection as XY.")

	local children = {}

	children.UIListLayout = Roact.createElement("UIListLayout", {
		Padding = UDim.new(0, itemsPaddingOffset),
		SortOrder = Enum.SortOrder.LayoutOrder,
		FillDirection = scrollingDirection == Enum.ScrollingDirection.Y and Enum.FillDirection.Vertical or Enum.FillDirection.Horizontal
	})

	if scrollingDirection == Enum.ScrollingDirection.Y then
		children.UIPadding = Roact.createElement("UIPadding", {
			PaddingTop = UDim.new(0, self.state.paddingStart)
		})
	elseif scrollingDirection == Enum.ScrollingDirection.X then
		children.UIPadding = Roact.createElement("UIPadding", {
			PaddingLeft = UDim.new(0, self.state.paddingStart)
		})
	end

	local lowerBound = math.max(1, self.state.viewStart)
	local upperBound = math.min(#items, self.state.viewStart + self.state.viewSize)

	for i = lowerBound, upperBound do
		local key = generateKey and generateKey(i) or i
		children[key] = renderItem(items[i], i)
	end

	local scrollingFrameProps = self.props.scrollingFrameProps or {}
	local canvasSize = nil
	if scrollingDirection == Enum.ScrollingDirection.Y then
		canvasSize = UDim2.new(1, 0, 0, #items * itemSize.Y + (#items - 1) * itemsPaddingOffset)
	elseif scrollingDirection == Enum.ScrollingDirection.X then
		canvasSize = UDim2.new(0, #items * itemSize.X + (#items - 1) * itemsPaddingOffset, 1, 0)
	end

	return Roact.createElement("ScrollingFrame", {
		Size = UDim2.new(1, 0, 1, 0),
		ScrollingEnabled = false, --Don't let the default select logic affect canvas position
		CanvasSize = canvasSize,
		Selectable = scrollingFrameProps.selectable or false,
		ScrollBarThickness = 0,
		ClipsDescendants = scrollingFrameProps.clipsDescendants,
		BackgroundTransparency = 1,
		ScrollingDirection = scrollingDirection,
		[Roact.Ref] = self.scrollingFrameRef,
		[Roact.Change.CanvasPosition] = function() self:updateViewBounds() end,
		[Roact.Change.AbsoluteSize] = function() self:updateViewBounds() end,
	}, children)
end

function WindowedScrollingFrame:didMount()
	self:updateViewBounds()
end

function WindowedScrollingFrame:didUpdate(prevProps, prevState)
	if not prevProps.inFocus and self.props.inFocus then
		self.conn = GuiService:GetPropertyChangedSignal("SelectedCoreObject"):connect(function()
			self:onSelectionChanged(GuiService.SelectedCoreObject)
		end)
	elseif prevProps.inFocus and not self.props.inFocus then
		Utility.DisconnectEvent(self.conn)
	end

	if self.props ~= prevProps then
		self:updateViewBounds()
	end
end

return WindowedScrollingFrame
