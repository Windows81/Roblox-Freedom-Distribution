return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local User = require(Modules.LuaApp.Models.User)
	local UserThumbnailPortraitOrientation = require(Modules.LuaApp.Components.Home.UserThumbnailPortraitOrientation)

	it("should create and destroy without errors", function()
		local element = Roact.createElement(UserThumbnailPortraitOrientation, {
			user = User.mock()
		})
		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end