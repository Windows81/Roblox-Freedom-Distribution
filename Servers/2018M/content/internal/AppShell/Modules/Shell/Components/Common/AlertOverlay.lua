--[[
		A Roact alert overlay screen.
		Props:
			Key : Variant - The key of the overlay screen.
			InFocus : bool - Is the component in focus.
			Title : String - The title of the screen.
			Description : String - The description of the screen.
			ImageLabel : Roact.Component - the image to be displayed.
			ButtonTextYes : String - The text on the yes button.
			ButtonTextNo : String - The text on the no button.
			CallbackYes : function() - The callback function for the yes button.
			CallbackNo : function() - The callback function for the no button.
			CallbackBack : function() - The callback function for when back is pressed.
			DefaultButton : 0 or 1 - The default selection for the overlay screen.
							0 for Yes
							1 for No
]]
local CoreGui = game:GetService("CoreGui")
local RobloxGui = CoreGui.RobloxGui
local Modules = RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local Utility = require(Modules.Shell.Utility)
local GlobalSettings = require(Modules.Shell.GlobalSettings)
local SoundManager = require(Modules.Shell.SoundManager)

local RoundedButton = require(Modules.Shell.Components.Common.RoundedButton)
local RedirectComponent = require(Modules.Shell.Components.Common.RedirectComponent)
local AlertOverlay = Roact.PureComponent:extend("AlertOverlay")

local TEXT_LEFT_EDGE = 776
local CONFRIM_KEY = "ComfirmButtonKey"
local CANCEL_KEY = "CancelButtonKey"
function AlertOverlay:init()
	self.key = self.props.Key
	self.guiObjs = {}
	self.defaultItemKey = CANCEL_KEY
	if self.props.DefaultButton == 0 then
		self.defaultItemKey = CONFRIM_KEY
	end
	self.state =
	{
		currentItemKey = self.defaultItemKey
	}
	self.onSelectionGained = function(key)
		self:setState(
		{
			currentItemKey = key
		})
	end
end

function AlertOverlay:willUpdate(nextProps, nextState)
	self.defaultItemKey = nil
	if self.props.InFocus == nextProps.InFocus then
		return
	end
	if nextProps.InFocus then
		self.defaultItemKey = nextState.currentItemKey
	end
end


