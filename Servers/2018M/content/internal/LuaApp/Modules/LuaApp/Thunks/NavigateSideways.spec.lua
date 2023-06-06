return function()
	local NavigateSideways = require(script.Parent.NavigateSideways)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local Rodux = require(Modules.Common.Rodux)

	local AppPage = require(Modules.LuaApp.AppPage)
	local AppReducer = require(Modules.LuaApp.AppReducer)

	it("should do nothing if navigation is locked", function()
		local store = Rodux.Store.new(AppReducer, {
			Navigation = {
				history = {
					{ { name = AppPage.Games } },
					{ { name = AppPage.Games }, { name = AppPage.GamesList, detail = "Popular" } },
				},
				lockTimer = tick() + 1,
			},
		})
		store:dispatch(NavigateSideways({ name = AppPage.GamesList, detail = "Featured" }))

		local state = store:GetState().Navigation
		expect(#state.history).to.equal(2)
		expect(#state.history[1]).to.equal(1)
		expect(state.history[1][1].name).to.equal(AppPage.Games)
		expect(#state.history[2]).to.equal(2)
		expect(state.history[2][1].name).to.equal(AppPage.Games)
		expect(state.history[2][2].name).to.equal(AppPage.GamesList)
		expect(state.history[2][2].detail).to.equal("Popular")
	end)

	it("should navigate to new page by removing the last element of the current route", function()
		local store = Rodux.Store.new(AppReducer, {
			Navigation = {
				history = {
					{ { name = AppPage.Games } },
					{ { name = AppPage.Games }, { name = AppPage.GamesList, detail = "Popular" } },
				},
				lockTimer = 0,
			},
		})
		store:dispatch(NavigateSideways({ name = AppPage.GamesList, detail = "Featured" }))

		local state = store:GetState().Navigation
		expect(#state.history).to.equal(3)
		expect(#state.history[1]).to.equal(1)
		expect(state.history[1][1].name).to.equal(AppPage.Games)
		expect(#state.history[2]).to.equal(2)
		expect(state.history[2][1].name).to.equal(AppPage.Games)
		expect(state.history[2][2].name).to.equal(AppPage.GamesList)
		expect(state.history[2][2].detail).to.equal("Popular")
		expect(#state.history[3]).to.equal(2)
		expect(state.history[3][1].name).to.equal(AppPage.Games)
		expect(state.history[3][2].name).to.equal(AppPage.GamesList)
		expect(state.history[3][2].detail).to.equal("Featured")
	end)

	it("should assert if given a non-table for route", function()
		NavigateSideways({})

		expect(function()
			NavigateSideways(nil)
		end).to.throw()

		expect(function()
			NavigateSideways("Blargle!")
		end).to.throw()

		expect(function()
			NavigateSideways(false)
		end).to.throw()

		expect(function()
			NavigateSideways(0)
		end).to.throw()

		expect(function()
			NavigateSideways(function() end)
		end).to.throw()
	end)

	it("should assert if given a non-nil non-number for navLockEndTime", function()
		NavigateSideways({}, nil)
		NavigateSideways({}, 0)

		expect(function()
			NavigateSideways({}, "Blargle!")
		end).to.throw()

		expect(function()
			NavigateSideways({}, {})
		end).to.throw()

		expect(function()
			NavigateSideways({}, false)
		end).to.throw()

		expect(function()
			NavigateSideways({}, function() end)
		end).to.throw()
	end)
end