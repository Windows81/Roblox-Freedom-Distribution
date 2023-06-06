--[[
		Creates a Roact component that is a category selector button
		Props:
			Key : Variant - The key for the selector button.
			Text : String - The label of the button.
			Size : UDim2 - The size of the this button.
			AnchorPoint : Vector2 - The anchor point of the button.
			Position : UDim2 - The position of the button.
			LayoutOrder : int - The layout order of the button.

			Focused : bool - Is the button in focus.
			Disabled : bool - Is the button disabled. By default a disabled button will not be selectable.
			Selected : bool - Should the button be selected.
			OnSelectionGained : function(key : Variant) - Fired when the GuiObject
														is being focused on with the Gamepad selector.
			OnSelectionLost : function(key : Variant) - Fired when the Gamepad selector stops focusing on the GuiObject.
			OnActivated : function(key : Variant) - Fires when the button is activated.
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules


local Roact = require(Modules.Common.Roact)
local Immutable = require(Modules.Common.Immutable)
local GlobalSettings = require(Modules.Shell.GlobalSettings)

local RoundedButton = require(Modules.Shell.Components.Common.RoundedButton)

local SelectorButton = Roact.PureComponent:extend("SelectorButton")

local SELECTOR_ICON_SIZE_X = 15
local SELECTOR_ICON_SIZE_Y = 30

local SELECTOR_OFFSET_X = 14

function SelectorButton:init()
	self.key = self.props.Key
	self.onSelectionGained = function()
		if self.props.OnSelectionGained then self.props.OnSelectionGained(self.key) end
	end
	self.onSelectionLost = function()
		if self.props.OnSelectionLost then self.props.OnSelectionLost(self.key) end
	end
	self.onActivated = function()
		if self.props.OnActivated then self.props.OnActivated(self.key) end
	end
end

function SelectorButton:render()
	local buttonProps = {}
	local textProps = {}
	local size = self.props.Size
	local position = self.props.Position
	local anchorPoint = self.props.AnchorPoint
	local focused  = self.props.Focused
	local disabled = self.props.Disabled
	local selected = self.props.Selected
	self.layoutOrder = self.props.LayoutOrder

	buttonProps.Size = UDim2.new(1, 0, 1, 0)
	buttonProps.AnchorPoint = Vector2.new(0.5, 0.5)
	buttonProps.Position = UDim2.new(0.5, 0, 0.5, 0)

	textProps.Text = self.props.Text
	textProps.Size = UDim2.new(1, 0, 1, 0)
	textProps.AnchorPoint = Vector2.new(0, 0.5)
	textProps.Position = UDim2.new(0, 24, 0.5, 0)

	local button = Roact.createElement(RoundedButton,
	{
		Button = buttonProps,
		Text = textProps,
		Focused = focused,
		Disabled = disabled,
		Selected = selected,
		OnSelectionGained = self.onSelectionGained,
		OnSelectionLost = self.onSelectionLost,
		OnActivated = self.onActivated,
	})

	local selector;
	if focused == true then
		selector = Roact.createElement("ImageLabel",
		{
			Size = UDim2.new(0, SELECTOR_ICON_SIZE_X, 0, SELECTOR_ICON_SIZE_Y),
			Image = GlobalSettings.Images.RightArrow,
			Position = UDim2.new(1, SELECTOR_OFFSET_X, 0.5, 0),
			AnchorPoint = Vector2.new(0, 0.5),
			BackgroundTransparency = 1,
		})
	end

	local children = self.props[Roact.Children] or {}

	return Roact.createElement("Frame",
	{
		Size = size,
		Position = position,
		AnchorPoint = anchorPoint,
		LayoutOrder = self.layoutOrder,
		BackgroundTransparency = 1,
	},Immutable.JoinDictionaries(
		{
			Button = button,
			Selector = selector,
		}, children)
	)
end

return SelectorButton