--[[
		Creates a component for sidebar
		Props:
			buttons : array An array of the buttons to be added on the sidebar.
				key - string The text to be shown on the sidebar button.
				value - function() A callback which will be called when the button is activated.
			text: string - The text to be shown on the sidebar.
			inFocus: bool - The boolean which indicates whether the sidebar is open.
			selectIndex: int - The button index we try to select when the sidebar is open.
			paddingTop : UDim - The padding to apply on the top side relative to the sidebar's normal size.
			paddingBottom : UDim - The padding to apply on the bottom side relative to the sidebar's normal size.
			displayOrder: int - The order that the sidebar ScreenGui is drawn.
			onRemoveFocus : function() - Callback function when the remove focus from sidebar
			onClose: function() - Callback function when the sidebar is closed.
			actionPriority : int - The action priority on sidebar.
]]
local CoreGui = game:GetService("CoreGui")
local Modules = CoreGui.RobloxGui.Modules
local Roact = require(Modules.Common.Roact)
local GlobalSettings = require(Modules.Shell.GlobalSettings)
local RoactMotion = require(Modules.LuaApp.RoactMotion)
local SoundManager = require(Modules.Shell.SoundManager)
local Components = Modules.Shell.Components
local SoundComponent = require(Modules.Shell.Components.Common.SoundComponent)
local ContextActionEvent = require(Components.ContextActionEvent)
local Utility = require(Modules.Shell.Utility)
local INSET_X = 65
local BUTTON_SIZE_Y = 75
local SIDEBAR_SELECTION_GROUP_NAME = "SideBar"

local SideBar = Roact.PureComponent:extend("SideBar")
function SideBar:init()
	self.groupKey = SIDEBAR_SELECTION_GROUP_NAME
	self.buttonImage = GlobalSettings.Images.ButtonDefault
	self.selectionImageObject = Utility.Create "ImageLabel"({
		Name = "SelectorImage",
		BackgroundTransparency = 1,
		Visible = false
	})

	self.defaultProps = {
		buttonColor3 = GlobalSettings.Colors.WhiteButton,
		buttonTransparency = 1,
		textColor3 = GlobalSettings.Colors.WhiteText,
	}

	self.focusedProps = {
		buttonColor3 = GlobalSettings.Colors.BlueButton,
		buttonTransparency = 0,
		textColor3 = GlobalSettings.Colors.TextSelected,
	}
end

