return function()
	local Navigation = require(script.Parent.Navigation)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local AppPage = require(Modules.LuaApp.AppPage)
	local ApplyNavigateToRoute = require(Modules.LuaApp.Actions.ApplyNavigateToRoute)
	local ApplyNavigateBack = require(Modules.LuaApp.Actions.ApplyNavigateBack)

	it("should have a single route to the home page by default", function()
		local navigation = Navigation(nil, {})

		expect(type(navigation.history)).to.equal("table")
		expect(#navigation.history).to.equal(1)
		expect(type(navigation.history[1])).to.equal("table")
		expect(#navigation.history[1]).to.equal(1)
		expect(navigation.history[1][1].name).to.equal(AppPage.Home)
	end)

	it("should be unchanged by other actions", function()
		local state = Navigation(nil, {})
		state = Navigation(state, { type = "not SetAppPage" })

		expect(#state.history).to.equal(1)
		expect(#state.history[1]).to.equal(1)
		expect(state.history[1][1].name).to.equal(AppPage.Home)
	end)

	describe("ApplyNavigateToRoute", function()
		it("should set the next route", function()
			local state = Navigation(nil, {})
			state = Navigation(state, ApplyNavigateToRoute({
				{ name = AppPage.Games },
				{ name = AppPage.GamesList, detail = "Popular" }
			}))

			expect(#state.history).to.equal(2)
			expect(#state.history[1]).to.equal(1)
			expect(state.history[1][1].name).to.equal(AppPage.Home)
			expect(#state.history[2]).to.equal(2)
			expect(state.history[2][1].name).to.equal(AppPage.Games)
			expect(state.history[2][2].name).to.equal(AppPage.GamesList)
			expect(state.history[2][2].detail).to.equal("Popular")
		end)

		it("should clear history if the route is a root page", function()
			local state = Navigation(nil, {})
			state = Navigation(state, ApplyNavigateToRoute({ { name = AppPage.Games } }))

			expect(#state.history).to.equal(1)
			expect(#state.history[1]).to.equal(1)
			expect(state.history[1][1].name).to.equal(AppPage.Games)
		end)

		it("should store the timeout value", function()
			local state = Navigation(nil, {})
			state = Navigation(state, ApplyNavigateToRoute({ { name = AppPage.Games } }, 12345))

			expect(state.lockTimer).to.equal(12345)
		end)

		it("should not set the timeout value if unspecified", function()
			local state = Navigation(nil, {})
			state.lockTimer = 12345
			state = Navigation(state, ApplyNavigateToRoute({ { name = AppPage.Games } }))

			expect(state.lockTimer).to.equal(12345)
		end)
	end)

	describe("ApplyNavigateBack", function()
		it("should go back to the previous route", function()
			local state = {
				history = {
					{ { name = AppPage.Home } },
					{ { name = AppPage.Home }, { name = AppPage.GamesList, detail = "Popular" } },
				},
				lockTimer = 0,
			}
			state = Navigation(state, ApplyNavigateBack())

			expect(#state.history).to.equal(1)
			expect(#state.history[1]).to.equal(1)
			expect(state.history[1][1].name).to.equal(AppPage.Home)
		end)

		it("should do nothing if there's only one route in the history", function()
			local state = Navigation(nil, {})
			state = Navigation(state, ApplyNavigateBack())

			expect(#state.history).to.equal(1)
			expect(#state.history[1]).to.equal(1)
			expect(state.history[1][1].name).to.equal(AppPage.Home)
		end)

		it("should store the timeout value", function()
			local state = Navigation(nil, {})
			state = Navigation(state, ApplyNavigateBack(12345))

			expect(state.lockTimer).to.equal(12345)
		end)

		it("should not set the timeout value if unspecified", function()
			local state = Navigation(nil, {})
			state.lockTimer = 12345
			state = Navigation(state, ApplyNavigateBack())

			expect(state.lockTimer).to.equal(12345)
		end)
	end)
end