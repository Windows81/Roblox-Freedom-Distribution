--[[
		A component that is used for navigation and redirects.
			Note: The parent must be a scolling

		Props:
			Key : String
			InFocus : bool
			Scale : Vector2
			RedirectBack : function()
			RedirectLeft : function(Ref<GuiObject>) - If nil,
			RedirectRight : function(Ref<GuiObject>)
			RedirectUp : function(Ref<GuiObject>)
			RedirectDown : function(Ref<GuiObject>)
			ActionPriority : The action priority
]]
local RobloxGui = game:GetService("CoreGui").RobloxGui
local Modules = RobloxGui.Modules

local Roact = require(Modules.Common.Roact)

local ContextActionService = game:GetService("ContextActionService")

local RedirectComponent = Roact.PureComponent:extend("RedirectComponent")

local BACK_KEY = Enum.KeyCode.ButtonB

local DEFAULT_ACTION_PRIORITY = 2000

local function addBackButton(self)
	self.exitActionName = "ExitSection"..self.Key
	ContextActionService:UnbindCoreAction(self.exitActionName)
	if self.props.ActionPriority then
		ContextActionService:BindCoreActionAtPriority(self.exitActionName, self.exitAction, false, DEFAULT_ACTION_PRIORITY + self.props.ActionPriority, BACK_KEY)
	else
		ContextActionService:BindCoreAction(self.exitActionName, self.exitAction, false, BACK_KEY)
	end
end

local function removeBackButton(self)
	if self.exitActionName ~= nil then
		ContextActionService:UnbindCoreAction(self.exitActionName)
		self.exitActionName = nil
	end
end

function RedirectComponent:init()
	self.Key = self.props.Key or "RedirectComponent"
	self.exitActionName = nil
	self.backPressed = false
	self.exitAction = function(actionName, inputState, inputObject)
		if not self.props.InFocus then
			return Enum.ContextActionResult.Pass
		end
		if inputState == Enum.UserInputState.Begin then
			self.backPressed = true
		elseif inputState == Enum.UserInputState.End and self.backPressed then
			self.backPressed = false
			self.props.RedirectBack()
		end
	end
end

function RedirectComponent:render()
	local props = self.props
	local scale = props.Scale or Vector2.new(1,1)
	if props.InFocus and props.RedirectBack then
		addBackButton(self)
	else
		removeBackButton(self)
	end
	local redirectLeftButton;
	if props.InFocus and props.RedirectLeft then
		redirectLeftButton = Roact.createElement('TextButton',
		{
			Position = UDim2.new(-scale.X/2, -1, 0.5, 0),
			Size = UDim2.new(0, 2, 1+scale.Y, 0),
			AnchorPoint = Vector2.new(0.5,0.5),
			BackgroundTransparency = 1,
			Text = "",
			[Roact.Event.SelectionGained] = function(rbx)
				props.RedirectLeft(rbx)
			end,
		})
	end
	local redirectRightButton;
	if props.InFocus and props.RedirectRight then
		redirectRightButton = Roact.createElement('TextButton',
		{
			Position = UDim2.new(1+scale.X/2, 1, 0.5, 0),
			Size = UDim2.new(0, 2, 1+scale.Y, 0),
			AnchorPoint = Vector2.new(0.5,0.5),
			BackgroundTransparency = 1,
			Text = "",
			[Roact.Event.SelectionGained] = function(rbx)
				props.RedirectRight(rbx)
			end,
		})
	end
	local redirectUpButton;
	if props.InFocus and props.RedirectUp then
		redirectUpButton = Roact.createElement('TextButton',
		{
			Position = UDim2.new(0.5, 0, -scale.Y/2, -1),
			Size = UDim2.new(1+scale.X, 0, 0, 2),
			AnchorPoint = Vector2.new(0.5,0.5),
			BackgroundTransparency = 1,
			Text = "",
			[Roact.Event.SelectionGained] = function(rbx)
				props.RedirectUp(rbx)
			end,
		})
	end
	local redirectDownButton;
	if props.InFocus and props.RedirectDown then
		redirectDownButton = Roact.createElement('TextButton',
		{
			Position = UDim2.new(0.5, 0, 1+scale.Y/2, 1),
			Size = UDim2.new(1+scale.X, 0, 0, 2),
			AnchorPoint = Vector2.new(0.5,0.5),
			BackgroundTransparency = 1,
			Text = "",
			[Roact.Event.SelectionGained] = function(rbx)
					props.RedirectDown(rbx)
			end,
		})
	end
	return Roact.createElement('ScrollingFrame',
	{
		Position = UDim2.new(0.5, 0, 0.5, 0),
		Size = UDim2.new(1, 0, 1, 0),
		AnchorPoint = Vector2.new(0.5,0.5),
		BackgroundTransparency = 1,
		Selectable = false,
		ScrollingEnabled = false,
		ScrollBarThickness = 0,
		CanvasSize = UDim2.new(0, 0, 1, 0),
	},{
		RedirectLeftButton = redirectLeftButton,
		RedirectRightButton = redirectRightButton,
		RedirectUpButton = redirectUpButton,
		RedirectDownButton = redirectDownButton,
	})
end

function RedirectComponent:willUnmount()
	removeBackButton(self)
end

return RedirectComponent