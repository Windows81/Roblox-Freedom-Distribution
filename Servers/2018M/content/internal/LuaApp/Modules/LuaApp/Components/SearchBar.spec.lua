return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local SearchBar = require(Modules.LuaApp.Components.SearchBar)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local element = mockServices({
			SearchBar = Roact.createElement(SearchBar, {
				isPhone = true,
				confirmSearch = function() end,
				cancelSearch = function() end,
			}),
		})
		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end