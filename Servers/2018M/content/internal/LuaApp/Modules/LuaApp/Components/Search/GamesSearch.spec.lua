return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)
	local SearchRetrievalStatus = require(Modules.LuaApp.Enum.SearchRetrievalStatus)
	local AppReducer = require(Modules.LuaApp.AppReducer)
	local GamesSearch = require(Modules.LuaApp.Components.Search.GamesSearch)
	local SearchInGames = require(Modules.LuaApp.Models.SearchInGames)
	local GameSortEntry = require(Modules.LuaApp.Models.GameSortEntry)
	local Game = require(Modules.LuaApp.Models.Game)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors when there is search data", function()
		local searchKeyword = "Meep"
		local searchUuid = 1
		local searchInGames = SearchInGames.mock()
		local entry = GameSortEntry.mock()
		local game = Game.mock()
		local entries = { entry }

		searchInGames.keyword = searchKeyword
		searchInGames.entries = entries

		local store = Rodux.Store.new(AppReducer, {
			SearchesInGames = { [searchUuid] = searchInGames },
			Games = { [entry.universeId] = game },
			RequestsStatus = { SearchesInGamesStatus = { [searchUuid] = SearchRetrievalStatus.Done } }
		})

		local element = mockServices({
			gamesSearch = Roact.createElement(GamesSearch, {
				searchUuid = searchUuid,
			})
		}, {
			includeStoreProvider = true,
			store = store,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)

	it("should create and destroy without errors when search is fetching", function()
		local searchUuid = 1

		local store = Rodux.Store.new(AppReducer, {
			RequestsStatus = { SearchesInGamesStatus = { [searchUuid] = SearchRetrievalStatus.Fetching } },
		})

		local element = mockServices({
			gamesSearch = Roact.createElement(GamesSearch, {
				searchUuid = searchUuid,
			})
		}, {
			includeStoreProvider = true,
			store = store,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)

	it("should create and destroy without errors when search failed", function()
		local searchUuid = 1

		local store = Rodux.Store.new(AppReducer, {
			RequestsStatus = { SearchesInGamesStatus = { [searchUuid] = SearchRetrievalStatus.Failed } },
		})

		local element = mockServices({
			gamesSearch = Roact.createElement(GamesSearch, {
				searchUuid = searchUuid,
			})
		}, {
			includeStoreProvider = true,
			store = store,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end