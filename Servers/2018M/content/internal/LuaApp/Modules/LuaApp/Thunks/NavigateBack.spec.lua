return function()
	local NavigateBack = require(script.Parent.NavigateBack)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local Rodux = require(Modules.Common.Rodux)

	local AppPage = require(Modules.LuaApp.AppPage)
	local AppReducer = require(Modules.LuaApp.AppReducer)

	it("should do nothing if navigation is locked", function()
		local store = Rodux.Store.new(AppReducer, {
			Navigation = {
				history = {
					{
						{ name = AppPage.Games },
					},
					{
						{ name = AppPage.Games },
						{ name = AppPage.GamesList, detail = "Popular" },
					},
					{
						{ name = AppPage.Games },
						{ name = AppPage.GamesList, detail = "Popular" },
						{ name = AppPage.GameDetails, detail = "12345" },
					},
				},
				lockTimer = 0,
			},
		})
		store:dispatch(NavigateBack(tick() + 1))
		store:dispatch(NavigateBack())

		local state = store:GetState().Navigation
		expect(#state.history).to.equal(2)
		expect(#state.history[1]).to.equal(1)
		expect(state.history[1][1].name).to.equal(AppPage.Games)
		expect(#state.history[2]).to.equal(2)
		expect(state.history[2][1].name).to.equal(AppPage.Games)
		expect(state.history[2][2].name).to.equal(AppPage.GamesList)
		expect(state.history[2][2].detail).to.equal("Popular")
	end)

	it("should remove the current route from the history", function()
		local store = Rodux.Store.new(AppReducer, {
			Navigation = {
				history = {
					{ { name = AppPage.Games } },
					{ { name = AppPage.Games }, { name = AppPage.GamesList, detail = "Popular" } },
				},
				lockTimer = 0,
			},
		})
		store:dispatch(NavigateBack())

		local state = store:GetState().Navigation
		expect(#state.history).to.equal(1)
		expect(#state.history[1]).to.equal(1)
		expect(state.history[1][1].name).to.equal(AppPage.Games)
	end)

	it("should assert if given a non-nil non-number for navLockEndTime", function()
		NavigateBack(nil)
		NavigateBack(0)

		expect(function()
			NavigateBack("Blargle!")
		end).to.throw()

		expect(function()
			NavigateBack({})
		end).to.throw()

		expect(function()
			NavigateBack(false)
		end).to.throw()

		expect(function()
			NavigateBack(function() end)
		end).to.throw()
	end)
end