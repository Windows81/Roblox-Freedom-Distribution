local Modules = game:GetService("CoreGui").RobloxGui.Modules
local SetPlatform = require(Modules.LuaApp.Actions.SetPlatform)

return function(state, action)
	state = state or Enum.Platform.None

	if action.type == SetPlatform.name then
		return action.platform
	end

	return state
end