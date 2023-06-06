return function()
	local GameCarousels = require(script.Parent.GameCarousels)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local AppReducer = require(Modules.LuaApp.AppReducer)
	local GameSortGroup = require(Modules.LuaApp.Models.GameSortGroup)
	local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
	local GameSortContents = require(Modules.LuaApp.Models.GameSortContents)
	local GameSort = require(Modules.LuaApp.Models.GameSort)
	local Game = require(Modules.LuaApp.Models.Game)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)
	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)


	it("should create and destroy without errors with one carousel", function()
		local gameSortGroup = GameSortGroup.mock()
		local gameSort = GameSort.mock()
		local gameSortContents = GameSortContents.mock()
		local entry = GameSortEntry.mock()
		local game = Game.mock()
		gameSortContents.entries = { entry }
		gameSort.name = "popular"
		gameSort.displayName = "Popular"
		table.insert(gameSortGroup.sorts, gameSort.name)

		local store = Rodux.Store.new(AppReducer, {
			GameSortGroups = { Games = gameSortGroup, sorts = { gameSort.name } },
			GameSorts = { [gameSort.name] = gameSort },
			GameSortsContents = { [gameSort.name] = gameSortContents },
			Games = { [entry.universeId] = game },
		})

		local element = mockServices({
			GameCarousel = Roact.createElement(GameCarousels, {
				gameSortGroup = "Games",
			})
		}, {
			includeStoreProvider = true,
			store = store
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
		store:destruct()
	end)

	it("should create and destroy without errors with more than one carousel", function()
		local gameSortGroup = GameSortGroup.mock()
		local gameSort1 = GameSort.mock()
		gameSort1.name = "Sort1"
		local gameSort2 = GameSort.mock()
		gameSort2.name = "Sort2"
		table.insert(gameSortGroup.sorts, gameSort1.name)
		table.insert(gameSortGroup.sorts, gameSort2.name)
		local gameSortContents1 = GameSortContents.mock()
		local gameSortContents2 = GameSortContents.mock()
		local entry1 = GameSortEntry.mock()
		local entry2 = GameSortEntry.mock()
		local game1 = Game.mock()
		local game2 = Game.mock()
		entry2.universeId = 666
		game2.universeId = entry2.universeId
		gameSortContents1.entries = { entry1 }
		gameSortContents2.entries = { entry1, entry2 }

		local store = Rodux.Store.new(AppReducer, {
			GameSortGroups = { Games = gameSortGroup },
			GameSorts = {
				[gameSort1.name] = gameSort1,
				[gameSort2.name] = gameSort2,
			},
			GameSortsContents = {
				[gameSort1.name] = gameSortContents1,
				[gameSort2.name] = gameSortContents2,
			 },
			Games = {
				[entry1.universeId] = game1,
				[entry2.universeId] = game2,
			},
		})
		local element = mockServices({
			GameCarousel = Roact.createElement(GameCarousels, {
				gameSortGroup = "Games",
			})
		}, {
			includeStoreProvider = true,
			store = store
		})
		local instance = Roact.mount(element)
		Roact.unmount(instance)
		store:destruct()
	end)
end