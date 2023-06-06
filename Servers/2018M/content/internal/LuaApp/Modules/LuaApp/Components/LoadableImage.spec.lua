return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local Roact = require(Modules.Common.Roact)
	local LoadableImage = require(script.parent.LoadableImage)

	local testImage = "https://t5.rbxcdn.com/ed422c6fbb22280971cfb289f40ac814"
	local defaultLoadImage = "rbxasset://textures/ui/LuaApp/icons/ic-game.png"

	describe("LoadableImage", function()
		it("should create and destroy without errors", function()
			local element = Roact.createElement(LoadableImage, {
					Image = testImage,
					Size = UDim2.new(0, 80, 0, 80),
					Position = UDim2.new(0, 50, 0, 50),
					BorderSizePixel = 0,
					BackgroundColor3 = Color3.new(0,0,0),
					loadingImage = defaultLoadImage,
				})
			local instance = Roact.mount(element)
			Roact.unmount(instance)
		end)

		it("should not set loading image if image is already in cache", function()
			LoadableImage._mockPreloadDone(testImage)
			local element = Roact.createElement(LoadableImage, {
					Image = testImage,
					Size = UDim2.new(0, 80, 0, 80),
					Position = UDim2.new(0, 50, 0, 50),
					BorderSizePixel = 0,
					BackgroundColor3 = Color3.new(0,0,0),
					loadingImage = defaultLoadImage,
				})
			local container = Instance.new("Folder")
			local instance = Roact.mount(element, container, "LoadableImageSample")
			expect(container.LoadableImageSample.Image).never.to.equal(defaultLoadImage)
			Roact.unmount(instance)
		end)
	end)
end