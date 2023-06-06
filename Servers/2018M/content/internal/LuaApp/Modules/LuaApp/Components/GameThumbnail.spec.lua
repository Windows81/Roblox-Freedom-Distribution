return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)
	local GameThumbnail = require(Modules.LuaApp.Components.GameThumbnail)
	local AppReducer = require(Modules.LuaApp.AppReducer)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local store = Rodux.Store.new(AppReducer, {
			GameThumbnails = {
				["70542190"] = "https://t5.rbxcdn.com/ed422c6fbb22280971cfb289f40ac814",
			},
		})

		local element = mockServices({
			gameThumbnail = Roact.createElement(GameThumbnail, {
				loadingImage = "rbxasset://textures/ui/LuaApp/icons/ic-game.png",
				universeId = 70542190,
			})
		}, {
			includeStoreProvider = true,
			store = store
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
		store:destruct()
	end)
end