return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local User = require(Modules.LuaApp.Models.User)
	local UserThumbnail = require(Modules.LuaApp.Components.UserThumbnail)

	it("should create and destroy without errors", function()
		local element = Roact.createElement(UserThumbnail, {
			measurements = {
				THUMBNAIL_SIZE = 90,
				DROPSHADOW_SIZE = 98,

				USERNAME = {
					TEXT_LINE_HEIGHT = 20,
					TEXT_FONT_SIZE = 18,
					TEXT_TOP_PADDING = 3,
				},

				PRESENCE = {
					TEXT_TOP_PADDING = 3,
					TEXT_LINE_HEIGHT = 20,
					TEXT_FONT_SIZE = 15,

					ICONS = {
						[User.PresenceType.ONLINE] = "",
						[User.PresenceType.IN_GAME] = "",
						[User.PresenceType.IN_STUDIO] = "",
					},

					DROPSHADOW_MARGIN = 0,
					BORDER_DIAMETER = 14,
					ICON_OFFSET = 5,
					ICON_SIZE = 24,
				},

				PRESENCE_TEXT_HEIGHT = 0
			},
			user = User.mock()
		})
		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end