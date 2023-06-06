return function()
    local MoreTable = require(script.Parent.MoreTable)

    local Modules = game:GetService("CoreGui").RobloxGui.Modules

    local Roact = require(Modules.Common.Roact)
    local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

    it("should create and destroy without errors", function()
        local itemList = {
            {
                Text = "CommonUI.Features.Label.Events",
                Image = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
                OnActivatedData = {
                    NotificationType = "VIEW_SUB_PAGE_IN_MORE",
                    NotificationData = "Events"
                },
            },
            {
                Text = "CommonUI.Features.Label.Blog",
                Image = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
                OnActivatedData = {
                    NotificationType = "VIEW_SUB_PAGE_IN_MORE",
                    NotificationData = "Blog"
                },
            },
        }
        local root = mockServices({
            element = Roact.createElement(MoreTable, {
                Items = itemList,
                RowHeight = 40,
                LayoutOrder = 1,
                onActivated = function() end,
            }),
        })

        local instance = Roact.mount(root)
        Roact.unmount(instance)
    end)
end