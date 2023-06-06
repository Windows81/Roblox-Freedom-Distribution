return function()
	it("should return a table", function()
		local action = require(script.Parent.SetRenderedFriendsData)

		expect(action).to.be.a("table")
	end)

	it("should return a table without data when passed nil", function()
		local action = require(script.Parent.SetRenderedFriendsData)()

		expect(action).to.be.a("table")
		expect(action.data).to.equal(nil)
	end)

	it("should set the name", function()
		local action = require(script.Parent.SetRenderedFriendsData)

		expect(action.name).to.equal("SetRenderedFriendsData")
	end)

	it("should set the elements at the first depth", function()
		local action = require(script.Parent.SetRenderedFriendsData)( { {}, {} } )

		expect(action.data[2]).to.be.a("table")
	end)

	it("should set the elements at the second depth", function()
		local action = require(script.Parent.SetRenderedFriendsData)( { { a="A", b="B" } } )

		expect(action.data[1]).to.be.a("table")
		expect(action.data[1].a).to.equal("A")
	end)

	it("should set the type", function()
		local action = require(script.Parent.SetRenderedFriendsData)()

		expect(action.type).to.equal("SetRenderedFriendsData")
	end)
end