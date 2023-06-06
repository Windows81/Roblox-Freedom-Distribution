return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local RoactMotion = require(Modules.LuaApp.RoactMotion)
	local UIScaler = require(Modules.LuaApp.Components.UIScaler)

	it("should create and destroy without errors", function()
		local element = Roact.createElement(UIScaler, {
			scaleValue = RoactMotion.spring(0.5),
			onRested = nil,
		})
		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end