return function()
	local NavigateToRoute = require(script.Parent.NavigateToRoute)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local Rodux = require(Modules.Common.Rodux)

	local AppPage = require(Modules.LuaApp.AppPage)
	local AppReducer = require(Modules.LuaApp.AppReducer)

	it("should do nothing if navigation is locked", function()
		local store = Rodux.Store.new(AppReducer, {
			Navigation = {
				history = {
					{ { name = AppPage.Home } }
				},
				lockTimer = tick() + 1,
			},
		})
		store:dispatch(NavigateToRoute({ { name = AppPage.Games } }))

		local state = store:GetState().Navigation
		expect(#state.history).to.equal(1)
		expect(#state.history[1]).to.equal(1)
		expect(state.history[1][1].name).to.equal(AppPage.Home)
	end)

	it("should navigate to the new route", function()
		local store = Rodux.Store.new(AppReducer)
		store:dispatch(NavigateToRoute({
			{ name = AppPage.Games },
			{ name = AppPage.GamesList, detail = "Popular" },
		}))

		local state = store:GetState().Navigation
		expect(#state.history).to.equal(2)
		expect(#state.history[1]).to.equal(1)
		expect(state.history[1][1].name).to.equal(AppPage.Home)
		expect(#state.history[2]).to.equal(2)
		expect(state.history[2][1].name).to.equal(AppPage.Games)
		expect(state.history[2][2].name).to.equal(AppPage.GamesList)
		expect(state.history[2][2].detail).to.equal("Popular")
	end)

	it("should assert if given a non-table for route", function()
		NavigateToRoute({})

		expect(function()
			NavigateToRoute(nil)
		end).to.throw()

		expect(function()
			NavigateToRoute("Blargle!")
		end).to.throw()

		expect(function()
			NavigateToRoute(false)
		end).to.throw()

		expect(function()
			NavigateToRoute(0)
		end).to.throw()

		expect(function()
			NavigateToRoute(function() end)
		end).to.throw()
	end)

	it("should assert if given a non-nil non-number for navLockEndTime", function()
		NavigateToRoute({}, nil)
		NavigateToRoute({}, 0)

		expect(function()
			NavigateToRoute({}, "Blargle!")
		end).to.throw()

		expect(function()
			NavigateToRoute({}, {})
		end).to.throw()

		expect(function()
			NavigateToRoute({}, false)
		end).to.throw()

		expect(function()
			NavigateToRoute({}, function() end)
		end).to.throw()
	end)
end