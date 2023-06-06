--[[
	{
		universeId  :  number ,
		isSponsored  :  bool ,
		adId  :  number ,
		playerCount  :  number ,
	}
]]

local GameSortEntry = {}

function GameSortEntry.new()
	local self = {}

	return self
end

function GameSortEntry.mock(universeId)
	local self = GameSortEntry.new()
	self.universeId = universeId or 149757
	self.placeId = 384314
	self.isSponsored = false
	self.adId = nil
	self.playerCount = 150
	return self
end

function GameSortEntry.fromJsonData(gameSortEntryJson)
	local self = GameSortEntry.new()
	self.universeId = gameSortEntryJson.universeId
	self.placeId = gameSortEntryJson.placeId
	self.isSponsored = gameSortEntryJson.isSponsored
	self.adId = gameSortEntryJson.nativeAdData
	self.playerCount = gameSortEntryJson.playerCount
	return self
end

return GameSortEntry