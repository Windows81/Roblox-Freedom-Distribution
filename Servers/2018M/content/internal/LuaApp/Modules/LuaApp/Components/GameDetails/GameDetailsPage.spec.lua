return function()
	local GameDetailsPage = require(script.Parent.GameDetailsPage)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)

	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)
	local AppReducer = require(Modules.LuaApp.AppReducer)
	local Game = require(Modules.LuaApp.Models.Game)
	local GameDetail = require(Modules.LuaApp.Models.GameDetail)
	local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
	local GameSortContents = require(Modules.LuaApp.Models.GameSortContents)

	it("should create and destroy without errors", function()
		local entry = GameSortEntry.mock()
		local gameSortContents = GameSortContents.mock()
		local game = Game.mock()

		gameSortContents.entries = { entry }

		local store = Rodux.Store.new(AppReducer, {
			GameSortsContents = { Recommended = gameSortContents },
			Games = { [entry.universeId] = game },
		})

		local element = mockServices({
			GameDetailsPage = Roact.createElement(GameDetailsPage, {
				game = Game.mock(),
				gameDetail = GameDetail.mock(),
			}),
		}, {
			includeStoreProvider = true,
			store = store,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end