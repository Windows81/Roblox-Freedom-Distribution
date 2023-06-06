local CoreGui = game:GetService("CoreGui")
local RunService = game:GetService("RunService")
local Workspace = game:GetService("Workspace")

local Modules = CoreGui.RobloxGui.Modules
local Constants = require(Modules.LuaChat.Constants)
local ExternalEventConnection = require(Modules.Common.RoactUtilities.ExternalEventConnection)
local Roact = require(Modules.Common.Roact)

local DEFAULT_ANIMATION_SPEED_MULTIPLIER = 1.75
local DEFAULT_DOT_COLOR = Constants.Color.GRAY3
local DEFAULT_DOT_HIGHLIGHT_COLOR = Constants.Color.BLUE_PRIMARY
local DEFAULT_DOT_SCALE = 0.7
local DEFAULT_INDICATOR_HEIGHT = 16
local DEFAULT_INDICATOR_WIDTH = 70

local DOT_COUNT = 3
local INDICATOR_RATIO = 35 / 8

local LoadingIndicator = Roact.PureComponent:extend("LoadingIndicator")

LoadingIndicator.defaultProps = {
	AnimationSpeedMultiplier = DEFAULT_ANIMATION_SPEED_MULTIPLIER,
	DotColor = DEFAULT_DOT_COLOR,
	DotHighlightColor = DEFAULT_DOT_HIGHLIGHT_COLOR,
	DotScale = DEFAULT_DOT_SCALE,
	Size = UDim2.new(0, DEFAULT_INDICATOR_WIDTH, 0, DEFAULT_INDICATOR_HEIGHT)
}

function LoadingIndicator:init()
	self.state = {
		timer = true,
	}

	self.renderSteppedCallback = function(dt)
		local nextState = {
			timer = not self.state.timer,
		}
		self:setState(nextState)
	end
end

function LoadingIndicator:render()
	local animationSpeedMultiplier = self.props.AnimationSpeedMultiplier
	local dotColor = self.props.DotColor
	local dotHighlightColor = self.props.DotHighlightColor
	local dotScale = self.props.DotScale
	local size = self.props.Size

	local deltaTime = (Workspace.DistributedGameTime * animationSpeedMultiplier) % DOT_COUNT
	local dotItems = {}

	dotItems["RatioConstraint"] = Roact.createElement("UIAspectRatioConstraint", {
		AspectRatio = INDICATOR_RATIO,
		AspectType = Enum.AspectType.FitWithinMaxSize,
	})

	for index = 1, DOT_COUNT do
		local backgroundColor = dotColor
		local currentYScale = dotScale
		local horizontalPosition = (index - 1) / (DOT_COUNT - 1)

		if deltaTime >= index - 1 and deltaTime <= index then
			local curve = math.sin(math.pi * (deltaTime % 1))
			currentYScale = currentYScale + (1 - currentYScale) * curve
			backgroundColor = dotColor:lerp(dotHighlightColor, curve)
		end

		dotItems[index] = Roact.createElement("Frame", {
			AnchorPoint = Vector2.new(horizontalPosition, 0.5),
			BackgroundColor3 = backgroundColor,
			BorderSizePixel = 0,
			Size = UDim2.new(dotScale, 0, currentYScale, 0),
			SizeConstraint = Enum.SizeConstraint.RelativeYY,
			Position = UDim2.new(horizontalPosition, 0, 0.5, 0),
		})
	end

	dotItems["RenderStepped"] = Roact.createElement(ExternalEventConnection, {
		callback = self.renderSteppedCallback,
		event = RunService.renderStepped,
	})

	return Roact.createElement("Frame", {
		AnchorPoint = self.props.AnchorPoint,
		BackgroundTransparency = 1,
		Position = self.props.Position,
		Size = size,
	}, dotItems)
end

return LoadingIndicator