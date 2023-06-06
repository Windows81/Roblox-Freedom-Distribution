return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)
	local AppReducer = require(Modules.LuaApp.AppReducer)
	local GameSortGroup = require(Modules.LuaApp.Models.GameSortGroup)
	local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
	local GameSortContents = require(Modules.LuaApp.Models.GameSortContents)
	local GameSort = require(Modules.LuaApp.Models.GameSort)
	local Game = require(Modules.LuaApp.Models.Game)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)
	local GameCarousel = require(Modules.LuaApp.Components.Games.GameCarousel)

	it("should create and destroy without errors", function()
		local gameSortGroup = GameSortGroup.mock()
		local gameSortContents = GameSortContents.mock()
		local gameSort = GameSort.mock()
		local gameSortEntry = GameSortEntry.mock()
		local gameModel = Game.mock()
		gameSort.name = "popular"
		gameSort.displayName = "Popular"
		gameSortContents.entries = { gameSortEntry }
		table.insert(gameSortGroup.sorts, gameSort.name)

		local store = Rodux.Store.new(AppReducer, {
			GameSortGroups = { Games = gameSortGroup },
			GameSorts = { [gameSort.name] = gameSort },
			GameSortsContents = { [gameSort.name] = gameSortContents },
			Games = { [gameSortEntry.universeId] = gameModel },
		})

		local element = mockServices({
			gameCarousel = Roact.createElement(GameCarousel, {
				sortName = gameSort.name,
				LayoutOrder = 1,
			})
		}, {
			includeStoreProvider = true,
			store = store,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
		store:Destruct()
	end)
end