return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)
	local AppReducer = require(Modules.LuaApp.AppReducer)
	local FormFactor = require(Modules.LuaApp.Enum.FormFactor)
	local DropDownList = require(Modules.LuaApp.Components.DropDownList)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local store = Rodux.Store.new(AppReducer, {
			FormFactor = FormFactor.PHONE,
		})

		local listItems = {
			{
				displayName = "Featured",
				displayIcon = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
			}, {
				displayName = "Popular",
				displayIcon = "rbxasset://textures/ui/LuaApp/category/ic-popular.png",
			}, {
				displayName = "Top Rated",
				displayIcon = "rbxasset://textures/ui/LuaApp/category/ic-top rated.png",
			}
		}

		local element = mockServices({
			dropDownList = Roact.createElement(DropDownList, {
				itemSelected = listItems[1],
				items = listItems,
				size = UDim2.new(0, 300, 0, 40),
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