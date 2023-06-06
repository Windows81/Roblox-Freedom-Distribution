return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local PlaceIdsToUniverseIds = require(script.Parent.PlaceIdsToUniverseIds)
	local AddPlaceIdsToUniverseIds = require(Modules.LuaApp.Actions.AddPlaceIdsToUniverseIds)
	local TableUtilities = require(Modules.LuaApp.TableUtilities)

	it("should be empty by default", function()
		local defaultState = PlaceIdsToUniverseIds(nil, {})

		expect(type(defaultState)).to.equal("table")
		expect(TableUtilities.FieldCount(defaultState)).to.equal(0)
	end)

	it("should be unchanged by other actions", function()
		local oldState = PlaceIdsToUniverseIds(nil, {})
		local newState = PlaceIdsToUniverseIds(oldState, { type = "not a real action" })
		expect(oldState).to.equal(newState)
	end)

	describe("AddPlaceIdsToUniverseIds", function()
		it("should preserve purity", function()
			local oldState = PlaceIdsToUniverseIds(nil, {})
			local newState = PlaceIdsToUniverseIds(oldState, AddPlaceIdsToUniverseIds({}))
			expect(oldState).to.never.equal(newState)
		end)

		it("should add PlaceIdsToUniverseIds", function()
			local somePlaceIdsToUniverseIds = {}
			somePlaceIdsToUniverseIds[606849621] = 245662005
			somePlaceIdsToUniverseIds[824337654] = 343344299
			local action = AddPlaceIdsToUniverseIds(somePlaceIdsToUniverseIds)

			local modifiedState = PlaceIdsToUniverseIds(nil, action)
			expect(TableUtilities.FieldCount(modifiedState)).to.equal(2)

			for placeId, universeId in pairs(somePlaceIdsToUniverseIds) do
				expect(modifiedState[placeId]).to.equal(universeId)
			end
		end)
	end)
end