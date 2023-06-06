return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local LoadingIndicator = require(Modules.LuaApp.Components.LoadingIndicator)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local element = mockServices({
			LoadingIndicator = Roact.createElement(LoadingIndicator)
		})
		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end