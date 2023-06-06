local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaChat = Modules.LuaChat

local Immutable = require(Common.Immutable)
local ReceivedPlaceThumbnail = require(LuaChat.Actions.ReceivedPlaceThumbnail)

return function(state, action)
	state = state or {}
	if action.type == ReceivedPlaceThumbnail.name then
		state = Immutable.Set(state, action.imageToken, action.thumbnail)
	end
	return state
end
