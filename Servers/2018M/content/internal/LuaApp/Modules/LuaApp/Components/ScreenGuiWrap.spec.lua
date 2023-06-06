return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local ScreenGuiWrap = require(script.parent.ScreenGuiWrap)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local element = mockServices({
			ScreenGuiWrap = Roact.createElement(ScreenGuiWrap, {
				component = "Frame",
				isVisible = true,
				props = {},
			})
		})
		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end