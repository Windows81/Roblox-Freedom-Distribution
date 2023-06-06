return function()
	local Modules = game:GetService("CoreGui"):FindFirstChild("RobloxGui").Modules
	local SearchRetrievalStatus = require(Modules.LuaApp.Enum.SearchRetrievalStatus)
	local SearchesInGamesStatus = require(Modules.LuaApp.Reducers.SearchesInGamesStatus)
	local SetSearchInGamesStatus = require(Modules.LuaApp.Actions.SetSearchInGamesStatus)

	it("Should not be mutated by other actions", function()
		local oldState = SearchesInGamesStatus(nil, {})
		local newState = SearchesInGamesStatus(oldState, { type = "not a real action" })
		expect(oldState).to.equal(newState)
	end)

	describe("SetSearchInGamesStatus", function()
		it("should preserve purity", function()
			local oldState = SearchesInGamesStatus(nil, {})
			local newState = SearchesInGamesStatus(oldState, SetSearchInGamesStatus(1, SearchRetrievalStatus.Failed))
			expect(oldState).to.never.equal(newState)
		end)

		it("should correctly set and only set the state of a search specified by id", function()
			local oldState = SearchesInGamesStatus(nil, {})
			local newState = SearchesInGamesStatus(oldState, SetSearchInGamesStatus(1, SearchRetrievalStatus.Done))
			expect(newState[1]).to.equal(SearchRetrievalStatus.Done)
			local newState2 = SearchesInGamesStatus(newState, SetSearchInGamesStatus(2, SearchRetrievalStatus.Fetching))
			expect(newState2[2]).to.equal(SearchRetrievalStatus.Fetching)
			expect(newState2[1]).to.equal(SearchRetrievalStatus.Done)
		end)
	end)
end