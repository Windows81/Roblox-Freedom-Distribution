local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local Action = require(Common.Action)
local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)

return Action(script.Name, function(userId)
	return {
		userId = userId,
		status = RetrievalStatus.Fetching,
	}
end)