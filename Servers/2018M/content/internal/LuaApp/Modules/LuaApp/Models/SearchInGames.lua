--[[
	{
		keyword : string,
		entries: [
			[1] = entry1 : GameSortEntry,
			[2] = entry2 : GameSortEntry,
			...
		]
		suggestedKeyword = string,
		correctedKeyword = string,
		filteredKeyword = string,

		-- A value to remember how many games we've requested so far.
		-- This value doens't necessarily equal #games. For more info, see
		-- comments inside GamesGetList.lua.
		"rowsRequested" : number,

		-- Indicating if we can request more games.
		hasMoreRows = bool,

		-- Indicating if we have enabled keywordSuggestion
		isKeywordSuggestionEnabled = bool,
    }
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules
local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
local TableUtilities = require(Modules.LuaApp.TableUtilities)

local SearchInGames = {}

function SearchInGames.new()
	local self = {}

	return self
end

function SearchInGames.mock()
	local self = SearchInGames.new()
	self.keyword = "Meepcity"
	self.entries = { GameSortEntry.mock(), }
	self.suggestedKeyword = nil
	self.correctedKeyword =  nil
	self.filteredKeyword = nil
	self.rowsRequested = 30
	self.hasMoreRows = false
	self.isKeywordSuggestionEnabled = false

	return self
end

function SearchInGames.fromJsonData(searchInGamesJson, keyword, entries, rowsRequested, isKeywordSuggestionEnabled)
	local self = SearchInGames.new()
	self.keyword = keyword
	self.entries = entries
	self.suggestedKeyword = searchInGamesJson.suggestedKeyword
	self.correctedKeyword = searchInGamesJson.correctedKeyword
	self.filteredKeyword = searchInGamesJson.filteredKeyword
	self.rowsRequested = rowsRequested
	self.hasMoreRows = searchInGamesJson.hasMoreRows
	self.isKeywordSuggestionEnabled = isKeywordSuggestionEnabled

	return self
end

function SearchInGames.IsEqual(data1, data2)
	-- Compare the entries
	if not TableUtilities.ShallowEqual(data1.entries, data2.entries) then
		return false
	end

	-- Compare other things
	local ignoreEntries = {["entries"] = true}

	return TableUtilities.ShallowEqual(data1, data2, ignoreEntries)
end

return SearchInGames