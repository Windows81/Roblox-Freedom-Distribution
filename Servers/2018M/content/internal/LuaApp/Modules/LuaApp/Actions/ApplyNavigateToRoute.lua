local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Action = require(Modules.Common.Action)

return Action(script.Name, function(route, timeout)
	assert(type(route) == "table", "NavigateToRoute action expects route to be a table")
	assert(type(timeout) == "nil" or type(timeout) == "number",
		"NavigateToRoute action expects timeout to be nil or a number")

	return {
		route = route,
		timeout = timeout,
	}
end)