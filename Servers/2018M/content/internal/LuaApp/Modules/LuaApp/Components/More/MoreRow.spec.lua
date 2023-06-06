return function()
    local MoreRow = require(script.Parent.MoreRow)

    local Modules = game:GetService("CoreGui").RobloxGui.Modules

    local Roact = require(Modules.Common.Roact)
    local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

    it("should create/destroy OK with an image", function()
        local root = mockServices({
            element = Roact.createElement(MoreRow, {
                Text = "Application.Logout.Action.Logout",
                Size = UDim2.new(1, 25, 0, 40),
                Image = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
                LayoutOrder = 1,
                onActivatedData = {
                    NotificationType = "ACTION_LOG_OUT",
                    NotificationData = ""
                },
                onActivated = function() end,
            }),
        })

        local instance = Roact.mount(root)
        Roact.unmount(instance)
    end)

    it("should create/destroy OK without an image", function()
        local root = mockServices({
            element = Roact.createElement(MoreRow, {
                Text = "Application.Logout.Action.Logout",
                Size = UDim2.new(1, 25, 0, 40),
                Image = nil,
                LayoutOrder = 1,
                onActivatedData = {
                    NotificationType = "ACTION_LOG_OUT",
                    NotificationData = ""
                },
                onActivated = function() end,
            }),
        })

        local instance = Roact.mount(root)
        Roact.unmount(instance)
    end)
end