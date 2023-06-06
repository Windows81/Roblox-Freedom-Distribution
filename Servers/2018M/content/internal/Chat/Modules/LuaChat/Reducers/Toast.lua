local Modules = game:GetService("CoreGui").RobloxGui.Modules

local ShowToast = require(Modules.LuaChat.Actions.ShowToast)
local ToastComplete = require(Modules.LuaChat.Actions.ToastComplete)

return function(state, action)
	state = state or nil

	if action.type == ShowToast.name then
		state = action.toast
	elseif action.type == ToastComplete.name then
		state = nil
	end

	return state
end