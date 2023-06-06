local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Action = require(Modules.Common.Action)

--[[
	{
		sort : String ,
		gameSortContents : table [] ,
    }
]]

return Action(script.Name, function(sortName, gameSortContents)
	return {
		sort = sortName,
		gameSortContents = gameSortContents
	}
end)
