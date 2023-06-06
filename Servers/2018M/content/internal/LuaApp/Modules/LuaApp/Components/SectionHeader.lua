local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)

local Constants = require(Modules.LuaApp.Constants)
local FitChildren = require(Modules.LuaApp.FitChildren)
local FitTextLabel = require(Modules.LuaApp.Components.FitTextLabel)

local SECTION_HEADER_HEIGHT = Constants.SECTION_HEADER_HEIGHT
local TEXT_SIZE = SECTION_HEADER_HEIGHT
local TEXT_FONT = Enum.Font.SourceSansLight

local SectionHeader = Roact.PureComponent:extend("SectionHeader")

SectionHeader.defaultProps = {
	Size = UDim2.new(1, 0, 0, SECTION_HEADER_HEIGHT),
}

function SectionHeader:render()
	local text = self.props.text
	local layoutOrder = self.props.LayoutOrder
	local size = self.props.Size
	local position = self.props.Position

	return Roact.createElement(FitTextLabel, {
		LayoutOrder = layoutOrder,
		Size = size,
		Position = position,
		BackgroundTransparency = 1,
		TextSize = TEXT_SIZE,
		TextColor3 = Constants.Color.GRAY1,
		Font = TEXT_FONT,
		Text = text,
		TextWrapped = true,
		TextXAlignment = Enum.TextXAlignment.Left,
		TextYAlignment = Enum.TextYAlignment.Top,
		fitAxis = FitChildren.FitAxis.Height,
	})
end

return SectionHeader