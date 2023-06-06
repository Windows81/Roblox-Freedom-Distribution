return function()
	local LocalizationService = game:GetService("LocalizationService")
	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local AppReducer = require(Modules.LuaApp.AppReducer)
	local Localization = require(Modules.LuaApp.Localization)
	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)

	local ContextualMenu = require(Modules.LuaApp.Components.ContextualMenu)
	local localization = Localization.new(LocalizationService.RobloxLocaleId)
	local FormFactor = require(Modules.LuaApp.Enum.FormFactor)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local store = Rodux.Store.new(AppReducer, {
			FormFactor = FormFactor.PHONE,
		})

		local menuItems = {
			{
				displayIcon = "rbxasset://textures/ui/LuaApp/icons/ic-games.png",
				name = "PlayGameButton",
				displayName = localization:Format("Feature.Chat.Drawer.PlayGame"),
			},
			{
				displayIcon = "rbxasset://textures/ui/LuaChat/icons/ic-pin.png",
				name = "PinGameButton",
				displayName = localization:Format("Feature.Chat.Drawer.PinGame")
			},
		}

		local screenShape = {
			x = 0,
			y = 0,
			width = 320,
			height = 240,
			parentWidth = 320,
			parentHeight = 240,
		}

		local callbackCancel = function()
			-- cancelled.
		end
		local callbackSelect = function(item)
			-- selected
		end

		local element = mockServices({
			contextualMenu = Roact.createElement(ContextualMenu, {
				callbackCancel = callbackCancel,
				callbackSelect = callbackSelect,
				menuItems = menuItems,
				screenShape = screenShape,
			})
		}, {
			includeStoreProvider = true,
			store = store
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
		store:Destruct()
	end)
end
