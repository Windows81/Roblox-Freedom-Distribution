local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local ClearAllGames = require(LuaChat.Actions.ShareGameToChatFromChat.ClearAllGamesInSortsShareGameToChatFromChat)
local Constants = require(LuaChat.Constants)
local Create = require(LuaChat.Create)
local DialogInfo = require(LuaChat.DialogInfo)
local Intent = DialogInfo.Intent
local ResetShareGameToChatAsync = require(LuaChat.Actions.ShareGameToChatFromChat.ResetShareGameToChatFromChatAsync)
local Roact = require(Common.Roact)
local RoactAnalytics = require(Modules.LuaApp.Services.RoactAnalytics)
local RoactLocalization = require(LuaApp.Services.RoactLocalization)
local RoactRodux = require(Common.RoactRodux)
local RoactServices = require(LuaApp.RoactServices)
local Signal = require(Common.Signal)

local Components = LuaChat.Components
local HeaderLoader = require(Components.HeaderLoader)
local ResponseIndicator = require(Components.ResponseIndicator)
local SharedGameList = require(Components.SharedGameList)
local TabBarView = require(LuaChat.TabBarView)
local TabPageParameters = require(LuaChat.Models.TabPageParameters)

local BrowseGames = {}
BrowseGames.__index = BrowseGames

function BrowseGames.new(appState)
    local self = {
        appState = appState,
    }
    setmetatable(self, BrowseGames)
    self.connections = {}
	self._analytics = self.appState.analytics
	self._localization = self.appState.localization

	self.responseIndicator = ResponseIndicator.new(appState)
	self.responseIndicator:SetVisible(false)

    self.header = HeaderLoader.GetHeader(appState, Intent.BrowseGames)
    self.header:SetDefaultSubtitle()
    self.header:SetTitle(self.appState.localization:Format("Feature.Chat.ShareGameToChat.BrowseGames"))
    self.header:SetBackButtonEnabled(true)
    self.header:SetConnectionState(Enum.ConnectionState.Disconnected)

	local sharedGamesConfig = Constants.SharedGamesConfig
	local GAME_PAGES = {}

	for _, sortName in ipairs(sharedGamesConfig.SortNames) do
		table.insert(
			GAME_PAGES,
			TabPageParameters(
				self._localization:Format(sharedGamesConfig.SortsAttribute[sortName].TILE_LOCALIZATION_KEY),
				SharedGameList,
				{
					gameSort = sortName,
				}
			)
		)
	end

    self.rbx = Create.new"Frame" {
        BackgroundTransparency = 1,
        BorderSizePixel = 0,
		Size = UDim2.new(1, 0, 1, 0),

        Create.new("UIListLayout") {
            Name = "ListLayout",
            SortOrder = Enum.SortOrder.LayoutOrder,
        },

        self.header.rbx,

		Create.new"Frame" {
            Name = "Content",
			BackgroundColor3 = Constants.Color.GRAY5,
            BorderSizePixel = 0,
			ClipsDescendants = true,
			LayoutOrder = 1,
			Size = UDim2.new(1, 0, 1, -self.header.heightOfHeader),

			self.responseIndicator.rbx,
		},
    }

    self.roactInstanceGamesTabBarView = Roact.mount(Roact.createElement(RoactRodux.StoreProvider, {
        store = appState.store,
    }, {
		Roact.createElement(RoactServices.ServiceProvider, {
			services = {
				[RoactAnalytics] = self._analytics,
				[RoactLocalization] = self._localization,
			}
		}, {
			Roact.createElement(TabBarView, {
				tabs = GAME_PAGES,
			})
		}),

    }), self.rbx.Content, "TabBarView")

    self.BackButtonPressed = Signal.new()
    self.header.BackButtonPressed:Connect(function()
		self:CleanGamesInSorts()
        self.BackButtonPressed:Fire()
    end)

    local headerSizeConnection = self.header.rbx:GetPropertyChangedSignal("AbsoluteSize"):Connect(function()
        self:Resize()
    end)
    table.insert(self.connections, headerSizeConnection)

    return self
end

function BrowseGames:CleanGamesInSorts()
	self.appState.store:dispatch(ClearAllGames())
	self.appState.store:dispatch(ResetShareGameToChatAsync())
end

function BrowseGames:Resize()
    local sizeContent = UDim2.new(1, 0, 1, -self.header.rbx.AbsoluteSize.Y)
    self.rbx.Content.Size = sizeContent
end

function BrowseGames:Update(current, previous)
    self.header:SetConnectionState(current.ConnectionState)

	local isSharing = self.appState.store:getState().ChatAppReducer.ShareGameToChatAsync.sharingGame or false
	self.responseIndicator:SetVisible(isSharing)
end

function BrowseGames:Destruct()
    for _, connection in pairs(self.connections) do
        connection:Disconnect()
    end
    self.connections = {}

    self.header:Destroy()
	self.responseIndicator:Destruct()
	Roact.unmount(self.roactInstanceGamesTabBarView)
    self.rbx:Destroy()
end

return BrowseGames