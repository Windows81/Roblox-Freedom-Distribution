local Modules = game:GetService("CoreGui").RobloxGui.Modules
local LuaChat = Modules.LuaChat
local Actions = LuaChat.Actions

local Immutable = require(Modules.Common.Immutable)

local RequestMultiplePlaceInfos = require(Actions.RequestMultiplePlaceInfos)
local FailedToFetchMultiplePlaceInfos = require(Actions.FailedToFetchMultiplePlaceInfos)
local ReceivedMultiplePlaceInfos = require(Actions.ReceivedMultiplePlaceInfos)

return function(state, action)
	state = state or {}
	if action.type == RequestMultiplePlaceInfos.name then
		local newFlags = {}
		for _, placeId in ipairs(action.placeIds) do
			newFlags[placeId] = true
		end
		return Immutable.JoinDictionaries(state, newFlags)
	elseif action.type == ReceivedMultiplePlaceInfos.name then
		local newFlags = {}
		for _, placeInfo in ipairs(action.placeInfos) do
			newFlags[placeInfo.placeId] = false
		end
		return Immutable.JoinDictionaries(state, newFlags)
	elseif action.type == FailedToFetchMultiplePlaceInfos.name then
		local newFlags = {}
		for _, placeId in ipairs(action.placeIds) do
			newFlags[placeId] = false
		end
		return Immutable.JoinDictionaries(state, newFlags)
	end
	return state
end
