return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local Carousel = require(Modules.LuaApp.Components.Carousel)

	it("should create and destroy without errors", function()
		local element = Roact.createElement(Carousel)
		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end