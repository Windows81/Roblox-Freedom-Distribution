return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local getGameCardSize = require(Modules.LuaApp.getGameCardSize)
	local Constants = require(Modules.LuaApp.Constants)

	describe("getGameCardSize", function()
		it("should return accurate game card widths and counts", function()
			local _, cardCount = getGameCardSize(320.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(3.25)
			_, cardCount = getGameCardSize(320.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.0)
			expect(cardCount).to.equal(3.0)
			_, cardCount = getGameCardSize(360.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(3.25)
			_, cardCount = getGameCardSize(375.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(3.25)
			_, cardCount = getGameCardSize(414.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(3.25)
			_, cardCount = getGameCardSize(510.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(3.25)
			_, cardCount = getGameCardSize(513.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(4.25)
			_, cardCount = getGameCardSize(513.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.0)
			expect(cardCount).to.equal(4.0)
			_, cardCount = getGameCardSize(600.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(4.25)
			_, cardCount = getGameCardSize(692.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(4.25)
			_, cardCount = getGameCardSize(768.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(4.25)
			_, cardCount = getGameCardSize(852.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(5.25)
			_, cardCount = getGameCardSize(1012.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(6.25)
			_, cardCount = getGameCardSize(1024.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(6.25)
			_, cardCount = getGameCardSize(1172.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(7.25)
			_, cardCount = getGameCardSize(1332.0 - Constants.GAME_CAROUSEL_PADDING,
				Constants.GAME_CAROUSEL_PADDING, Constants.GAME_CAROUSEL_CHILD_PADDING, 0.25)
			expect(cardCount).to.equal(8.25)
		end)
	end)
end