function AlertOverlay:render()
	local confirmButton;
	if not self.props.CallbackYes and self.defaultItemKey == CONFRIM_KEY then
		self.defaultItemKey = CANCEL_KEY
	elseif not self.props.CallbackNo and self.defaultItemKey == CANCEL_KEY then
		self.defaultItemKey = CONFRIM_KEY
	end
	if self.props.CallbackYes then
		local confirmButtonProps =
		{
			Position = UDim2.new(0, TEXT_LEFT_EDGE, 1, -166);
			AnchorPoint = Vector2.new(0,0),
			Size = UDim2.new(0, 320, 0, 66);
		}
		local confirmButtonTextProps =
		{
			Text = self.props.ButtonTextYes,
			TextXAlignment = Enum.TextXAlignment.Center,
		}
		confirmButton =  Roact.createElement(RoundedButton,
		{
			Button = confirmButtonProps,
			Text = confirmButtonTextProps,
			Focused = self.props.InFocus and self.state.currentItemKey == CONFRIM_KEY,
			Selected = self.defaultItemKey == CONFRIM_KEY,
			OnSelectionGained = function()
				self.onSelectionGained(CONFRIM_KEY)
			end,
			OnActivated = function()
				SoundManager:Play('ButtonPress')
				self.props.CallbackYes()
			end
		})
	end
	local cancelButton;
	if self.props.CallbackNo then
		local cancelButtonProps =
		{
			Position = UDim2.new(0, 1106, 1 ,-166),
			AnchorPoint = Vector2.new(0, 0),
			Size = UDim2.new(0, 320, 0, 66),
		}
		local cancelButtonTextProps =
		{
			Text = self.props.ButtonTextNo,
			TextXAlignment = Enum.TextXAlignment.Center,
		}
		cancelButton =  Roact.createElement(RoundedButton,
		{
			Button = cancelButtonProps,
			Text = cancelButtonTextProps,
			Focused = self.props.InFocus and self.state.currentItemKey == CANCEL_KEY,
			Selected = self.defaultItemKey == CANCEL_KEY,
			OnSelectionGained = function()
				self.onSelectionGained(CANCEL_KEY)
			end,
			OnActivated = function()
				SoundManager:Play('ButtonPress')
				self.props.CallbackNo()
			end
		})
	elseif self.defaultItemKey == CANCEL_KEY then
		self.defaultItemKey = CONFRIM_KEY
	end
	local titleText = Roact.createElement("TextLabel",
	{
		Size = UDim2.new(0, 0, 0, 0),
		Position = UDim2.new(0, TEXT_LEFT_EDGE, 0, 136),
		BackgroundTransparency = 1,
		Font = GlobalSettings.RegularFont,
		FontSize = GlobalSettings.HeaderSize,
		TextColor3 = GlobalSettings.WhiteTextColor,
		Text = self.props.Title,
		TextXAlignment = Enum.TextXAlignment.Left,
	})
	local descriptionText = Roact.createElement("TextLabel",
	{
		Size = UDim2.new(0, 762, 0, 304),
		Position = UDim2.new(0, TEXT_LEFT_EDGE, 0, 200),
		BackgroundTransparency = 1,
		TextXAlignment = Enum.TextXAlignment.Left,
		TextYAlignment = Enum.TextYAlignment.Top,
		Font = GlobalSettings.LightFont,
		FontSize = GlobalSettings.TitleSize,
		TextColor3 = GlobalSettings.WhiteTextColor,
		TextWrapped = true,
		Text = self.props.Description,
	})
	local reportIcon = self.props.ImageLabel
	if reportIcon == nil then
		reportIcon = Roact.createElement("ImageLabel",
		{
			Position = UDim2.new(0.5, 0, 0.5, 0),
			AnchorPoint = Vector2.new(0.5, 0.5),
			BackgroundTransparency = 1,
			Image = GlobalSettings.Images.LargeErrorIcon,
			Size = UDim2.new(0, 321, 0, 264),
		})
	end
	local imageContainer = Roact.createElement("Frame",
	{
		Size = UDim2.new(0, 576, 0, 642),
		Position = UDim2.new(0, 100, 0.5, 0),
		AnchorPoint = Vector2.new(0, 0.5),
		BorderSizePixel = 0,
		BackgroundTransparency = 1,
	},{
		reportImage = reportIcon
	})
	local container = Roact.createElement("Frame",
	{
		Size = UDim2.new(1, 0, 0, 640),
		AnchorPoint = Vector2.new(0, 0.5),
		Position = UDim2.new(0, 0, 0.5, 0),
		BackgroundColor3 = GlobalSettings.Colors.OverlayColor;
	},{
		ImageContainer = imageContainer,
		TitleText = titleText,
		DescriptionText = descriptionText,
		CancelButton = cancelButton,
		ConfirmButton = confirmButton,
	})
	local modalOverlay = Roact.createElement("Frame",
	{
		Size = UDim2.new(1, 0, 1, 0),
		AnchorPoint = Vector2.new(0, 0.5),
		Position = UDim2.new(0, 0, 0.5, 0),
		BackgroundColor3 = Color3.new(0, 0, 0),
		BackgroundTransparency = 0.3,
		[Roact.Ref] = function(rbx)
			self.ref = rbx
		end,
	},{
		Container = container,
	})
	local redirectObj;
	if self.props.CallbackBack then
		redirectObj = Roact.createElement(RedirectComponent,
		{
			Key = self.key,
			InFocus = true,
			RedirectBack = function()
				self.props.CallbackBack()
			end,
		})
	end
	return Roact.createElement(Roact.Portal,
	{
		target = CoreGui
	},{
		[self.key] = Roact.createElement("ScreenGui",
		{
			ZIndexBehavior = Enum.ZIndexBehavior.Sibling,
			DisplayOrder = 1
		},
		{
			ModalOverlay = modalOverlay,
			RedirectObj = redirectObj,
		}),
	})
end

function AlertOverlay:didMount()
	delay(0,function()
		Utility.AddSelectionParent(self.key, self.ref)
	end)
	SoundManager:Play("OverlayOpen")
end

function AlertOverlay:willUnmount()
	Utility.RemoveSelectionGroup(self.key)
end

return AlertOverlay