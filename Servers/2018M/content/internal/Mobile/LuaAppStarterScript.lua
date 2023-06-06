local CoreGui = game:GetService("CoreGui")
local UserInputService = game:GetService("UserInputService")
local CorePackages = game:GetService("CorePackages")

local Modules = CoreGui.RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local App = require(Modules.LuaApp.Components.App)
local LuaErrorReporter = require(Modules.Common.LuaErrorReporter)
local FlagSettings = require(Modules.LuaApp.FlagSettings)

if not UserSettings().GameSettings:InStudioMode() then
	-- listen and report errors
	local errorReporter = LuaErrorReporter.new()
	errorReporter:setCurrentApp("Mobile")
	errorReporter:startQueueTimers()
end

-- Common Setup
if game.Players.LocalPlayer == nil then
	game.Players.PlayerAdded:Wait()
end

-- Reduce render quality to optimize performance
if settings():GetFFlag("AppShellManagementRefactor4") then
	local renderSteppedConnection = nil
	renderSteppedConnection = game:GetService("RunService").RenderStepped:connect(function()
		if renderSteppedConnection then
			renderSteppedConnection:Disconnect()
		end
		settings().Rendering.QualityLevel = 1
	end)
else
	settings().Rendering.QualityLevel = 1
end

-- Update LuaApp.FlagSettings using the fact that this script is loaded.
FlagSettings:SetIsLuaAppStarterScriptEnabled(true)

local root = Roact.createElement(App)
Roact.mount(root, CoreGui, "App")

-- Run tests when shift+alt+ctrl+T is pressed
UserInputService.InputEnded:connect(function(input, gameProcessed)
	if input.UserInputType == Enum.UserInputType.Keyboard and
		input.KeyCode == Enum.KeyCode.T and
		UserInputService:IsKeyDown(Enum.KeyCode.LeftShift) and
		UserInputService:IsKeyDown(Enum.KeyCode.LeftControl) and
		UserInputService:IsKeyDown(Enum.KeyCode.LeftAlt)
	then
		local TestEZ = require(CorePackages.TestEZ)

		TestEZ.run(Modules.LuaApp, function(results)
			TestEZ.Reporters.TextReporter.report(results)
		end)
	end
end)
