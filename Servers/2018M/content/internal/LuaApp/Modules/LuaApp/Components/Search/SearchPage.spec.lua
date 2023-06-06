return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)
	local AppReducer = require(Modules.LuaApp.AppReducer)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)
	local SearchPage = require(Modules.LuaApp.Components.Search.SearchPage)
	it("should create and destroy without errors", function()
		local store = Rodux.Store.new(AppReducer, {
			SearchesInGames = {},
		})

		local element = mockServices({
			searchPage = Roact.createElement(SearchPage, {
				searchUuid = 1,
			})
		}, {
			includeStoreProvider = true,
			store = store,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end