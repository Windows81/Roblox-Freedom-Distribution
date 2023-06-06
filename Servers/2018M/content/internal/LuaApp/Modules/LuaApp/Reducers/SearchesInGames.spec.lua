return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local SearchesInGames = require(script.Parent.SearchesInGames)
	local SearchInGames = require(Modules.LuaApp.Models.SearchInGames)
	local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
	local SetSearchInGames = require(Modules.LuaApp.Actions.SetSearchInGames)
	local AppendSearchInGames = require(Modules.LuaApp.Actions.AppendSearchInGames)
	local RemoveSearchInGames = require(Modules.LuaApp.Actions.RemoveSearchInGames)
	local ResetSearchesInGames = require(Modules.LuaApp.Actions.ResetSearchesInGames)

	local function countChildObjects(aTable)
		local numChildren = 0
		for _ in pairs(aTable) do
			numChildren = numChildren + 1
		end

		return numChildren
	end

	local function createFakeSearches(numSearches)
		local searches = {}
		for i = 1, numSearches do
			local search = SearchInGames.mock()
			search.keyword = search.keyword..tostring(i)
			table.insert(searches, search)
		end

		return searches
	end

	it("should be empty by default", function()
		local defaultState = SearchesInGames(nil, {})

		expect(type(defaultState)).to.equal("table")
		expect(countChildObjects(defaultState)).to.equal(0)
	end)

	it("should be unchanged by other actions", function()
		local oldState = SearchesInGames(nil, {})
		local newState = SearchesInGames(oldState, { type = "not a real action" })
		expect(oldState).to.equal(newState)
	end)

	describe("SetSearchInGames", function()
		it("should preserve purity", function()
			local oldState = SearchesInGames(nil, {})
			local newState = SearchesInGames(oldState, SetSearchInGames(1, SearchInGames.mock()))
			expect(oldState).to.never.equal(newState)
		end)

		it("should add searches", function()
			local expectedNumSearches = 5
			local someSearches = createFakeSearches(expectedNumSearches)
			someSearches[1].entries = { GameSortEntry.mock("testId1") }

			local state = nil
			for i = 1, expectedNumSearches do
				state = SearchesInGames(state, SetSearchInGames(i, someSearches[i]))
				expect(countChildObjects(state)).to.equal(i)
				expect(SearchInGames.IsEqual(state[i], someSearches[i])).to.equal(true)
			end
		end)
	end)

	describe("AppendSearchInGames", function()
		it("should preserve purity", function()
			local oldState = SearchesInGames(nil, {})
			local newState = SearchesInGames(oldState, AppendSearchInGames(1, SearchInGames.mock()))
			expect(oldState).to.never.equal(newState)
		end)

		it("should append content to specified search", function()
			local expectedNumSearches = 3
			local someSearches = createFakeSearches(expectedNumSearches)
			local appendSearchIndex = 2
			someSearches[appendSearchIndex].entries = { GameSortEntry.mock("testId1") }

			local state = nil
			for i = 1, expectedNumSearches do
				state = SearchesInGames(state, SetSearchInGames(i, someSearches[i]))
			end

			local newSearch = SearchInGames.mock()
			newSearch.entries = { GameSortEntry.mock("testId2") }
			someSearches[appendSearchIndex] = newSearch
			someSearches[appendSearchIndex].entries = { GameSortEntry.mock("testId1"), GameSortEntry.mock("testId2") }

			state = SearchesInGames(state, AppendSearchInGames(appendSearchIndex, newSearch))

			for i = 1, expectedNumSearches do
				expect(SearchInGames.IsEqual(state[i], someSearches[i])).to.equal(true)
			end
		end)
	end)

	describe("RemoveSearchInGames", function()
		it("should preserve purity", function()
			local oldState = SearchesInGames(nil, {})
			local newState = SearchesInGames(oldState, RemoveSearchInGames(1))
			expect(oldState).to.never.equal(newState)
		end)

		it("should remove and only remove specified search", function()
			local expectedNumSearches = 5
			local someSearches = createFakeSearches(expectedNumSearches)

			local state = nil
			for i = 1, expectedNumSearches do
				state = SearchesInGames(state, SetSearchInGames(i, someSearches[i]))
			end

			local removeSearchIndex = 2
			someSearches[removeSearchIndex] = nil
			state = SearchesInGames(state, RemoveSearchInGames(removeSearchIndex))

			expect(countChildObjects(state)).to.equal(4)
			expect(state[removeSearchIndex]).to.equal(nil)
			for i = 1, expectedNumSearches do
				if i ~= removeSearchIndex then
					expect(SearchInGames.IsEqual(state[i], someSearches[i])).to.equal(true)
				end
			end
		end)
	end)

	describe("ResetSearchesInGames", function()
		it("should preserve purity", function()
			local oldState = SearchesInGames(nil, {})
			local newState = SearchesInGames(oldState, ResetSearchesInGames())
			expect(oldState).to.never.equal(newState)
		end)

		it("should reset searches", function()
			local expectedNumSearches = 3
			local someSearches = createFakeSearches(expectedNumSearches)
			local state = nil
			for i = 1, expectedNumSearches do
				state = SearchesInGames(state, SetSearchInGames(i, someSearches[i]))
			end

			state = SearchesInGames(state, ResetSearchesInGames())
			expect(countChildObjects(state)).to.equal(0)
		end)
	end)
end