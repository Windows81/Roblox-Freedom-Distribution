return function()
	local Modules = game:GetService("CoreGui"):FindFirstChild("RobloxGui").Modules
	local GameSortTokenFetchingStatus = require(script.parent.GameSortTokenFetchingStatus)
	local SetGameSortTokenFetchingStatus = require(Modules.LuaApp.Actions.SetGameSortTokenFetchingStatus)

	it("Should not be mutated by other actions", function()
		local oldState = GameSortTokenFetchingStatus(nil, {})
		local newState = GameSortTokenFetchingStatus(oldState, { type = "not a real action" })
		expect(oldState).to.equal(newState)
	end)

	describe("SetGameSortTokenFetchingStatus", function()
		it("should preserve purity", function()
			local oldState = GameSortTokenFetchingStatus(nil, {})
			local newState = GameSortTokenFetchingStatus(oldState, SetGameSortTokenFetchingStatus("Games", "Failed"))
			expect(oldState).to.never.equal(newState)
		end)

		it("should correctly set the state of token fetching of various sort groups", function()
			local oldState = GameSortTokenFetchingStatus(nil, {})
			local newState = GameSortTokenFetchingStatus(oldState, SetGameSortTokenFetchingStatus("Games", "Done"))
			expect(newState["Games"]).to.equal("Done")
			local newState2 = GameSortTokenFetchingStatus(oldState, SetGameSortTokenFetchingStatus("HomeGames", "Failed"))
			expect(newState2["HomeGames"]).to.equal("Failed")
		end)
	end)
end