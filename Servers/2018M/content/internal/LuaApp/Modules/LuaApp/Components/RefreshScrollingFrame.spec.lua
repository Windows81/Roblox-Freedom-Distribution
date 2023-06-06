return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)
	local RefreshScrollingFrame = require(Modules.LuaApp.Components.RefreshScrollingFrame)

	it("should create and destroy without errors, given only refresh function", function()
		local element = mockServices({
			scrollingFrame = Roact.createElement(RefreshScrollingFrame, {
				currentPage = "Games",
				refresh = function()
					return 1
				end,
				Size = UDim2.new(1, 0, 1, 0),
				BackgroundColor3 = Color3.fromRGB(0,0,0),
				Position = UDim2.new(0, 0, 0, 0),
			}),
		}, {
			includeStoreProvider = true,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)

	it("should create and destroy without errors, given only loadMore function", function()
		local element = mockServices({
			scrollingFrame = Roact.createElement(RefreshScrollingFrame, {
				currentPage = "Games",
				loadMore = function()
					return 1
				end,
				Size = UDim2.new(1, 0, 1, 0),
				BackgroundColor3 = Color3.fromRGB(0,0,0),
				Position = UDim2.new(0, 0, 0, 0),
			}),
		}, {
			includeStoreProvider = true,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)

	it("should create and destroy without errors, given both refresh and loadMore function", function()
		local element = mockServices({
			scrollingFrame = Roact.createElement(RefreshScrollingFrame, {
				currentPage = "Games",
				refresh = function()
					return 1
				end,
				loadMore = function()
					return 1
				end,
				Size = UDim2.new(1, 0, 1, 0),
				BackgroundColor3 = Color3.fromRGB(0,0,0),
				Position = UDim2.new(0, 0, 0, 0),
			}),
		}, {
			includeStoreProvider = true,
		})

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)
end