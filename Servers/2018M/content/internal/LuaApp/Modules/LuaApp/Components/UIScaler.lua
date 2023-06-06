local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactMotion = require(Modules.LuaApp.RoactMotion)

local UIScaler = Roact.PureComponent:extend("UIScaler")

function UIScaler:render()
	local scaleValue = self.props.scaleValue
	local onRested = self.props.onRested

	return Roact.createElement(RoactMotion.SimpleMotion, {
		style = {
			scale = scaleValue,
		},
		onRested = onRested,
		render = function(values)
			return Roact.createElement("UIScale", {
				Scale = values.scale,
			})
		end,
	})
end

return UIScaler