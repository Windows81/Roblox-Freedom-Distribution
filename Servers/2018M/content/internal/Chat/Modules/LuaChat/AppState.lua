local CoreGui = game:GetService("CoreGui")
local LocalizationService = game:GetService("LocalizationService")

local Modules = CoreGui.RobloxGui.Modules

local Common = Modules.Common

local ScreenManager = require(Modules.LuaChat.ScreenManager)
local AppReducer = require(Modules.LuaApp.AppReducer)
local Localization = require(Modules.LuaApp.Localization)

local Analytics = require(Common.Analytics)
local Rodux = require(Common.Rodux)

local AppState = {}

local function appStateConstructor(chatGui, store, analyticsImpl)
	local state = {}

	state.store = store
	state.localization = Localization.new(LocalizationService.RobloxLocaleId)
	state.analytics = analyticsImpl
	state.screenManager = ScreenManager.new(chatGui, state)
	return state
end

function AppState.new(chatGui, store)
	local analyticsImpl = Analytics.new()
	return appStateConstructor(chatGui, store, analyticsImpl)
end

function AppState.mock(chatGui, store, analyticsImpl)
	analyticsImpl = analyticsImpl or Analytics.mock()
	chatGui = chatGui or CoreGui
	store = store or Rodux.Store.new(AppReducer)

	return appStateConstructor(chatGui, store, analyticsImpl)
end

function AppState:Destruct()
	self.store:destruct()
end

return AppState