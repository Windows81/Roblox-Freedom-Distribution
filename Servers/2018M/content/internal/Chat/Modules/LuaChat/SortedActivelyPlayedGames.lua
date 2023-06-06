local SortActivelyPlayedGames = {}

local function getSortedActivelyPlayedGames(pinnedGameRootPlaceId, inGameParticipants, includeEmptyPinned)
	local sortedGames = {}
	local activeGamesDict = {}
	local pinnedGameBeingPlayed = false

	for _, user in pairs(inGameParticipants) do
		if not activeGamesDict[user.placeId] then
			activeGamesDict[user.placeId] = {}
		end

		table.insert(activeGamesDict[user.placeId], {uid = user.id, joinedAt = user.joinedAt or 0})
	end

	for placeId, players in pairs(activeGamesDict) do
		table.sort(players, function(a, b)
			return a.joinedAt > b.joinedAt
		end)
		if placeId == pinnedGameRootPlaceId then
			pinnedGameBeingPlayed = true
			table.insert(sortedGames, {placeId = placeId, friends = players, pinned = true, recommended = false})
		else
			table.insert(sortedGames, {placeId = placeId, friends = players, pinned = false, recommended = false})
		end
	end

	table.sort(sortedGames, function(a, b)
		if #a.friends > #b.friends then
			return true
		end
		if #a.friends == #b.friends then
			return a.friends[1].joinedAt > b.friends[1].joinedAt
		end
		return false
	end)

	-- if pinned game is being played, move it to the first Position
	if pinnedGameBeingPlayed then
		for index, game in pairs(sortedGames) do
			if game.placeId == pinnedGameRootPlaceId then
				if index == 1 then
					break
				end
				table.insert(sortedGames, 1, table.remove(sortedGames, index))
				break
			end
		end
	elseif pinnedGameRootPlaceId and includeEmptyPinned then
		-- Our pinned game isn't included, but it should be:
		table.insert(sortedGames, 1, {placeId = pinnedGameRootPlaceId, friends = {} , pinned = true, recommended = false})
	end

	return sortedGames
end

function SortActivelyPlayedGames.getSortedGames(pinnedGameRootPlaceId, inGameParticipants)
	return getSortedActivelyPlayedGames(pinnedGameRootPlaceId, inGameParticipants, false)
end

function SortActivelyPlayedGames.getSortedGamesPlusEmptyPinned(pinnedGameRootPlaceId, inGameParticipants)
	return getSortedActivelyPlayedGames(pinnedGameRootPlaceId, inGameParticipants, true)
end

return SortActivelyPlayedGames