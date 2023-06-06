local CoreGui = game:GetService("CoreGui")
local Modules = CoreGui.RobloxGui.Modules

local SetConnectionState = require(Modules.LuaChat.Actions.SetConnectionState)

return function(state, action)
	state = state or Enum.ConnectionState.Connected

	if action.type == SetConnectionState.name then
		state = action.connectionState
	end

	return state
end