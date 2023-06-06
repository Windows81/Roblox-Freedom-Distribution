--[[
	{
		-- A list of placeIds to indicate which games are in this sort.
		entries: [
			[1] = entry1 : GameSortEntry,
			[2] = entry2 : GameSortEntry,
			...
		]

		-- A value to remember how many games we've requested so far.
		-- This value doens't necessarily equal #games. For more info, see
		-- comments inside GamesGetList.lua.
		"rowsRequested" : number,

		-- Indicating if we can request more games.
		"hasMoreRows": boolean,
	}
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules
local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
local TableUtilities = require(Modules.LuaApp.TableUtilities)

local GameSortContents = {}

function GameSortContents.new()
	local self = {}

	self.entries = {}
	self.rowsRequested = 0
	self.hasMoreRows = false
	self.nextPageExclusiveStartId = 0

	return self
end

function GameSortContents.mock()
	local self = GameSortContents.new()

	self.entries = { GameSortEntry.mock(), }
	self.rowsRequested = 1
	self.hasMoreRows = false
	self.nextPageExclusiveStartId = 0

	return self
end

function GameSortContents.fromData(gameSortContentsData)
	local self = GameSortContents.new()

	self.entries = gameSortContentsData.entries
	self.rowsRequested = gameSortContentsData.rowsRequested
	self.hasMoreRows = gameSortContentsData.hasMoreRows
	self.nextPageExclusiveStartId = gameSortContentsData.nextPageExclusiveStartId

	return self
end

function GameSortContents.IsEqual(data1, data2)
	-- Compare the entries
	if not TableUtilities.ShallowEqual(data1.entries, data2.entries) then
		return false
	end

	-- Compare other things
	local ignoreEntries = {["entries"] = true}

	return TableUtilities.ShallowEqual(data1, data2, ignoreEntries)
end

return GameSortContents