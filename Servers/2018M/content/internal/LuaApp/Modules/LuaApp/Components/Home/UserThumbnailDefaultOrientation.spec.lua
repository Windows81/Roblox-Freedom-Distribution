return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local User = require(Modules.LuaApp.Models.User)
	local UserThumbnailDefaultOrientation = require(Modules.LuaApp.Components.Home.UserThumbnailDefaultOrientation)

	it("should create and destroy without errors", function()
		local element = Roact.createElement(UserThumbnailDefaultOrientation, {
			user = User.mock()
		})
		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end