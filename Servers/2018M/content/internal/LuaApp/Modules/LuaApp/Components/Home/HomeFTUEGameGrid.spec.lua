return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)

	local AppReducer = require(Modules.LuaApp.AppReducer)
	local Constants = require(Modules.LuaApp.Constants)

	local HomeFTUEGameGrid = require(Modules.LuaApp.Components.Home.HomeFTUEGameGrid)
	local FormFactor = require(Modules.LuaApp.Enum.FormFactor)
	local GameSortGroup = require(Modules.LuaApp.Models.GameSortGroup)
	local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
	local GameSortContents = require(Modules.LuaApp.Models.GameSortContents)
	local GameSort = require(Modules.LuaApp.Models.GameSort)
	local Game = require(Modules.LuaApp.Models.Game)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local homeSortGroup = GameSortGroup.mock()
		local gameSort = GameSort.mock()
		local entry = GameSortEntry.mock()
		local gameSortContents = GameSortContents.mock()
		local game = Game.mock()

		gameSortContents.entries = { entry }
		homeSortGroup.sorts = { gameSort.name }

		local store = Rodux.Store.new(AppReducer, {
			GameSorts = { [gameSort.name] = gameSort },
			GameSortsContents = { [gameSort.name] = gameSortContents },
			Games = { [entry.universeId] = game },
			FormFactor = FormFactor.PHONE,
			GameSortGroups = { [Constants.GameSortGroups.HomeGames] = homeSortGroup },
		})

		local element = mockServices({
			gameGrid = Roact.createElement(HomeFTUEGameGrid, {
				LayoutOrder = 7,
			}),
		}, {
			includeStoreProvider = true,
			store = store,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end