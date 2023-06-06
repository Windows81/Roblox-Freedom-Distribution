local CoreGui = game:GetService("CoreGui")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")

local Modules = CoreGui.RobloxGui.Modules

local AppNameEnum = require(Modules.Mobile.AppNameEnum)
local Create = require(Modules.Mobile.Create)
local Constants = require(Modules.Mobile.Constants)
local AppGui = require(Modules.LuaApp.Legacy.AvatarEditor.AppGui)

local LuaAppConstants = require(Modules.LuaApp.Constants)

local AvatarEditorSetup = {}

function AvatarEditorSetup:Initialize(notifyAppReady, useRoactLuaApp)
	--This is to cover the sky while loading, and also prevent the sky from flashing in when the global gui inset changes
	local screenGui

	if not UserSettings().GameSettings:InStudioMode() then
		screenGui = Create.new "ScreenGui" {
			Name = "SkyCoverGui",
			DisplayOrder = 1,

			Create.new "Frame" {
				Name = "HackHeader",
				Position = UDim2.new(0, 0, 0, 0),
				Size = UDim2.new(1, 0, 0, UserInputService.NavBarSize.Y+UserInputService.StatusBarSize.Y),
				BorderSizePixel = 0,
				BackgroundColor3 = Constants.Color.BLUE_PRESSED,
			},
			Create.new "Frame" {
				Name = "HackBody",
				Position = UDim2.new(0, 0, 0, UserInputService.NavBarSize.Y+UserInputService.StatusBarSize.Y),
				Size = UDim2.new(1, 0, 1, 200),
				BorderSizePixel = 0,
				BackgroundColor3 = Constants.Color.WHITE,
			},
		}
	else
		screenGui = Create.new "ScreenGui" {
			Name = "SkyCoverGui",
			DisplayOrder = 1,

			Create.new "Frame" {
				Name = "HackHeader",
				Position = UDim2.new(0, 0, 0, 0),
				Size = UDim2.new(1, 0, 0, 64),
				BorderSizePixel = 0,
				BackgroundColor3 = Constants.Color.BLUE_PRESSED,
			},
			Create.new "Frame" {
				Name = "HackBody",
				Position = UDim2.new(0, 0, 0, 64),
				Size = UDim2.new(1, 0, 1, 200),
				BorderSizePixel = 0,
				BackgroundColor3 = Constants.Color.WHITE,
			},
		}
	end

	local function adjustScreenGuiLayout()
		local headerHeight = UserInputService.NavBarSize.Y+UserInputService.StatusBarSize.Y
		screenGui.HackHeader.Size = UDim2.new(1, 0, 0, headerHeight)
		screenGui.HackBody.Position = UDim2.new(0, 0, 0, headerHeight)
	end

	local navBarChanged = UserInputService:GetPropertyChangedSignal("NavBarSize")
	navBarChanged:Connect(function()
		adjustScreenGuiLayout()
	end)

	local statusBarChanged = UserInputService:GetPropertyChangedSignal("StatusBarSize")
	statusBarChanged:Connect(function()
		adjustScreenGuiLayout()
	end)

	screenGui.Parent = CoreGui

	if useRoactLuaApp then
		screenGui.Enabled = false
	end

	--[[
		As long as initializing AvatarEditorMain requires a yield, it has to run in a
		spawned task.  It is then possible for the user to switch apps in the middle of
		initialization.  So, openAvatarEditor and closeAvatarEditor first check to see
		if it's currently initializing, and if it is, they set a bool indicating whether
		to call Start() when initialization is done.
	]]
	local startAvatarEditorAfterInitializing = false

	self.openAvatarEditor = function()
		startAvatarEditorAfterInitializing = true
	end

	self.closeAvatarEditor = function()
		startAvatarEditorAfterInitializing = false
	end

	local function avatarEditorInitialization()
		spawn(function()
			self.AppGui = nil

			if not useRoactLuaApp then
				local header
				if not UserSettings().GameSettings:InStudioMode() then
					header = require(Modules.LuaApp.Legacy.AvatarEditor.Header).new("Avatar",
						UserInputService.NavBarSize.Y, UserInputService.StatusBarSize.Y)

					local headerHeight = UserInputService.StatusBarSize.Y + UserInputService.NavBarSize.Y
					self.AppGui = AppGui(
						UDim2.new(0, 0, 0,  headerHeight),
						UDim2.new(1, 0, 1, -headerHeight))

					local function updateUIDimensions()
						header:SetNavAndStatusBarHeight(UserInputService.NavBarSize.Y, UserInputService.StatusBarSize.Y)
						local headerHeight = UserInputService.NavBarSize.Y + UserInputService.StatusBarSize.Y
						self:UpdateTopBarHeight(headerHeight)
					end

					UserInputService:GetPropertyChangedSignal("NavBarSize"):Connect( updateUIDimensions )
					UserInputService:GetPropertyChangedSignal("StatusBarSize"):Connect( updateUIDimensions )
				else
					local navBarHeight = 44
					local statusBarHeight = 20

					header = require(Modules.LuaApp.Legacy.AvatarEditor.Header).new("Avatar",
						navBarHeight, statusBarHeight)

					local headerHeight = navBarHeight + statusBarHeight
					self.AppGui = AppGui(
						UDim2.new(0, 0, 0,  headerHeight),
						UDim2.new(1, 0, 1, -headerHeight))
				end
				header.rbx.Parent = self.AppGui.ScreenGui
			else
				-- Sync with default value in LuaApp topbar reducer
				local topBarHeight = LuaAppConstants.TOP_BAR_SIZE
				self.AppGui = AppGui(
					UDim2.new(0, 0, 0,  topBarHeight),
					UDim2.new(1, 0, 1, -topBarHeight))
			end

			AvatarEditorMain =
				require(Modules.LuaApp.Legacy.AvatarEditor.AvatarEditorMain)
					.new(self.AppGui)

			local function startAvatarEditor()
				if useRoactLuaApp then
					screenGui.Enabled = true
				end
				screenGui.HackBody.Visible = false
				AvatarEditorMain:Start()

				-- Staging broadcasting of APP_READY to accomodate for unpredictable
				-- delay on the native side.
				-- Once Lua tab bar is integrated, there will be no use for this
				notifyAppReady(AppNameEnum.AvatarEditor)
			end

			if startAvatarEditorAfterInitializing then
				startAvatarEditor()
			end

			self.openAvatarEditor = startAvatarEditor

			self.closeAvatarEditor = function()
				screenGui.HackBody.Visible = true
				AvatarEditorMain:Stop()
				if useRoactLuaApp then
					screenGui.Enabled = false
				end
			end
		end)
	end

	if settings():GetFFlag("AppShellManagementRefactor4") then
		local hasRunInitialization = false
		local renderSteppedConnection = nil
		renderSteppedConnection = RunService.RenderStepped:connect(function()
			if not hasRunInitialization then
				hasRunInitialization = true
				if renderSteppedConnection then
					renderSteppedConnection:Disconnect()
				end
				avatarEditorInitialization()
			end
		end)
	else
		avatarEditorInitialization()
	end
end

function AvatarEditorSetup:Open()
	if not _G.__TESTEZ_RUNNING_TEST__ then
		RunService:setThrottleFramerateEnabled(false)
	end
	self.openAvatarEditor()
end

function AvatarEditorSetup:Close()
	if not _G.__TESTEZ_RUNNING_TEST__ then
		RunService:setThrottleFramerateEnabled(true)
	end
	self.closeAvatarEditor()
end

function AvatarEditorSetup:UpdateTopBarHeight(topBarHeight)
	if self.AppGui then
		self.AppGui:setDimensions(
			UDim2.new(0, 0, 0,  topBarHeight),
			UDim2.new(1, 0, 1, -topBarHeight))
	end
end

return AvatarEditorSetup
