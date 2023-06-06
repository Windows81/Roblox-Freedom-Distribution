local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local Constants = require(Modules.LuaApp.Constants)
local LocalizedTextLabel = require(Modules.LuaApp.Components.LocalizedTextLabel)
local LocalizedTextButton = require(Modules.LuaApp.Components.LocalizedTextButton)

local FONT = Enum.Font.SourceSans
local TEXT_SIZE = 20

local IMAGE_WIDTH = 20
local IMAGE_HEIGHT = 20
local IMAGE_X_OFFSET = 15
local IMAGE_Y_OFFSET = 10
local LABEL_X_OFFSET = 60

local MoreRow = Roact.PureComponent:extend("MoreRow")

function MoreRow:init()
    self.state = {
        isButtonPressed = false,
    }

    self.onInputBegan = function()
        self:setState({
            isButtonPressed = true
        })
    end

    self.onInputEnded = function()
        self:setState({
            isButtonPressed = false
        })
    end

    self.onActivated = function()
        local onActivated = self.props.onActivated
        if onActivated then
            onActivated(self.props.onActivatedData)
        end
    end
end

function MoreRow:render()
    local size = self.props.Size
    local position = self.props.Position or UDim2.new(0, 0, 0, 0)
    local text = self.props.Text
    local image = self.props.Image
    local LayoutOrder = self.props.LayoutOrder
    local isButtonPressed = self.state.isButtonPressed

    local buttonBackgroundColor
    if isButtonPressed then
        buttonBackgroundColor = Constants.Color.GRAY5
    else
        buttonBackgroundColor = Constants.Color.WHITE
    end

    -- We have two cases: one with an image and one without.
    if image then
        return Roact.createElement("ImageButton", {
            Size = size,
            Position = position,
            BackgroundTransparency = 1,
            BorderSizePixel = 0,
            AutoButtonColor = false,
            LayoutOrder = LayoutOrder,
            [Roact.Event.Activated] = self.onActivated,
            -- Until we can get a better visual effect of the touch input, disable it!
            -- Also, remember to set BackgroundTransparency = 0 also.
            --[[
            BackgroundColor3 = buttonBackgroundColor,
            [Roact.Event.InputBegan] = self.onInputBegan,
            [Roact.Event.InputEnded] = self.onInputEnded,
            --]]
        }, {
            Image = Roact.createElement("ImageLabel", {
                Size = UDim2.new(0, IMAGE_WIDTH, 0, IMAGE_HEIGHT),
                Position = UDim2.new(0, IMAGE_X_OFFSET, 0, IMAGE_Y_OFFSET),
                BackgroundTransparency = 1,
                BorderSizePixel = 0,
                ClipsDescendants = false,
                Image = image,
            }),
            Text = Roact.createElement(LocalizedTextLabel, {
                Size = UDim2.new(1, 0, 1, 0),
                Position = UDim2.new(0, LABEL_X_OFFSET, 0, 0),
                BackgroundTransparency = 1,
                BorderSizePixel = 0,
                Font = FONT,
                Text = text,
                TextSize = TEXT_SIZE,
                TextXAlignment = Enum.TextXAlignment.Left,
                TextYAlignment = Enum.TextYAlignment.Center,
            }),
        })
    else
        return Roact.createElement(LocalizedTextButton, {
            Size = size,
            Position = position,
            BackgroundTransparency = 0,
            BorderSizePixel = 0,
            AutoButtonColor = false,
            LayoutOrder = LayoutOrder,
            Font = FONT,
            Text = text,
            TextSize = TEXT_SIZE,
            TextXAlignment = Enum.TextXAlignment.Center,
            TextYAlignment = Enum.TextYAlignment.Center,
            [Roact.Event.Activated] = self.onActivated,
            -- Implement the effect of the touch input.
            BackgroundColor3 = buttonBackgroundColor,
            [Roact.Event.InputBegan] = self.onInputBegan,
            [Roact.Event.InputEnded] = self.onInputEnded,
        })
    end
end

return MoreRow