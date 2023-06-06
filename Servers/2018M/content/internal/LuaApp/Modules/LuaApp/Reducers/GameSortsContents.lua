local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Immutable = require(Modules.Common.Immutable)
local SetGameSortContents = require(Modules.LuaApp.Actions.SetGameSortContents)
local AddGameSortContents = require(Modules.LuaApp.Actions.AddGameSortContents)
local AddGameSorts = require(Modules.LuaApp.Actions.AddGameSorts)
local GameSortContents = require(Modules.LuaApp.Models.GameSortContents)

return function(state, action)
	state = state or {}

	if action.type == AddGameSorts.name then
		local tmpTable = {}
		for _, sortData in pairs(action.sorts) do
			tmpTable[sortData.name] = state[sortData.name] or GameSortContents.new()
		end
		state = Immutable.JoinDictionaries(state, tmpTable)

	elseif action.type == SetGameSortContents.name then
		-- store the universeIds associated with their sort
		state = Immutable.Set(state, action.sort, action.gameSortContents)

	elseif action.type == AddGameSortContents.name then
		local prevData = state[action.sort]
		local newData = action.gameSortContents

		if prevData then
			newData.entries = Immutable.JoinLists(prevData.entries, newData.entries)
		end

		state = Immutable.Set(state, action.sort, newData)
	end
	return state
end
