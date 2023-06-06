local Modules = game:GetService("CoreGui").RobloxGui.Modules
local SetHomePageDataStatus = require(Modules.LuaApp.Actions.SetHomePageDataStatus)
local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)

return function(state, action)
	state = state or RetrievalStatus.NotStarted

	if action.type == SetHomePageDataStatus.name then
		state = action.status
	end

	return state
end