local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local LuaChat = Modules.LuaChat
local LuaApp = Modules.LuaApp

local Constants = require(LuaChat.Constants)
local Create = require(LuaChat.Create)
local User = require(LuaApp.Models.User)

local UserPresenceTextLabel = {}
UserPresenceTextLabel.__index = UserPresenceTextLabel

function UserPresenceTextLabel.new(appState, userId, additionalProps)
	local self = {
		appState = appState,
		connections = {},
		lastUserModel = nil,
		userId = userId,
	}
	setmetatable(self, UserPresenceTextLabel)

	self.rbx = Create.new("TextLabel")(
		{
			BackgroundTransparency = 1,
			TextSize = Constants.Font.FONT_SIZE_14,
			TextColor3 = Constants.Color.GRAY3,
			Font = Enum.Font.SourceSans,
			TextXAlignment = Enum.TextXAlignment.Left,
		},
		additionalProps
	)

	table.insert(self.connections, appState.store.Changed:Connect(function(newState)
		self:Update(newState)
	end))
	self:Update(appState.store:getState())

	return self
end

function UserPresenceTextLabel:RenderPresenceText(user)
	self.rbx.Text = User.userPresenceToText(self.appState.localization, user)
end

function UserPresenceTextLabel:Update(state)
	local user = state.Users[self.userId]

	if not user then
		return
	end

	if user == self.lastUserModel then
		return
	end
	self.lastUserModel = user

	self:RenderPresenceText(user)
end

function UserPresenceTextLabel:Destruct()
	for _, connection in pairs(self.connections) do
		connection:Disconnect()
	end
	self.rbx:Destroy()
end

return UserPresenceTextLabel

