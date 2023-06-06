return function()
	describe("require", function()
		it("should create without errors", function()
			require(script.Parent.RemoveScreen)
		end)

		it("should set the name", function()
			local action = require(script.Parent.RemoveScreen)

			expect(action.name).to.equal("RemoveScreen")
		end)
	end)

	describe("call", function()
		it("should return a table when called as a function", function()
			local action = require(script.Parent.RemoveScreen)

			action = action({})
			expect(action).to.be.a("table")
		end)

		it("should set the type", function()
			local action = require(script.Parent.RemoveScreen)

			action = action({})
			expect(action.type).to.equal("RemoveScreen")
		end)

		it("should set the item", function()
			local action = require(script.Parent.RemoveScreen)

			local item = "foo"
			action = action(item)
			expect(action.item).to.equal("foo")
		end)

		it("should set the type and name to be equal", function()
			local action = require(script.Parent.RemoveScreen)

			local actionItem = action({})
			expect(actionItem.type).to.equal(action.name)
		end)
	end)
end