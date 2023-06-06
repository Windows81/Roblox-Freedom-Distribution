--[[
		Creates a component for no friends
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local GlobalSettings = require(Modules.Shell.GlobalSettings)

return function(props)
	return Roact.createElement("Frame", {
		Size = UDim2.new(1, 0, 1, 0),
		BackgroundTransparency = 1
	}, {
		NoFriendsIcon = Roact.createElement("ImageLabel", {
			Size = UDim2.new(0, 296, 0, 259),
			Position = UDim2.new(0.5, -148, 0, 100),
			BackgroundTransparency = 1,
			Image = "rbxasset://textures/ui/Shell/Icons/FriendsIcon@1080.png",
		}),
		NoFriendsText = Roact.createElement("TextLabel", {
			Size = UDim2.new(0, 440, 0, 72),
			Position = UDim2.new(0.5, -220, 0, 392),
			BackgroundTransparency = 1,
			Font = GlobalSettings.RegularFont,
			FontSize = GlobalSettings.ButtonSize,
			TextColor3 = GlobalSettings.WhiteTextColor,
			Text = props.text,
			TextYAlignment = Enum.TextYAlignment.Top,
			TextWrapped = true
		}),
	})
end