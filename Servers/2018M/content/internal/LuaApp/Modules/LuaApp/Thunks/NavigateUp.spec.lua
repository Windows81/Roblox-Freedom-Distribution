return function()
	local NavigateUp = require(script.Parent.NavigateUp)

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
		store:dispatch(NavigateUp())

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
					{
						{ name = AppPage.Games },
						{ name = AppPage.GamesList, detail = "Popular" },
						{ name = AppPage.GameDetails, detail = "12345" },
					},
				},
				lockTimer = 0,
			},
		})
		store:dispatch(NavigateUp())

		local state = store:GetState().Navigation
		expect(#state.history).to.equal(2)
		expect(#state.history[1]).to.equal(3)
		expect(state.history[1][1].name).to.equal(AppPage.Games)
		expect(state.history[1][2].name).to.equal(AppPage.GamesList)
		expect(state.history[1][2].detail).to.equal("Popular")
		expect(state.history[1][3].name).to.equal(AppPage.GameDetails)
		expect(state.history[1][3].detail).to.equal("12345")
		expect(#state.history[2]).to.equal(2)
		expect(state.history[2][1].name).to.equal(AppPage.Games)
		expect(state.history[2][2].name).to.equal(AppPage.GamesList)
		expect(state.history[2][2].detail).to.equal("Popular")
	end)

	it("should assert if given a non-nil non-number for navLockEndTime", function()
		NavigateUp(nil)
		NavigateUp(0)

		expect(function()
			NavigateUp("Blargle!")
		end).to.throw()

		expect(function()
			NavigateUp({})
		end).to.throw()

		expect(function()
			NavigateUp(false)
		end).to.throw()

		expect(function()
			NavigateUp(function() end)
		end).to.throw()
	end)
end