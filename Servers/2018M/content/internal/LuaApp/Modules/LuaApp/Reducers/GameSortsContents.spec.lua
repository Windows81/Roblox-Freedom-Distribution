return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local AddGameSorts = require(Modules.LuaApp.Actions.AddGameSorts)
	local SetGameSortContents = require(Modules.LuaApp.Actions.SetGameSortContents)
	local AddGameSortContents = require(Modules.LuaApp.Actions.AddGameSortContents)
	local GameSortsContents = require(Modules.LuaApp.Reducers.GameSortsContents)
	local GameSort = require(Modules.LuaApp.Models.GameSort)
	local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
	local GameSortContents = require(Modules.LuaApp.Models.GameSortContents)

	local testEntry1 = GameSortEntry.mock("testId1")
	local testEntry2 = GameSortEntry.mock("testId2")
	local testEntry3 = GameSortEntry.mock("testId3")

	it("should be unmodified by other actions", function()
		local oldState = GameSortsContents(nil, {})
		local newState = GameSortsContents(oldState, { type = "not a real action" })

		expect(oldState).to.equal(newState)
	end)

	describe("AddGameSorts", function()
		it("should update when empty", function()
			local oldState = GameSortsContents(nil, {})
			local testSort = GameSort.mock()
			testSort.name = "Popular"
			local action = AddGameSorts({ testSort })

			local newState = GameSortsContents(oldState, action)
			expect(newState["Popular"]).to.never.equal(nil)
		end)
	end)

	describe("SetGameSortContents", function()
		it("should preserve purity", function()
			local oldState = GameSortsContents(nil, {})
			local newState = GameSortsContents(oldState, SetGameSortContents("Popular", GameSortContents.new()))
			expect(oldState).to.never.equal(newState)
		end)

		it("should set the games in sorts", function()
			local expectedModifiedGroup = "Popular"
			local testGameSortContents = GameSortContents.fromData({
				entries = {testEntry1, testEntry2, testEntry3},
				rowsRequested = 4,
				hasMoreRows = false,
				nextPageExclusiveStartId = 0
			})

			local defaultState = GameSortsContents({ [expectedModifiedGroup] = GameSortContents.new() }, {})

			-- check that there are no sorts in the expected group to begin with
			local gameSortContents = #defaultState[expectedModifiedGroup]
			expect(gameSortContents).to.equal(0)

			-- modify the store
			local action = SetGameSortContents(expectedModifiedGroup, testGameSortContents)
			local modifiedState = GameSortsContents(defaultState, action)

			-- check the store now contains the correct data
			expect(GameSortContents.IsEqual(testGameSortContents, modifiedState[expectedModifiedGroup])).to.equal(true)
		end)
	end)

	describe("AddGameSortContents", function()
		it("should preserve purity", function()
			local oldState = GameSortsContents(nil, {})
			local newState = GameSortsContents(oldState, AddGameSortContents("Popular", GameSortContents.new()))
			expect(oldState).to.never.equal(newState)
		end)

		it("should add games in sorts", function()
			local modifiedGroup = "Popular"
			local testInitialGames = GameSortContents.fromData({
				entries = {testEntry1, testEntry2},
				rowsRequested = 4,
				hasMoreRows = true,
				nextPageExclusiveStartId = 0
			})
			local testAddedGames = GameSortContents.fromData({
				entries = {testEntry3},
				rowsRequested = 5,
				hasMoreRows = false,
				nextPageExclusiveStartId = 0
			})
			local testTotalGames = GameSortContents.fromData({
				entries = {testEntry1, testEntry2, testEntry3},
				rowsRequested = 5,
				hasMoreRows = false,
				nextPageExclusiveStartId = 0
			})

			local defaultState = GameSortsContents({ [modifiedGroup] = testInitialGames }, {})

			-- modify the store
			local action = AddGameSortContents(modifiedGroup, testAddedGames)
			local modifiedState = GameSortsContents(defaultState, action)

			-- check the store now contains the correct data
			expect(GameSortContents.IsEqual(testTotalGames, modifiedState[modifiedGroup])).to.equal(true)
		end)
	end)
end