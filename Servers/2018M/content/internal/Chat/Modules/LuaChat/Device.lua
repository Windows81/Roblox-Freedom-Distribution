local UserInputService = game:GetService("UserInputService")
local GuiService = game:GetService("GuiService")
local RunService = game:GetService("RunService")
local CoreGui = game:GetService("CoreGui")
local Workspace = game:GetService("Workspace")

local Modules = CoreGui.RobloxGui.Modules

local Config = require(Modules.LuaApp.Config)
local Create = require(Modules.LuaChat.Create)
local SetPlatform = require(Modules.LuaApp.Actions.SetPlatform)
local SetFormFactor = require(Modules.LuaApp.Actions.SetFormFactor)
local FormFactor = require(Modules.LuaApp.Enum.FormFactor)

local STATUS_BAR_HEIGHT_IOS = 20
local STATUS_BAR_HEIGHT_ANDROID = 24
local NAV_BAR_HEIGHT = 44

local FlagSettings = require(Modules.LuaApp.FlagSettings)

local Device = {}

local function simulateIOS()
	local statusBarSize = Vector2.new(0, STATUS_BAR_HEIGHT_IOS)
	local navBarSize = Vector2.new(0, NAV_BAR_HEIGHT)
	local bottomBarSize = Vector2.new(0, 0)
	--Pcall because Tests have a lower security context
	pcall(function()
		UserInputService:SendAppUISizes(statusBarSize, navBarSize, bottomBarSize)
		GuiService:SetSafeZoneOffsets(0, 0, 0, 0)
	end)
end

local function simulateAndroid()
	local statusBarSize = Vector2.new(0, STATUS_BAR_HEIGHT_ANDROID)
	local navBarSize = Vector2.new(0, NAV_BAR_HEIGHT)
	local bottomBarSize = Vector2.new(0, 0)
	--Pcall because Tests have a lower security context
	pcall(function()
		UserInputService:SendAppUISizes(statusBarSize, navBarSize, bottomBarSize)
		GuiService:SetSafeZoneOffsets(0, 0, 0, 0)
	end)

	local screenGui = Create.new "ScreenGui" {
		Name = "StudioShellSimulation",
		DisplayOrder = 10,

		Create.new "Frame" {
			Name = "StatusBar",
			Position = UDim2.new(0, 0, 0, 0),
			Size = UDim2.new(1, 0, 0, UserInputService.StatusBarSize.Y),
			BorderSizePixel = 0,
			BackgroundColor3 = Color3.fromRGB(117, 117, 117),
		}
	}
	screenGui.Parent = CoreGui
end

local function getDevicePlatform()
	if _G.__TESTEZ_RUNNING_TEST__ then
		return Enum.Platform.None
	end

	return UserInputService:GetPlatform()
end

function Device.simulatePlatformIfInStudio(store)
	if not FlagSettings.IsLuaAppDeterminingFormFactorAndPlatform() then
		local function setFormFactor(viewportSize)
			local formFactor = FormFactor.TABLET
			if viewportSize.X <= 1 then
				-- Camera.ViewportSize hasn't been properly set yet
				formFactor = FormFactor.UNKNOWN
			elseif viewportSize.Y > viewportSize.X then
				formFactor = FormFactor.PHONE
			end
			store:dispatch(SetFormFactor(formFactor))
		end
		local camera = Workspace:WaitForChild("Camera")
		setFormFactor(camera.ViewportSize)
		camera.Changed:Connect(function(prop)
			if prop == "ViewportSize" then
				setFormFactor(camera.ViewportSize)
			end
		end)
	end

	if RunService:IsStudio() then
		store:dispatch(SetPlatform(Config.General.SimulatePlatform))

		if Config.General.SimulatePlatform == Enum.Platform.IOS then
			simulateIOS()
		elseif Config.General.SimulatePlatform == Enum.Platform.Android then
			simulateAndroid()
		end
	else
		-- We only want to set Platform here if:
		-- 1) We are not in Studio
		-- 2) LuaApp is not determining Platform in LuaApp/App.lua
		if not FlagSettings.IsLuaAppDeterminingFormFactorAndPlatform() then
			local platform = getDevicePlatform()
			store:dispatch(SetPlatform(platform))
		end
	end
end

return Device