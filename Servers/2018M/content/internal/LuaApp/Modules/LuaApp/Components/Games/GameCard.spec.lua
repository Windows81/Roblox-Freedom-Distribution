return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)

	local AppReducer = require(Modules.LuaApp.AppReducer)
	local GameCard = require(Modules.LuaApp.Components.Games.GameCard)
	local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
	local Game = require(Modules.LuaApp.Models.Game)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local entry = GameSortEntry.mock()
		local gameModel = Game.mock()

		local store = Rodux.Store.new(AppReducer, {
			Games = { [entry.universeId] = gameModel },
		})

		local element = mockServices({
			gameCard = Roact.createElement(GameCard, {
				entry = entry,
				size = Vector2.new(60, 60),
			})
		}, {
			includeStoreProvider = true,
			store = store
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
		store:Destruct()
	end)

	it("should create and destroy without errors when a game is sponsored", function()
		local entry = GameSortEntry.mock()
		entry.isSponsored = true
		local gameModel = Game.mock()

		local store = Rodux.Store.new(AppReducer, {
			Games = { [entry.universeId] = gameModel },
		})

		local element = mockServices({
			gameCard = Roact.createElement(GameCard, {
				entry = entry,
				size = Vector2.new(60, 60),
			})
		}, {
			includeStoreProvider = true,
			store = store
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
		store:Destruct()
	end)
end