return function()
	local LocalizationService = game:GetService("LocalizationService")
	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local AppReducer = require(Modules.LuaApp.AppReducer)
	local Localization = require(Modules.LuaApp.Localization)
	local MockId = require(Modules.LuaApp.MockId)
	local Roact = require(Modules.Common.Roact)
	local RoactRodux = require(Modules.Common.RoactRodux)
	local Rodux = require(Modules.Common.Rodux)

	local ChatGameDrawer = require(Modules.LuaChat.Components.ChatGameDrawer)

	local localization = Localization.new(LocalizationService.RobloxLocaleId)

	it("should create and destroy without errors", function()

		local store = Rodux.Store.new(AppReducer)

		local element = Roact.createElement(RoactRodux.StoreProvider, {
			store = store,
		}, {
			GameDrawer = Roact.createElement(ChatGameDrawer, {
				AnchorPoint = Vector2.new(0, 0),
				conversationId = MockId(),
				Localization = localization,
				Position = UDim2.new(0, 0, 0, 0),
				onSize = function(newSize, forceOpen)
					-- pass
				end,
			}),
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end
