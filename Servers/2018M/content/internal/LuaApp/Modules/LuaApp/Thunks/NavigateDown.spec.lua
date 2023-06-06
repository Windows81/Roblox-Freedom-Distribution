return function()
	local NavigateDown = require(script.Parent.NavigateDown)

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
		store:dispatch(NavigateDown({ name = AppPage.GamesList, detail = "Popular" }))

		local state = store:GetState().Navigation
		expect(#state.history).to.equal(1)
		expect(#state.history[1]).to.equal(1)
		expect(state.history[1][1].name).to.equal(AppPage.Home)
	end)

	it("should navigate to new page by appending to the last route", function()
		local store = Rodux.Store.new(AppReducer)
		store:dispatch(NavigateDown({ name = AppPage.GamesList, detail = "Popular" }))

		local state = store:GetState().Navigation
		expect(#state.history).to.equal(2)
		expect(#state.history[1]).to.equal(1)
		expect(state.history[1][1].name).to.equal(AppPage.Home)
		expect(#state.history[2]).to.equal(2)
		expect(state.history[2][1].name).to.equal(AppPage.Home)
		expect(state.history[2][2].name).to.equal(AppPage.GamesList)
		expect(state.history[2][2].detail).to.equal("Popular")
	end)

	it("should assert if given a non-table for route", function()
		NavigateDown({})

		expect(function()
			NavigateDown(nil)
		end).to.throw()

		expect(function()
			NavigateDown("Blargle!")
		end).to.throw()

		expect(function()
			NavigateDown(false)
		end).to.throw()

		expect(function()
			NavigateDown(0)
		end).to.throw()

		expect(function()
			NavigateDown(function() end)
		end).to.throw()
	end)

	it("should assert if given a non-nil non-number for navLockEndTime", function()
		NavigateDown({}, nil)
		NavigateDown({}, 0)

		expect(function()
			NavigateDown({}, "Blargle!")
		end).to.throw()

		expect(function()
			NavigateDown({}, {})
		end).to.throw()

		expect(function()
			NavigateDown({}, false)
		end).to.throw()

		expect(function()
			NavigateDown({}, function() end)
		end).to.throw()
	end)
end