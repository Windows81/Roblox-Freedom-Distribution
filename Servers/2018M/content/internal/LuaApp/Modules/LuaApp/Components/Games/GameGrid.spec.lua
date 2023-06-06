return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)

	local AppReducer = require(Modules.LuaApp.AppReducer)
	local GameGrid = require(Modules.LuaApp.Components.Games.GameGrid)
	local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
	local Game = require(Modules.LuaApp.Models.Game)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local entry = GameSortEntry.mock()
		local game = Game.mock()

		local entries = { entry }

		local store = Rodux.Store.new(AppReducer, {
			Games = { [entry.universeId] = game },
		})

		local element = mockServices({
			gameGrid = Roact.createElement(GameGrid, {
				LayoutOrder = 7,
				entries = entries,
				numberOfRowsToShow = 1,
				windowSize = Vector2.new(500, 800),
			})
		}, {
			includeStoreProvider = true,
			store = store,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end