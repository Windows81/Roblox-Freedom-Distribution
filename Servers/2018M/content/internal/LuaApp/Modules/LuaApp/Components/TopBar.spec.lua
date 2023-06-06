return function()
	local TopBar = require(script.Parent.TopBar)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local Roact = require(Modules.Common.Roact)
	local Rodux = require(Modules.Common.Rodux)
	local AppReducer = require(Modules.LuaApp.AppReducer)
	local SetTopBarHeight = require(Modules.LuaApp.Actions.SetTopBarHeight)
	local mockServices = require(Modules.LuaApp.TestHelpers.mockServices)


	local function MockStore()
		return Rodux.Store.new(AppReducer)
	end

	local function MockTopBarElement(store)
		return mockServices({
			TopBar = Roact.createElement(TopBar, {
				showBackButton = true,
				showBuyRobux = true,
				showNotifications = true,
				showSearch = true,
				textKey = "CommonUI.Features.Label.Game",
			}),
		}, {
			includeStoreProvider = true,
			store = store
		})
	end

	it("should create and destroy without errors", function()
		local store = MockStore()
		local topBar = MockTopBarElement(store)

		local screenGui = Instance.new("ScreenGui")
		local instance = Roact.mount(topBar, screenGui)

		Roact.unmount(instance)
		store:destruct()
	end)

	it("should update when status bar size changes", function()
		local store = MockStore()
		local newTopBarHeight = 100
		store:dispatch(SetTopBarHeight(newTopBarHeight))

		local topBar = MockTopBarElement(store)
		local container = Instance.new("ScreenGui")
		local instance = Roact.mount(topBar, container, "TopBar")

		expect(container.TopBar.TopBar.AbsoluteSize.Y).to.equal(newTopBarHeight)

		Roact.unmount(instance)
		store:destruct()
	end)

end