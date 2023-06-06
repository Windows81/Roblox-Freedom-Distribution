return function()
	local AppRouter = require(script.Parent.AppRouter)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)

	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)
	local AppPage = require(Modules.LuaApp.AppPage)
	local AppReducer = require(Modules.LuaApp.AppReducer)
	local NavigateDown = require(Modules.LuaApp.Thunks.NavigateDown)

	it("should create and destroy without errors", function()
		local element = mockServices({
			Router = Roact.createElement(AppRouter, {
				pageConstructors = {
					[AppPage.Home] = function(visible)
						return nil
					end,
				}
			}),
		}, {
			includeStoreProvider = true,
		})
		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)

	it("should create a page for each route in the history, with only the top one visible", function()
		local store = Rodux.Store.new(AppReducer)

		local element = mockServices({
			Router = Roact.createElement(AppRouter, {
				pageConstructors = {
					[AppPage.Home] = function(visible)
						return Roact.createElement("TextLabel", {
							Visible = visible,
							Text = AppPage.Home,
						})
					end,
					[AppPage.GamesList] = function(visible, detail)
						return Roact.createElement("TextLabel", {
							Visible = visible,
							Text = string.format(AppPage.GamesList .. ":" .. detail),
						})
					end,
					[AppPage.GameDetail] = function(visible, detail)
						return Roact.createElement("TextLabel", {
							Visible = visible,
							Text = string.format(AppPage.GameDetail .. ":" .. detail),
						})
					end,
				}
			}),
		}, {
			includeStoreProvider = true,
			store = store,
		})
		local container = Instance.new("Folder")
		Roact.mount(element, container, "RouteTest")

		expect(container).to.be.ok()
		expect(container.RouteTest).to.be.ok()
		expect(container.RouteTest[AppPage.Home]).to.be.ok()
		expect(container.RouteTest[AppPage.Home].Text).to.equal(AppPage.Home)
		expect(container.RouteTest[AppPage.Home].Visible).to.equal(true)

		store:dispatch(NavigateDown({ name = AppPage.GamesList, detail = "popular" }))
		store:flush()
		local gamesListName = AppPage.GamesList .. ":popular"

		expect(container.RouteTest[AppPage.Home]).to.be.ok()
		expect(container.RouteTest[AppPage.Home].Text).to.equal(AppPage.Home)
		expect(container.RouteTest[AppPage.Home].Visible).to.equal(false)
		expect(container.RouteTest[gamesListName]).to.be.ok()
		expect(container.RouteTest[gamesListName].Text).to.equal(gamesListName)
		expect(container.RouteTest[gamesListName].Visible).to.equal(true)

		store:dispatch(NavigateDown({ name = AppPage.GameDetail, detail = "123456" }))
		store:flush()
		local gameDetailName = AppPage.GameDetail .. ":123456"

		expect(container.RouteTest[AppPage.Home]).to.be.ok()
		expect(container.RouteTest[AppPage.Home].Text).to.equal(AppPage.Home)
		expect(container.RouteTest[AppPage.Home].Visible).to.equal(false)
		expect(container.RouteTest[gamesListName]).to.be.ok()
		expect(container.RouteTest[gamesListName].Text).to.equal(gamesListName)
		expect(container.RouteTest[gamesListName].Visible).to.equal(false)
		expect(container.RouteTest[gameDetailName]).to.be.ok()
		expect(container.RouteTest[gameDetailName].Text).to.equal(gameDetailName)
		expect(container.RouteTest[gameDetailName].Visible).to.equal(true)
	end)
end