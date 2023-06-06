local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Immutable = require(Modules.Common.Immutable)

local RequestPlaceThumbnail = require(Modules.LuaChat.Actions.RequestPlaceThumbnail)
local ReceivedPlaceThumbnail = require(Modules.LuaChat.Actions.ReceivedPlaceThumbnail)
local FailedToFetchPlaceThumbnail = require(Modules.LuaChat.Actions.FailedToFetchPlaceThumbnail)

return function(state, action)
	state = state or {}
	if action.type == RequestPlaceThumbnail.name then
		return Immutable.JoinDictionaries(state, {
			[action.imageToken] = true,
		})
	elseif action.type == ReceivedPlaceThumbnail.name then
		return Immutable.JoinDictionaries(state, {
			[action.imageToken] = false,
		})
	elseif action.type == FailedToFetchPlaceThumbnail.name then
		return Immutable.JoinDictionaries(state, {
			[action.imageToken] = false,
		})
	end
	return state
end
