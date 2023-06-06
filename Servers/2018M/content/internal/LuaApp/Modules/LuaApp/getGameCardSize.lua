local GAME_CARD_DETAIL_HEIGHT = 60

local function getMinCardCountForWidth(width)
	if width < 513 then
		return 3
	elseif width < 852 then
		return 4
	elseif width < 1012 then
		return 5
	elseif width < 1172 then
		return 6
	elseif width < 1332 then
		return 7
	else
		return 8
	end
end


--[[
	Uses this document:
	https://docs.google.com/spreadsheets/d/1CqzYHlCZxRUvY8_FuQJ7yc-H_gSNL0XWwEdDS2pNShA/edit#gid=15226408
	To lookup intended card count for screen size, then uses that to calculate the game card width.
]]
local function getGameCardSize(containerWidth, containerPadding, cardPadding, trailingCardFraction)
	assert(type(containerWidth) == "number", "containerWidth (argument 1) must be a number")
	assert(type(cardPadding) == "number", "cardPadding (argument 2) must be a number")
	assert(type(trailingCardFraction) == "number", "trailingCardFraction (argument 3) must be a number")

	local cardCount = getMinCardCountForWidth(containerWidth + containerPadding) + trailingCardFraction

	-- for example, when we have 3.25 cards, there'll be 3 paddings
	-- when we have 3 cards, there'll be 2 paddings
	local paddingCount = math.ceil(cardCount) - 1
	local cardWidth = (containerWidth - cardPadding * paddingCount)/cardCount
	local cardHeight = cardWidth + GAME_CARD_DETAIL_HEIGHT

	return Vector2.new(cardWidth, cardHeight), cardCount
end

return getGameCardSize