return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Constants = require(Modules.LuaApp.Constants)
	local TopBar = require(Modules.LuaApp.Reducers.TopBar)

	local SetTopBarHeight = require(Modules.LuaApp.Actions.SetTopBarHeight)

	describe("initial state", function()
		it("should return an initial table when passed nil", function()
			local state = TopBar(nil, {})
			expect(state).to.be.a("table")
		end)
	end)

	describe("SetTopBarHeight", function()
		it("should update topBarHeight", function()
			local state = TopBar(nil, {})
			expect(state.topBarHeight).to.equal(Constants.TOP_BAR_SIZE)

			local newTopBarHeight = 100
			state = TopBar(state, SetTopBarHeight(newTopBarHeight))
			expect(state.topBarHeight).to.equal(newTopBarHeight)
		end)
	end)

end