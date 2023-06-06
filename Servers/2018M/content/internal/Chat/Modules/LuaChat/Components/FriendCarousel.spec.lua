return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local AppReducer = require(Modules.LuaApp.AppReducer)
	local MockId = require(Modules.LuaApp.MockId)
	local Roact = require(Modules.Common.Roact)
	local RoactRodux = require(Modules.Common.RoactRodux)
	local Rodux = require(Modules.Common.Rodux)

	local FriendCarousel = require(Modules.LuaChat.Components.FriendCarousel)

	it("should create and destroy without errors", function()

		local store = Rodux.Store.new(AppReducer)

		local gameFriends = { { uid = MockId() }, { uid = MockId() },
			{ uid = MockId() }, { uid = MockId() }, { uid = MockId() } }
		local carouselItemGap = 9
		local carouselItemHeight = 32
		local carouselItemDotSize = 10

		local element = Roact.createElement(RoactRodux.StoreProvider, {
			store = store,
		}, {
			GameFriends = Roact.createElement(FriendCarousel, {
				dotSize = carouselItemDotSize,
				friends = gameFriends,
				HorizontalAlignment = Enum.HorizontalAlignment.Left,
				itemGap = carouselItemGap,
				itemSize = carouselItemHeight,
				Size = UDim2.new(1, 0, 1, carouselItemHeight),
			}),
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end
