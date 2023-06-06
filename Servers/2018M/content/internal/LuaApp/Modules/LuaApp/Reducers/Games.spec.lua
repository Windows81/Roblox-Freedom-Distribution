return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Games = require(script.Parent.Games)
	local Game = require(Modules.LuaApp.Models.Game)
	local AddGames = require(Modules.LuaApp.Actions.AddGames)
	local SetPlayabilityStatus = require(Modules.LuaApp.Actions.SetPlayabilityStatus)
	local PlayabilityStatus = require(Modules.LuaApp.Enum.PlayabilityStatus)
	local MockId = require(Modules.LuaApp.MockId)

	local function countChildObjects(aTable)
		local numChildren = 0
		for _ in pairs(aTable) do
			numChildren = numChildren + 1
		end

		return numChildren
	end

	local function createFakeGame()
		local game = Game.mock()
		game.universeId = MockId()
		game.placeId = MockId()

		return game
	end

	local function createFakeGameTable(numGames)
		local someGames = {}
		for _ = 1, numGames do
			local game = createFakeGame()
			someGames[game.universeId] = game
		end

		return someGames
	end

	it("should be empty by default", function()
		local defaultState = Games(nil, {})

		expect(type(defaultState)).to.equal("table")
		expect(countChildObjects(defaultState)).to.equal(0)
	end)

	it("should be unchanged by other actions", function()
		local oldState = Games(nil, {})
		local newState = Games(oldState, { type = "not a real action" })
		expect(oldState).to.equal(newState)
	end)

	describe("AddGames", function()
		it("should preserve purity", function()
			local oldState = Games(nil, {})
			local newState = Games(oldState, AddGames(createFakeGameTable(1)))
			expect(oldState).to.never.equal(newState)
		end)

		it("should add games", function()
			local expectedNumGames = 5
			local someGames = createFakeGameTable(expectedNumGames)
			local action = AddGames(someGames)

			-- add some games to the store
			local modifiedState = Games(nil, action)
			expect(countChildObjects(modifiedState)).to.equal(expectedNumGames)

			-- check that the games have been added to the store
			for _, game in pairs(someGames) do
				local storedGame = modifiedState[game.universeId]
				for key in pairs(storedGame) do
					expect(storedGame[key]).to.equal(game[key])
				end
			end
		end)
	end)

	describe("SetPlayabilityStatus", function()
		it("should set playabilityStatus for game", function()
			local expectedNumGames = 5
			local someGames = createFakeGameTable(expectedNumGames)
			local oldState = Games(nil, {})
			local newState = Games(oldState, AddGames(someGames))

			-- Default playabilityStatus is ""
			for universeId, game in pairs(someGames) do
				expect(newState[universeId].playabilityStatus).to.equal(game.playabilityStatus)
				expect(newState[universeId].playabilityStatus).to.equal("")
			end

			-- Set PlayabilityStatus
			local playabilityStatus = PlayabilityStatus.Playable
			for universeId, game in pairs(someGames) do
				newState = Games(newState, SetPlayabilityStatus(universeId, playabilityStatus))
			end

			-- playabilityStatus should have been updated
			for universeId, game in pairs(someGames) do
				expect(newState[universeId].playabilityStatus).to.equal(playabilityStatus)
			end
		end)
	end)
end