local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local Immutable = require(Common.Immutable)
local LuaChat = Modules.LuaChat
local ShareGameToChatActions = LuaChat.Actions.ShareGameToChatFromChat

local AddGamesInformation =  require(ShareGameToChatActions.AddGamesInformationShareGameToChatFromChat)

return function(state, action)
	state = state or {}
	if action.type == AddGamesInformation.name then
		local tmpTable = {}
		for _, gameInfo in pairs(action.games) do
			tmpTable[gameInfo.placeId] = gameInfo
		end
		state = Immutable.JoinDictionaries(state, tmpTable)
	end

	return state
end