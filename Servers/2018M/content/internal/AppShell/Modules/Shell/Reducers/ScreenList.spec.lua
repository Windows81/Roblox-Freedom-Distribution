return function()
	local ScreenList = require(script.Parent.ScreenList)
	local ScreenItem = require(script.Parent.Parent.Models.ScreenItem)
	local InsertScreen = require(script.Parent.Parent.Actions.InsertScreen)
	local RemoveScreen = require(script.Parent.Parent.Actions.RemoveScreen)

	describe("require", function()
		it("should require without error", function()
			require(script.Parent.ScreenList)
		end)
	end)

	describe("call", function()
		it("should create with initial state", function()
			local state = ScreenList(nil, {})
			expect(state).to.be.a("table")
		end)

		it("should insert a single screen", function()
			local item = ScreenItem.new("foo", 1, {})
			local action = InsertScreen(item)

			local state = ScreenList({}, action)
			expect(#state).to.equal(1)
			expect(state[1].id).to.equal("foo")
			expect(state[1].priority).to.equal(1)
			expect(state[1].data).to.be.a("table")
		end)

		it("should insert multiple screens", function()
			local item1 = ScreenItem.new("foo", 1, {})
			local item2 = ScreenItem.new("bar", 2, {})
			local action1 = InsertScreen(item1)
			local action2 = InsertScreen(item2)

			local state = ScreenList({}, action1)
			state = ScreenList(state, action2)

			expect(#state).to.equal(2)
			expect(state[1].id).to.equal("bar")
			expect(state[1].priority).to.equal(2)
			expect(state[1].data).to.be.a("table")
		end)

		it("should sort the screens by descending priority", function()
			local item1 = ScreenItem.new("foo", 3, {})
			local item2 = ScreenItem.new("bar", 1, {})
			local action1 = InsertScreen(item1)
			local action2 = InsertScreen(item2)

			local state = ScreenList({}, action1)
			state = ScreenList(state, action2)

			expect(#state).to.equal(2)
			expect(state[1].id).to.equal("foo")
			expect(state[1].priority).to.equal(3)
			expect(state[1].data).to.be.a("table")
		end)

		it("should remove screens", function()
			local item = ScreenItem.new("foo", 1, {})
			local action = InsertScreen(item)

			local state = ScreenList({}, action)

			local action2 = RemoveScreen(item)
			state = ScreenList(state, action2)

			expect(#state).to.equal(0)
		end)
	end)
end