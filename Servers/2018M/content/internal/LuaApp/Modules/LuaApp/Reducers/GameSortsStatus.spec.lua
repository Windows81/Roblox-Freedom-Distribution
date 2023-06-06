return function()
	local Modules = game:GetService("CoreGui"):FindFirstChild("RobloxGui").Modules
	local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)
	local GameSortsStatus = require(Modules.LuaApp.Reducers.GameSortsStatus)
	local SetGameSortStatus = require(Modules.LuaApp.Actions.SetGameSortStatus)

	it("Should not be mutated by other actions", function()
		local oldState = GameSortsStatus(nil, {})
		local newState = GameSortsStatus(oldState, { type = "not a real action" })
		expect(oldState).to.equal(newState)
	end)

	describe("SetGameSortStatus", function()
		it("should preserve purity", function()
			local oldState = GameSortsStatus(nil, {})
			local newState = GameSortsStatus(oldState, SetGameSortStatus("Popular", RetrievalStatus.Failed))
			expect(oldState).to.never.equal(newState)
		end)

		it("should correctly set and only set the state of a sort specified by id", function()
			local oldState = GameSortsStatus(nil, {})
			local newState = GameSortsStatus(oldState, SetGameSortStatus("Popular", RetrievalStatus.Done))
			expect(newState["Popular"]).to.equal(RetrievalStatus.Done)
			local newState2 = GameSortsStatus(newState, SetGameSortStatus("Featured", RetrievalStatus.Fetching))
			expect(newState2["Featured"]).to.equal(RetrievalStatus.Fetching)
			expect(newState2["Popular"]).to.equal(RetrievalStatus.Done)
		end)
	end)
end