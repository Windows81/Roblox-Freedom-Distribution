local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Action = require(Modules.Common.Action)

return Action(script.Name, function(status)
	assert(type(status) == "string",
		"SetGamesPageDataStatus action expects status to be an RetrievalStatus (string)")

	return {
		status = status,
	}
end)