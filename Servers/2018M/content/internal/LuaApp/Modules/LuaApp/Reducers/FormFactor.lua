local Modules = game:GetService("CoreGui").RobloxGui.Modules
local FormFactor = require(Modules.LuaApp.Enum.FormFactor)
local SetFormFactor = require(Modules.LuaApp.Actions.SetFormFactor)

return function(state, action)
	state = state or FormFactor.UNKNOWN

	if action.type == SetFormFactor.name then
		return action.formFactor
	end

	return state
end