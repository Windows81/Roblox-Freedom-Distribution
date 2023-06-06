--[[
		Creates a Roact component provides a vertical list menu for multiple elements
		Props:
			Key : Variant - The key for this category menu. The key cannot be changed after init.
			InFocus : bool - Is the component in focus.
			Navigator : Navigator - The Navigator object.
			DefaultCategoryFocus : Variant - This is the key of the default focus button.
			DefaultCategoryKey : Variant - The default selection of the category menu.
			Categories : Categories - An object that provides data needed for the creating the categories
						The object must have an order mapping and a StringKeys mapping for localization.
				E.g.
					Categories[CategoryKey].Key = "Category"
					Categories[CategoryKey].Order = 1
					Categories[CategoryKey].StringKey = "CategoryStringKey"

			OnSelectSection : function(Key : Variant) - Callback for when a section of the key is select.
			OnLeaveSection : function(Key : Variant) - Callback for when a section of the key is no longer selected.
			EnterSection : function() - Callback functin to enter the menu section.
			RedirectUp : function() - Callback functin when redirect up.
			RedirectDown : function() - Callback functin when redirect down.
			ActionPriority : int - The action priority.
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local Utility = require(Modules.Shell.Utility)
local LocalizedStrings = require(Modules.Shell.LocalizedStrings)

local VerticalListView = require(Modules.Shell.Components.Common.VerticalListView)
local SelectorButton = require(Modules.Shell.Components.Common.SelectorButton)
local RedirectComponent = require(Modules.Shell.Components.Common.RedirectComponent)

local CategoryMenuView = Roact.PureComponent:extend("CategoryMenuView")

local BUTTON_WIDTH = 360
local BUTTON_HEIGHT = 80

function CategoryMenuView:OnSelectSection(key)
	if self.state.currentSectionKey ~= key then
		self:setState(
		{
			currentSectionKey = key,
		})
	end
end

function CategoryMenuView:init()
	self.key = self.props.Key
	self.defaultCategoryKey = self.props.DefaultCategoryKey
	self.defaultCategoryFocus = self.defaultCategoryKey or self.props.DefaultCategoryFocus
	self.state =
	{
		currentSectionKey = self.props.DefaultCategoryFocus,
	}
	self.getCurrentPageIndex = function()
		return self.CurrentSection
	end
end

function CategoryMenuView:willUpdate(nextProps, nextState)
	self.defaultCategoryKey = nil
	if self.props.InFocus == nextProps.InFocus then
		return
	end
	if nextProps.InFocus then
		self.defaultCategoryKey = nextState.currentSectionKey or self.props.DefaultCategoryKey
	end
end

function CategoryMenuView:render()
	self.categories = self.props.Categories
	local buttons = {}
	for k in pairs(self.categories) do
		buttons[k] = Roact.createElement(SelectorButton,
		{
			Size = UDim2.new(0, BUTTON_WIDTH, 0, BUTTON_HEIGHT),
			AnchorPoint = Vector2.new(0, 0),
			Text = LocalizedStrings:LocalizedString(self.categories[k].StringKey),
			Key = k,
			LayoutOrder = self.categories[k].Order,
			Focused = self.state.currentSectionKey == k,
			Selected = self.defaultCategoryKey == k,
			OnSelectionGained = function(key)
				self:OnSelectSection(key)
				if self.props.OnSelectSection then
					self.props.OnSelectSection(key)
				end
			end,
			OnSelectionLost = self.props.OnLeaveSection,
			OnActivated = self.props.EnterSection,
		})
	end

	local navObj = Roact.createElement(RedirectComponent,
	{
		ActionPriority = self.props.ActionPriority,
		Key = self.key,
		InFocus = self.props.InFocus,
		RedirectRight = self.props.EnterSection,
		RedirectUp = self.props.RedirectUp,
		RedirectDown = self.props.RedirectDown,
	})

	local buttonView = Roact.createElement(VerticalListView,
	{
		PaddingTop = UDim.new(0.005, 0),
		PaddingBottom = UDim.new(0.005, 0),
		Spacing = UDim.new(0.025, 0),
		ScrollBarThickness = 0,
		Items = buttons,
		HorizontalAlignment = Enum.HorizontalAlignment.Left,
		ScrollingEnabled = false,
	})

	return Roact.createElement("Frame",
	{
		Size = UDim2.new(1, 0, 1, 0),
		AnchorPoint = Vector2.new(0, 0),
		Position = UDim2.new(0, 0, 0, 0),
		BackgroundTransparency = 1,
		Selectable = false,
		[Roact.Ref] = function(rbx)
			self.ref = rbx
		end,
	},{
		NavObj = navObj,
		ButtonView = buttonView,
	})
end

function CategoryMenuView:didMount()
	delay(0, function()
		if self.props.InFocus and self.ref then
			Utility.RemoveSelectionGroup(self.key)
			Utility.AddSelectionParent(self.key, self.ref)
		end
	end)
end

function CategoryMenuView:didUpdate(previousProps, previousState)
	if self.props.InFocus == previousProps.InFocus then
		return
	end
	if self.props.InFocus and self.ref then
		Utility.RemoveSelectionGroup(self.key)
		Utility.AddSelectionParent(self.key, self.ref)
	else
		Utility.RemoveSelectionGroup(self.key)
	end
end

function CategoryMenuView:willUnmount()
	Utility.RemoveSelectionGroup(self.key)
end

return CategoryMenuView