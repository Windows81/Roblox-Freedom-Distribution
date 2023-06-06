--[[
		Creates a Roact component that is a rounded button
		Props:
			Button : dictionary - Config for the button.
				.Image : Content - The image of the button.
				.Size : UDim2 - Size of the button.
				.Position : UDim2 - Position of the button.
				.AnchorPoint : UDim2 - The anchor point of the button.
				.ZIndex: int - Determines the order in which GUI objects are rendered, with 10 being in front and 1 in back.
				.LayoutOrder: int - Controls the sorting priority of this button.
				.Selectable : bool - Whether or not this object should be selectable using joysticks (controller).

			Text : dictionary - A map of props for the text
				.Text : string - The label of the button.
				.Size : UDim2 - Size of the button.
				.Position : UDim2 - Position of the button.
				.AnchorPoint : The anchor point of the button.
				.Font : Font - The font used to display the given text.
				.TextSize : float - The font size in pixels.
				.TextXAlignment : TextXAlignment - Sets where text is placed on the X axis within the TextLabel.
				.ZIndex: int - Determines the order in which GUI objects are rendered, with 10 being in front and 1 in back.


			Focused : bool - Is the button in focus.
			Disabled : bool - Is the button disabled. By default a disabled button will not be selectable.
			Selected : bool - Should the button be selected.
			OnSelectionGained : bool function() -
								Fired when the GuiObject is being focused on with the Gamepad selector.
								Return true if it should be focused. False otherwise.
			OnSelectionLost : bool function() -
								Fired when the Gamepad selector stops focusing on the GuiObject.
								Return false if it should be un-focused. True otherwise.
			OnActivated : function() - Fires when the button is activated.

			HideSelectionImage : bool - Whether or not to hide the selection object

			DefaultProps : dictionary a map for the default props of the button.
				.ImageColor3 : Color3
				.ImageTransparency : float
				.TextColor3 : Color3

			FocusedProps : dictionary a map for the focused props of the button.
				.ImageColor3 : Color3
				.ImageTransparency : float
				.TextColor3 : Color3

			DisabledProps : dictionary a map for the disabled props of the button.
				.ImageColor3 : Color3
				.ImageTransparency : float
				.TextColor3 : Color3
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local Immutable = require(Modules.Common.Immutable)
local Utility = require(Modules.Shell.Utility)
local GlobalSettings = require(Modules.Shell.GlobalSettings)
local SoundComponent = require(Modules.Shell.Components.Common.SoundComponent)
local RoundedButton = Roact.PureComponent:extend("RoundedButton")

function RoundedButton:init()
	self.selectionImageObject = Utility.Create "ImageLabel"
	{
		Name = "SelectorImage",
		Image = GlobalSettings.Images.ButtonSelector,
		Position = UDim2.new(0, -7, 0, -7),
		Size = UDim2.new(1, 14, 1, 14),
		BackgroundTransparency = 1,
		ScaleType = Enum.ScaleType.Slice,
		SliceCenter = Rect.new(31, 31, 63, 63),
	}

	self.defaultProps =
	{
		ImageColor3 = GlobalSettings.Colors.WhiteButton,
		ImageTransparency = 0.8,
		TextColor3 = GlobalSettings.Colors.WhiteText,
	}
	self.focusedProps =
	{
		ImageColor3 = GlobalSettings.Colors.BlueButton,
		ImageTransparency = 0,
		TextColor3 = GlobalSettings.Colors.TextSelected,
	}
	self.disabledProps =
	{
		ImageColor3 = GlobalSettings.Colors.WhiteButton,
		ImageTransparency = 1,
		TextColor3 = GlobalSettings.Colors.WhiteText,
	}
	self.buttonImage = GlobalSettings.Images.ButtonDefault

	--TODO: Change to new Ref API
	self.onCreate = function(rbx)
		self.ref = rbx
	end
end

function RoundedButton:render()
	local button = self.props.Button or {}
	local text = self.props.Text or {}

	local inputDefaultProps = self.props.DefaultProps or {}
	local defaultProps = {}
	for k in pairs(self.defaultProps) do
		defaultProps[k] = inputDefaultProps[k] or self.defaultProps[k]
	end

	local inputFocusedProps = self.props.FocusedProps or {}
	local focusedProps = {}
	for k in pairs(self.focusedProps) do
		focusedProps[k] = inputFocusedProps[k] or self.focusedProps[k]
	end

	local inputDisabledProps = self.props.DisabledProps or {}
	local disabledProps = {}
	for k in pairs(self.disabledProps) do
		disabledProps[k] = inputDisabledProps[k] or self.disabledProps[k]
	end

	if self.props.HideSelectionImage then
		self.selectionImageObject.Visible = false
	else
		self.selectionImageObject.Visible = true
	end
	local selectable = true
	if button.Selectable == false then
		selectable = false
	end
	local currentProps = defaultProps
	if self.props.Disabled then
		currentProps = disabledProps
		selectable = button.Selectable or false
	elseif self.props.Focused then
		currentProps = focusedProps
	end
	local baseButtonProps =
	{
		Image = self.buttonImage,
		Size = UDim2.new(1, 0, 1, 0),
		Position = UDim2.new(0.5, 0, 0.5, 0),
		AnchorPoint = Vector2.new(0.5, 0.5),
		Selectable = selectable,
		[Roact.Ref] = self.onCreate,
		[Roact.Event.SelectionGained] = self.props.OnSelectionGained,
		[Roact.Event.SelectionLost] = self.props.OnSelectionLost,
		[Roact.Event.Activated] = self.props.OnActivated,
		ImageColor3 = currentProps.ImageColor3,
		ImageTransparency = currentProps.ImageTransparency,
		ScaleType = Enum.ScaleType.Slice,
		SliceCenter = Rect.new(8, 8, 9, 9),
		SelectionImageObject = self.selectionImageObject,
		BackgroundTransparency = 1,
	}
	local buttonProps = Immutable.JoinDictionaries(baseButtonProps, button)

	local baseTextProps =
	{
		Text = "",
		Size = UDim2.new(1, 0, 1, 0),
		Position = UDim2.new(0.5, 0, 0.5, 0),
		AnchorPoint = Vector2.new(0.5, 0.5),
		Font = GlobalSettings.Fonts.Regular,
		TextSize = GlobalSettings.TextSizes.Button,
		TextXAlignment = Enum.TextXAlignment.Left,
		TextColor3 = currentProps.TextColor3,
		TextTransparency = currentProps.TextTransparency,
		BackgroundTransparency = 1,
	}

	local textProps = Immutable.JoinDictionaries(baseTextProps, text)

	local textLabel = Roact.createElement("TextLabel", textProps)
	local moveSelection = Roact.createElement(SoundComponent,
		{
			SoundName = "MoveSelection",
		}
	)

	local children = self.props[Roact.Children] or {}

	return Roact.createElement("ImageButton",
		buttonProps,
		Immutable.JoinDictionaries(
			{
				Label = textLabel,
				MoveSelection = moveSelection,
			}, children)
	)
end

function RoundedButton:didMount()
	delay(0, function()
		if self.props.Selected then
			Utility.SetSelectedCoreObject(self.ref)
		end
	end)
end

function RoundedButton:didUpdate(previousProps, previousState)
	if not previousProps.Selected and self.props.Selected then
		Utility.SetSelectedCoreObject(self.ref)
	end
end

return RoundedButton
