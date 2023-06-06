return function()
	local TokenRefreshComponent = require(script.Parent.TokenRefreshComponent)
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)

	local Roact = require(Modules.Common.Roact)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)

	it("should create and destroy without errors", function()
		local element = mockServices({
			TokenRefreshComponent = Roact.createElement(TokenRefreshComponent, {
				sortToRefresh = "Games",
				refresh = function() end,
				nextTokenRefreshTime = {["Games"] = 1},
				GameSortTokenFetchingStatus = {["Games"] = RetrievalStatus.NotStarted},
			})
		}, {
			includeStoreProvider = true,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end