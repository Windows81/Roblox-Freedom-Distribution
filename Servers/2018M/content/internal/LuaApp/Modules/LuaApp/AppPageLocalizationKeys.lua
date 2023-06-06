local AppPage = require(game:GetService("CoreGui").RobloxGui.Modules.LuaApp.AppPage)

return {
	[AppPage.None] = "CommonUI.Features.Label.Nil",
	[AppPage.Home] = "CommonUI.Features.Label.Home",
	[AppPage.Games] = "CommonUI.Features.Label.Game",
	[AppPage.Catalog] = "CommonUI.Features.Label.Catalog",
	[AppPage.AvatarEditor] = "CommonUI.Features.Label.Avatar",
	[AppPage.Friends] = "CommonUI.Features.Label.Friends",
	[AppPage.Chat] = "CommonUI.Features.Label.Chat",
	[AppPage.More] = "CommonUI.Features.Label.More",
}