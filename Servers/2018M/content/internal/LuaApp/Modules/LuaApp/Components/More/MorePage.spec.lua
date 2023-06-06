return function()
    local MorePage = require(script.Parent.MorePage)

    local Modules = game:GetService("CoreGui").RobloxGui.Modules

    local Roact = require(Modules.Common.Roact)
    local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

    local function MockMorePage()
        return mockServices({
            MorePage = Roact.createElement(MorePage),
        }, {
            includeStoreProvider = true,
        })
    end

    it("should create and destroy without errors", function()
        local element = MockMorePage()
        local instance = Roact.mount(element)
        Roact.unmount(instance)
    end)
end