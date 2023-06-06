local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Immutable = require(Modules.Common.Immutable)
local SetSearchInGames = require(Modules.LuaApp.Actions.SetSearchInGames)
local AppendSearchInGames = require(Modules.LuaApp.Actions.AppendSearchInGames)
local RemoveSearchInGames = require(Modules.LuaApp.Actions.RemoveSearchInGames)
local ResetSearchesInGames = require(Modules.LuaApp.Actions.ResetSearchesInGames)

return function(state, action)
	state = state or {}

	if action.type == SetSearchInGames.name then
		state = Immutable.Set(state, action.searchUuid, action.searchInGames)

	elseif action.type == AppendSearchInGames.name then
		local searchUuid = action.searchUuid
		local prevData = state[searchUuid]
		local newData = action.searchInGames

		if prevData then
			newData.entries = Immutable.JoinLists(prevData.entries, newData.entries)
			newData.keyword = prevData.keyword
			newData.suggestedKeyword = prevData.suggestedKeyword
			newData.correctedKeyword = prevData.correctedKeyword
			newData.filteredKeyword = prevData.filteredKeyword
			newData.isKeywordSuggestionEnabled = prevData.isKeywordSuggestionEnabled
		end

		state = Immutable.Set(state, searchUuid, newData)

	elseif action.type == RemoveSearchInGames.name then
		state = Immutable.Set(state, action.searchUuid, nil)

	elseif action.type == ResetSearchesInGames.name then
		state = {}
	end

	return state
end