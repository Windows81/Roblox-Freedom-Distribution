--[[
		Create a Roact toggle button
		Props:
			Key : Variant - The key for the toggle button.
			Text : String - The text of the button.
			Size : UDim2 - The size of the this button.
			AnchorPoint : Vector2 - The anchor point of the button.
			Position : UDim2 - The position of the button.

			Toggle : bool - Whether or not the button is toggled or not.
			Focused : bool - Is the button selected.
			Disabled : bool - Whether or not this button is disabled.
			Selected : bool - Should the button be selected.
			Selectable : bool - Whether or not the button is selectable.
			OnSelectionGained : function(key : Variant) - Fired when the GuiObject is being focused on with the Gamepad selector.
			OnSelectionLost : function(key : Variant) - Fired when the Gamepad selector stops focusing on the GuiObject.
			OnActivated : function() - Fires when the button is activated.
]]

local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local Immutable = require(Modules.Common.Immutable)
local GlobalSettings = require(Modules.Shell.GlobalSettings)

local RoundedButton = require(Modules.Shell.Components.Common.RoundedButton)

local ToggleButton = Roact.Component:extend("ToggleButton")

local TOGGLE_ICON_SIZE = 32

local TOGGLE_ICON_OFFSET_X = 20

function ToggleButton:init()
	self.key = self.props.Key
	self.state =
	{
		selected = false,
		active = false,
	}
	self.onSelectionGained = function()
		if self.props.OnSelectionGained then self.props.OnSelectionGained(self.key) end
	end
	self.onSelectionLost = function()
		if self.props.OnSelectionLost then self.props.OnSelectionLost(self.key) end
	end
	self.onActivated = function()
		if self.props.OnActivated then self.props.OnActivated() end
	end
end

function ToggleButton:render()
	local buttonProps = {}
	local textProps = {}
	local size = self.props.Size
	local position = self.props.Position
	local anchorPoint = self.props.AnchorPoint
	local focused  = self.props.Focused
	local disabled = self.props.Disabled
	local selected = self.props.Selected
	--Default is unknown since its not on or off
	local iconColor = GlobalSettings.Colors.StatusIconUnknown
	if self.props.Toggle == true then
		iconColor = GlobalSettings.Colors.StatusIconEnabled
	elseif self.props.Toggle == false then
		iconColor = GlobalSettings.Colors.StatusIconDisabled
	end

	buttonProps.Size = UDim2.new(1, 0, 1, 0)
	buttonProps.AnchorPoint = Vector2.new(0.5, 0.5)
	buttonProps.Position = UDim2.new(0.5, 0, 0.5, 0)
	buttonProps.Selectable = self.props.Selectable

	textProps.Text = self.props.Text
	textProps.Size = UDim2.new(1, 0, 1, 0)
	textProps.AnchorPoint = Vector2.new(0, 0.5)
	textProps.Position = UDim2.new(0, TOGGLE_ICON_SIZE+2*TOGGLE_ICON_OFFSET_X, 0.5, 0)

	local toggleImage = Roact.createElement("ImageLabel",
	{
		Size = UDim2.new(0, TOGGLE_ICON_SIZE, 0, TOGGLE_ICON_SIZE),
		Image = GlobalSettings.Images.EnabledStatusIcon,
		ImageColor3 = iconColor,
		Position = UDim2.new(0, TOGGLE_ICON_OFFSET_X, 0.5, 0),
		AnchorPoint = Vector2.new(0, 0.5),
		BackgroundTransparency = 1,
	})

	local button =  Roact.createElement(RoundedButton,
	{
		Button = buttonProps,
		Text = textProps,
		Focused = focused,
		Disabled = disabled,
		Selected = selected,
		OnSelectionGained = self.onSelectionGained,
		OnSelectionLost = self.onSelectionLost,
		OnActivated = self.onActivated,
	},{
		ToggleImage = toggleImage,
	})

	local children = self.props[Roact.Children] or {}
	return Roact.createElement("Frame",
	{
		Size = size,
		Position = position,
		AnchorPoint = anchorPoint,
		BackgroundTransparency = 1,
	}, Immutable.JoinDictionaries(
		{
			Button = button,
		}, children))
end

return ToggleButton