local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaChat = Modules.LuaChat

local ReceivedMultiplePlaceInfos = require(LuaChat.Actions.ReceivedMultiplePlaceInfos)

local Immutable = require(Common.Immutable)

return function(state, action)
	state = state or {}
	if action.type == ReceivedMultiplePlaceInfos.name then

		local newInfos = {}
		for _, placeInfo in ipairs(action.placeInfos) do
			newInfos[placeInfo.placeId] = placeInfo
		end

		state = Immutable.JoinDictionaries(state, newInfos)
	end
	return state
end
