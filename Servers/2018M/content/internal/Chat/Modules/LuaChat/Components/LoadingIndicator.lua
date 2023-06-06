local CoreGui = game:GetService("CoreGui")
local RunService = game:GetService("RunService")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local Constants = require(LuaChat.Constants)
local Create = require(LuaChat.Create)
local FlagSettings = require(LuaApp.FlagSettings)
local LoadingBar = require(LuaApp.Components.LoadingBar)
local Roact = require(Common.Roact)

local LOADING_INDICATOR_WIDTH = 70
local LOADING_INDICATOR_HEIGHT = 16
local DOT_COUNT = 3
local DOT_ANIMATION_SPEED_MULTIPLIER = 1.75
local DOT_BASE_RELATIVE_HEIGHT = 0.7
local DOT_BASE_RELATIVE_WIDTH = 0.7
local DOT_HEIGHT_LERP_AMPLITUDE = 0.3

local LoadingIndicator = {}

local function makeDot()
	return Create.new "ImageLabel" {
		Name = "DotContainer",
		BackgroundTransparency = 1,
		Size = UDim2.new(1, 0, 1, 0),
		SizeConstraint = Enum.SizeConstraint.RelativeYY,

		Create.new "Frame" {
			Name = "Dot",
			BorderSizePixel = 0,
			Size = UDim2.new(1, 0, 1, 0),
			SizeConstraint = Enum.SizeConstraint.RelativeYY,
			Position = UDim2.new(0.5, 0, 0.5, 0),
			AnchorPoint = Vector2.new(0.5, 0.5)
		},
	}
end

local function renderLoadingDots(self)
	if not self.rbx.Visible then
		return
	end
	local dotsTime = (time() * DOT_ANIMATION_SPEED_MULTIPLIER) % #self.dots
	for i, dot in ipairs(self.dots) do
		local dotHeight = DOT_BASE_RELATIVE_HEIGHT
		if dotsTime >= i - 1 and dotsTime <= i then
			dotHeight = DOT_BASE_RELATIVE_HEIGHT + DOT_HEIGHT_LERP_AMPLITUDE * math.sin(math.pi * (dotsTime % 1))
			local colorAlpha = math.sin(math.pi * (dotsTime % 1))
			dot.Dot.BackgroundColor3 = Constants.Color.GRAY3:lerp(Constants.Color.BLUE_PRIMARY, colorAlpha)
		else
			dot.Dot.BackgroundColor3 = Constants.Color.GRAY3
		end
		dot.Dot.Size = UDim2.new(DOT_BASE_RELATIVE_WIDTH, 0, dotHeight, 0)
	end
end

function LoadingIndicator.new(appState, scale)
	scale = scale or 1

	local self = {}
	self.connections = {}

	self.rbx = Create.new "Frame" {
		Name = "LoadingIndicator",
		BackgroundTransparency = 1,
		Size = UDim2.new(0, scale * LOADING_INDICATOR_WIDTH, 0, scale * LOADING_INDICATOR_HEIGHT)
	}

	local platform = appState.store:GetState().Platform
	local isLuaHomePageEnabled = FlagSettings.IsLuaHomePageEnabled(platform)
	local isLuaGamesPageEnabled = FlagSettings.IsLuaGamesPageEnabled(platform)
	self.isLoadingBarEnabled = isLuaHomePageEnabled and isLuaGamesPageEnabled

	if self.isLoadingBarEnabled then
		self.loadingBar = Roact.mount(Roact.createElement(LoadingBar), self.rbx)
	else -- use dots loading indicator for non-lua pages
		self.dots = {}
		for i = 1, DOT_COUNT do
			local value = (i - 1) / (DOT_COUNT - 1)

			local dot = makeDot()
			dot.Position = UDim2.new(value, 0, 0.5, 0)
			dot.AnchorPoint = Vector2.new(value, 0.5)
			dot.Parent = self.rbx

			table.insert(self.dots, dot)
		end
	end

	setmetatable(self, LoadingIndicator)

	do
		local connection = self.rbx.AncestryChanged:Connect(function(object, parent)
			if object == self.rbx and parent == nil then
				self:Destroy()
			end
		end)
		table.insert(self.connections, connection)
	end

	if not self.isLoadingBarEnabled then
		local connection = RunService.RenderStepped:Connect(function()
			renderLoadingDots(self)
		end)
		table.insert(self.connections, connection)
	end

	return self
end

function LoadingIndicator:SetZIndex(index)
	self.rbx.ZIndex = index
	if self.isLoadingBarEnabled then
		self.loadingBar.ZIndex = index
	else
		for _, dot in ipairs(self.dots) do
			dot.ZIndex = index
			dot.Dot.ZIndex = index
		end
	end
end

function LoadingIndicator:SetVisible(visible)
	self.rbx.Visible = visible
end

function LoadingIndicator:Destroy()
	if self.isLoadingBarEnabled then
		Roact.unmount(self.loadingBar)
	end

	for _, connection in ipairs(self.connections) do
		connection:Disconnect()
	end

	self.rbx:Destroy()
	self.connections = {}
end

LoadingIndicator.__index = LoadingIndicator

return LoadingIndicator