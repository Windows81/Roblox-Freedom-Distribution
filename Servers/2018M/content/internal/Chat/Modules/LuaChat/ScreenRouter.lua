local CoreGui = game:GetService("CoreGui")
local Modules = CoreGui.RobloxGui.Modules

local LuaChat = Modules.LuaChat

local FormFactor = require(Modules.LuaApp.Enum.FormFactor)
local DialogInfo = require(Modules.LuaChat.DialogInfo)

local Intent = DialogInfo.Intent

local ScreenRouter = {}

ScreenRouter.RouteMaps = {

	[FormFactor.PHONE] = {

		BrowseGames = function(appState, route)
			local BrowseGames = require(LuaChat.Views.BrowseGames)
			return BrowseGames:Get(appState, route)
		end,
		ConversationHub = function(appState, route)
			local ConversationHub = require(LuaChat.Views.Phone.ConversationHub)
			return ConversationHub:Get(appState, route)
		end,
		Conversation = function(appState, route)
			local Conversation = require(LuaChat.Views.Phone.Conversation)
			return Conversation:Get(appState, route)
		end,
		GroupDetail = function(appState, route)
			local GroupDetail = require(LuaChat.Views.Phone.GroupDetail)

			return GroupDetail:Get(appState, route)
		end,
		NewChatGroup = function(appState, route)
			local NewChatGroup = require(LuaChat.Views.Phone.NewChatGroup)
			return NewChatGroup:Get(appState, route)
		end,
		CreateChat = function(appState, route)
			local CreateChat = require(LuaChat.Views.CreateChat)
			return CreateChat:Get(appState, route)
		end,
		EditChatGroup = function(appState, route)
			local EditChatGroup = require(LuaChat.Views.Phone.EditChatGroup)
			return EditChatGroup:Get(appState, route)
		end,
		GenericDialog = function(appState, route)
			local GenericDialog = require(LuaChat.Views.GenericDialog)
			return GenericDialog:Get(appState, route)
		end,
		GameShare = function(appState, route)
			local GameShare = require(LuaChat.Views.Phone.GameShareView)
			return GameShare:Get(appState, route)
		end,
	},

	[FormFactor.TABLET] = {

		BrowseGames = function(appState, route)
			local BrowseGames = require(LuaChat.Views.BrowseGames)
			return BrowseGames:Get(appState, route)
		end,
		ConversationHub = function(appState, route)
			local ConversationHub = require(LuaChat.Views.Tablet.ConversationHub)
			return ConversationHub:Get(appState, route)
		end,
		Conversation = function(appState, route)
			local Conversation = require(LuaChat.Views.Phone.Conversation)
			return Conversation:Get(appState, route)
		end,
		GroupDetail = function(appState, route)
			local GroupDetail = require(LuaChat.Views.Phone.GroupDetail)
			return GroupDetail:Get(appState, route)
		end,
		NewChatGroup = function(appState, route)
			local NewChatGroup = require(LuaChat.Views.Phone.NewChatGroup)
			return NewChatGroup:Get(appState, route)
		end,
		CreateChat = function(appState, route)
			local CreateChat = require(LuaChat.Views.CreateChat)
			return CreateChat:Get(appState, route)
		end,
		EditChatGroup = function(appState, route)
			local EditChatGroup = require(LuaChat.Views.Phone.EditChatGroup)
			return EditChatGroup:Get(appState, route)
		end,
		GenericDialog = function(appState, route)
			local GenericDialog = require(LuaChat.Views.GenericDialog)
			return GenericDialog:Get(appState, route)
		end,
		GameShare = function(appState, route)
			local GameShare = require(LuaChat.Views.Tablet.GameShareView)
			return GameShare:Get(appState, route)
		end,
	},
}

function ScreenRouter:Compare(firstRoute, secondRoute)

	if firstRoute.intent ~= secondRoute.intent then
		return false
	end

	for key, value in pairs(firstRoute.parameters) do
		if value ~= secondRoute.parameters[key] then
			return false
		end
	end

	for key, value in pairs(secondRoute.parameters) do
		if value ~= firstRoute.parameters[key] then
			return false
		end
	end

	return true
end

function ScreenRouter:GetView(appState, route, routeMap)
	if not Intent[route.intent] then
		error(("Invalid intent value '%s'"):format(
		), 2)
	end

	local mapper = routeMap[route.intent]

	if not mapper then
		error(("No route map defined for intent '%s'"):format(
			route.intent
		), 2)
	end

	return mapper(appState, route)
end

return ScreenRouter
