return function()
	local GamesList = require(script.Parent.GamesList)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)
	local AppReducer = require(Modules.LuaApp.AppReducer)
	local GameSortGroup = require(Modules.LuaApp.Models.GameSortGroup)
	local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
	local GameSortContents = require(Modules.LuaApp.Models.GameSortContents)
	local GameSort = require(Modules.LuaApp.Models.GameSort)
	local Game = require(Modules.LuaApp.Models.Game)
	local AppPage = require(Modules.LuaApp.AppPage)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local gameSortGroup = GameSortGroup.mock()
		local gameSortContents = GameSortContents.mock()
		local gameSort = GameSort.mock()
		local entry = GameSortEntry.mock()
		local game = Game.mock()
		gameSort.name = "popular"
		gameSort.displayName = "Popular"
		gameSortContents.entries = { entry }
		table.insert(gameSortGroup.sorts, gameSort.name)

		local store = Rodux.Store.new(AppReducer, {
			GameSortGroups = { Games = gameSortGroup },
			GameSorts = { [gameSort.name] = gameSort },
			GameSortsContents = { [gameSort.name] = gameSortContents },
			Games = { [entry.universeId] = game },
		})

		local element = mockServices({
			GamesList = Roact.createElement(GamesList, {
				sortName = gameSort.name,
			})
		}, {
			includeStoreProvider = true,
			store = store,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)

	it("should assert on creating analytics if not in the path of home page or games hub", function()
		local gameSortGroup = GameSortGroup.mock()
		local gameSort = GameSort.mock()
		local entry = GameSortEntry.mock()
		local game = Game.mock()
		gameSort.name = "popular"
		gameSort.displayName = "Popular"
		table.insert(gameSortGroup.sorts, gameSort.name)

		local store = Rodux.Store.new(AppReducer, {
			GameSortGroups = { Games = gameSortGroup },
			GameSorts = { [gameSort.name] = gameSort },
			EntriesInSort = { [gameSort.name] = { entry } },
			Games = { [entry.universeId] = game },
			Navigation = {
				history = { { { name = AppPage.Chat } } },
				lockTimer = 0,
			}
		})

		local element = mockServices({
			GamesList = Roact.createElement(GamesList, {
				sortName = gameSort.name,
			})
		}, {
			includeStoreProvider = true,
			store = store,
		})

		expect(function()
			Roact.mount(element)
		end).to.throw()
	end)
end