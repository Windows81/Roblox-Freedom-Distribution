return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local FramePopup = require(Modules.LuaApp.Components.FramePopup)

	it("should create and destroy without errors", function()
		local element = Roact.createElement(FramePopup, {
				heightAllItems = 100,
				heightScrollContainer = 50,
				onCancel = nil,
			},
			nil
		)

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end