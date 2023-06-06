return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local EndOfScroll = require(Modules.LuaApp.Components.EndOfScroll)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local element = mockServices({
			EndOfScroll = Roact.createElement(EndOfScroll)
		})
		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end