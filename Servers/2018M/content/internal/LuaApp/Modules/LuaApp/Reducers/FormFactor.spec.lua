return function()
	local Modules = game:GetService("CoreGui"):FindFirstChild("RobloxGui").Modules
	local SetFormFactor = require(Modules.LuaApp.Actions.SetFormFactor)

	local FormFactorReducer = require(Modules.LuaApp.Reducers.FormFactor)
	local FormFactorEnum = require(Modules.LuaApp.Enum.FormFactor)
	describe("FormFactor", function()
		it("should be unknown by default", function()
			local state = FormFactorReducer(nil, {})

			expect(state).to.equal(FormFactorEnum.UNKNOWN)
		end)

		it("should be unmodified by other actions", function()
			local oldState = FormFactorReducer(nil, {})
			local newState = FormFactorReducer(oldState, { type = "not a real action" })

			expect(oldState).to.equal(newState)
		end)

		it("should be changed using SetFormFactor", function()
			local state = FormFactorReducer(nil, {})

			state = FormFactorReducer(state, SetFormFactor(FormFactorEnum.PHONE))
			expect(state).to.equal(FormFactorEnum.PHONE)

			state = FormFactorReducer(state, SetFormFactor(FormFactorEnum.TABLET))
			expect(state).to.equal(FormFactorEnum.TABLET)
		end)
	end)
end