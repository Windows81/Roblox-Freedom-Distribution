-- Written by Kip Turner, Copyright Roblox 2015

local CoreGui = game:GetService("CoreGui")

local RobloxGui = CoreGui:FindFirstChild("RobloxGui")
local Modules = RobloxGui:FindFirstChild("Modules")
local ShellModules = Modules:FindFirstChild("Shell")

local Utility = require(ShellModules:FindFirstChild('Utility'))

local AssetManager = {}

function AssetManager.CreateShadow(zIndex)
	return Utility.Create'ImageLabel'
	{
		Name = 'Shadow';
		Image = 'rbxasset://textures/ui/Shell/Buttons/Generic9ScaleShadow.png';
		Size = UDim2.new(1,3,1,3);
		Position = UDim2.new(0,0,0,0);
		ScaleType = Enum.ScaleType.Slice;
		SliceCenter = Rect.new(10,10,28,28);
		BackgroundTransparency = 1;
		ZIndex = zIndex or 1;
	}
end

return AssetManager
