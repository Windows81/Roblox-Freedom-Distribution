local Modules = game:GetService("CoreGui").RobloxGui.Modules
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local BaseScreen = require(LuaChat.Views.Phone.BaseScreen)
local Create = require(LuaChat.Create)
local Constants = require(LuaChat.Constants)
local GameShareComponent = require(LuaChat.Components.GameShareComponent)

local SetTabBarVisible = require(LuaApp.Actions.SetTabBarVisible)

local GameShareView = BaseScreen:Template()
GameShareView.__index = GameShareView

function GameShareView.new(appState, route)
	local self = {}
	self.appState = appState
	self.route = route

	setmetatable(self, GameShareView)

	local innerFrame = Create.new"Frame" {
		Name = "InnerFrame",
		Size = UDim2.new(1, 0, 1, 0),
		Position = UDim2.new(0.5, 0, 0, 0),
		AnchorPoint = Vector2.new(0.5, 0),
		BackgroundColor3 = Constants.Color.GRAY5,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		LayoutOrder = 2,
		Create.new("UIListLayout") {
			Name = "ListLayout",
			SortOrder = Enum.SortOrder.LayoutOrder,
		},
	}

	self.gameShareComponent = GameShareComponent.new(appState, route.parameters.placeId, innerFrame)
	self.rbx = self.gameShareComponent.rbx

	return self
end

function GameShareView:Start()
	self.gameShareComponent:Start()
	self.prevTabBarVisibility = self.appState.store:getState().TabBarVisible

	BaseScreen.Start(self)

	self.appState.store:dispatch(SetTabBarVisible(false))
end

function GameShareView:Stop()
	self.gameShareComponent:Stop()

	BaseScreen.Stop(self)

	self.appState.store:dispatch(SetTabBarVisible(self.prevTabBarVisibility))
end

function GameShareView:Destruct()
	self.gameShareComponent:Destruct()

	BaseScreen.Destruct(self)
end

return GameShareView