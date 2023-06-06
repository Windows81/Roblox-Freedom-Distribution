local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local LuaChat = Modules.LuaChat
local Components = LuaChat.Components

local BaseScreen = require(LuaChat.Views.Phone.BaseScreen)
local BrowseGamesComponent = require(Components.BrowseGames)
local PopRoute = require(LuaChat.Actions.PopRoute)

local BrowseGames = BaseScreen:Template()
BrowseGames.__index = BrowseGames

function BrowseGames.new(appState, route)
    local self = {
        appState = appState,
        route = route,
        connections = {};
    }
    setmetatable(self, BrowseGames)

    self.BrowseGamesComponent = BrowseGamesComponent.new(appState)
    self.rbx = self.BrowseGamesComponent.rbx

    local backButtonPressedConnection = self.BrowseGamesComponent.BackButtonPressed:Connect(function()
        self.appState.store:Dispatch(PopRoute())
    end)
    table.insert(self.connections, backButtonPressedConnection)

    return self
end

function BrowseGames:Start()
    BaseScreen.Start(self)
    do
        local connection = self.appState.store.Changed:Connect(function(current, previous)
            self:Update(current, previous)
        end)
        table.insert(self.connections, connection)
    end
end

function BrowseGames:Stop()
    for _, connection in pairs(self.connections) do
        connection:Disconnect()
    end
    self.connections = {}

    BaseScreen.Stop(self)
end

function BrowseGames:Destruct()
    self.BrowseGamesComponent:Destruct()
    self.BrowseGamesComponent = nil

    BaseScreen.Destruct(self)
end

function BrowseGames:Update(current, previous)
    self.BrowseGamesComponent:Update(current, previous)
end

return BrowseGames