function SideBar:render()
	local props = self.props

	local onClose = function()
		self.buttons = {}
		Utility.RemoveSelectionGroup(self.groupKey)
		if props.onClose then
			props.onClose()
		end
	end

	local contents = {
		--Make it inside the title safe container
		UIPadding = Roact.createElement("UIPadding", {
			PaddingTop = props.paddingTop or UDim.new(0, 156),
			PaddingBottom = props.paddingBottom or UDim.new(0, 39)
		})
	}

	if props.buttons then
		local index = 0
		for _, buttonObj in ipairs(props.buttons) do
			index = index + 1
			local btIndex = index
			local focused = self.state.selectedIndex and self.state.selectedIndex == btIndex
			local currProps = focused and self.focusedProps or self.defaultProps
			local btText = Roact.createElement("TextLabel", {
				Size = UDim2.new(1, -INSET_X, 1, 0),
				Position = UDim2.new(0, INSET_X, 0, 0),
				AnchorPoint = Vector2.new(0, 0),
				Text = buttonObj.text,
				TextSize = GlobalSettings.TextSizes.Medium,
				TextXAlignment = Enum.TextXAlignment.Left,
				TextColor3 = currProps.textColor3,
				Font = GlobalSettings.RegularFont,
				BackgroundTransparency = 1,
			})
			local moveSelection = Roact.createElement(SoundComponent, {
				SoundName = "MoveSelection",
			})
			contents["Button"..btIndex] = Roact.createElement("ImageButton", {
				Image = self.buttonImage,
				Position = UDim2.new(0.5, 0, 0.5, 0),
				AnchorPoint = Vector2.new(0.5, 0.5),
				Size = UDim2.new(1, -1, 0, BUTTON_SIZE_Y),
				LayoutOrder = btIndex,
				ImageColor3 = currProps.buttonColor3,
				ImageTransparency = currProps.buttonTransparency,
				ScaleType = Enum.ScaleType.Slice,
				SliceCenter = Rect.new(8, 8, 9, 9),
				SelectionImageObject = self.selectionImageObject,
				BackgroundTransparency = 1,
				[Roact.Event.SelectionGained] = function()
					self:setState({
						selectedIndex = btIndex
					})
				end,
				[Roact.Event.SelectionLost] = function()
					self:setState({
						selectedIndex = Roact.None
					})
				end,
				[Roact.Event.Activated] = function()
					SoundManager:Play("ButtonPress")
					onClose()
					buttonObj.callback()
				end,
				[Roact.Ref] = function(bt)
					self.buttons = self.buttons or {}
					self.buttons[btIndex] = bt
				end,
			}, {
				ButtonText = btText,
				MoveSelection = moveSelection,
			})
		end

		if index > 0 then
			contents.UIListLayout = Roact.createElement("UIListLayout", {
				Padding = UDim.new(0, 0),
				SortOrder = Enum.SortOrder.LayoutOrder,
				HorizontalAlignment = Enum.HorizontalAlignment.Left,
				VerticalAlignment = Enum.VerticalAlignment.Top,
			})
		end
	else
		contents.TextLabel = Roact.createElement("TextLabel", {
			Size = UDim2.new(1, -INSET_X - 100, 1, 0),
			Position = UDim2.new(0, INSET_X, 0, 0),
			BorderSizePixel = 0,
			BackgroundTransparency = 1,
			Text = props.text,
			TextXAlignment = Enum.TextXAlignment.Left,
			TextYAlignment = Enum.TextYAlignment.Top,
			TextColor3 = GlobalSettings.WhiteTextColor,
			Font = GlobalSettings.RegularFont,
			FontSize = GlobalSettings.DescriptionSize,
			TextWrapped = true,
		})
	end

	local inFocus = props.inFocus
	local modalBackgroundTransparency = inFocus and GlobalSettings.ModalBackgroundTransparency or 1
	local containerPositionXScale = inFocus and 0.7 or 1
	if not inFocus then
		self.seenPressed = false
	end

	return Roact.createElement(RoactMotion.SimpleMotion, {
		defaultStyle = {
			modalBackgroundTransparency = 1,
			containerPositionXScale = 1,
		},
		style = {
			modalBackgroundTransparency = RoactMotion.spring(modalBackgroundTransparency, 600, 60),
			containerPositionXScale = RoactMotion.spring(containerPositionXScale, 600, 60),
		},
		onRested = not inFocus and onClose,
		render = function(values)
			return Roact.createElement(Roact.Portal, { target = CoreGui }, {
				SideBarGui = Roact.createElement("ScreenGui", {
					ZIndexBehavior = Enum.ZIndexBehavior.Sibling,
					DisplayOrder = props.displayOrder or 1
				}, {
					BackConnector = inFocus and Roact.createElement(ContextActionEvent, {
						name = "CloseSideBar",
						callback = function(actionName, inputState, inputObject)
							if inputObject.KeyCode == Enum.KeyCode.ButtonB then
								if inputState == Enum.UserInputState.Begin then
									self.seenPressed = true
								elseif inputState == Enum.UserInputState.End and self.seenPressed then
									self:setState({
										selectedIndex = Roact.None
									})
									if props.onRemoveFocus then
										props.onRemoveFocus()
									end
								end
							end
						end,
						binds = { Enum.UserInputType.Gamepad1, Enum.UserInputType.Gamepad2, Enum.UserInputType.Gamepad3, Enum.UserInputType.Gamepad4 },
						actionPriority = props.actionPriority
					}),
					ModalOverlay = Roact.createElement("Frame", {
						Size = UDim2.new(1, 0, 1, 0),
						BackgroundTransparency = values.modalBackgroundTransparency,
						BackgroundColor3 = GlobalSettings.ModalBackgroundColor,
						BorderSizePixel = 0,
					}, {
						SideBarContainer = Roact.createElement("Frame", {
							Size = UDim2.new(0.3, 0, 1, 0),
							Position = UDim2.new(values.containerPositionXScale, 0, 0, 0),
							BorderSizePixel = 0,
							BackgroundColor3 = GlobalSettings.OverlayColor,
							[Roact.Ref] = function(container)
								self.container = container
							end
						}, contents)
					})
				}),
			})
		end
	})
end

function SideBar:didMount()
	delay(0, function()
		if self.props.inFocus and self.container then
			Utility.RemoveSelectionGroup(self.groupKey)
			Utility.AddSelectionParent(self.groupKey, self.container)
			local trySelectIndex = self.props.selectIndex or 1
			if self.buttons and self.buttons[trySelectIndex] then
				if not self.state.selectedIndex then
					Utility.SetSelectedCoreObject(self.buttons[trySelectIndex])
				end
			else
				Utility.SetSelectedCoreObject(nil)
			end
		end
	end)
end

function SideBar:didUpdate(previousProps, previousState)
	if self.props.inFocus == previousProps.inFocus then
		return
	end
	if self.props.inFocus and self.container then
		Utility.RemoveSelectionGroup(self.groupKey)
		Utility.AddSelectionParent(self.groupKey, self.container)
		local trySelectIndex = self.props.selectIndex or 1
		if self.buttons and self.buttons[trySelectIndex] then
			if not self.state.selectedIndex then
				Utility.SetSelectedCoreObject(self.buttons[trySelectIndex])
			end
		else
			Utility.SetSelectedCoreObject(nil)
		end
	else
		Utility.RemoveSelectionGroup(self.groupKey)
	end
end

function SideBar:willUnmount()
	Utility.RemoveSelectionGroup(self.groupKey)
end

return SideBar