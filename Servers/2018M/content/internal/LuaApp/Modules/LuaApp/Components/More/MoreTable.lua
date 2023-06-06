local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local Constants = require(Modules.LuaApp.Constants)
local Line = require(Modules.LuaApp.Components.Line)

local MoreRow = require(Modules.LuaApp.Components.More.MoreRow)

local X_PADDING = -10
local DIVIDER_HEIGHT = 1
local DIVIDER_LEFT_MARGIN = 50

local MoreTable = Roact.PureComponent:extend("MoreTable")

local function Divider(props)
    local height = props.height or DIVIDER_HEIGHT
    local xOffset = props.xOffset or DIVIDER_LEFT_MARGIN
    local LayoutOrder = props.LayoutOrder

    return Roact.createElement("Frame", {
        Size = UDim2.new(1, 0, 0, height),
        BorderSizePixel = 0,
        BackgroundTransparency = 1,
        LayoutOrder = LayoutOrder
    }, {
        Roact.createElement(Line, {
            Position = UDim2.new(0, xOffset, 0, 0),
        }),
    })
end

function MoreTable:render()
    local items = self.props.Items
    local rowHeight = self.props.RowHeight
    local LayoutOrder = self.props.LayoutOrder
    local onActivated = self.props.onActivated

    local listContents = {}

    listContents["Layout"] = Roact.createElement("UIListLayout", {
        SortOrder = Enum.SortOrder.LayoutOrder,
        HorizontalAlignment = Enum.HorizontalAlignment.Center,
    })

    local currentLayoutOrder = 0
    local function nextLayoutOrder()
        currentLayoutOrder = currentLayoutOrder + 1
        return currentLayoutOrder
    end

    local rowCount = 0
    for position, item in ipairs(items) do
        rowCount = rowCount + 1
        listContents[rowCount] = Roact.createElement(MoreRow, {
            LayoutOrder = nextLayoutOrder(),
            Size = UDim2.new(1, 0, 0, rowHeight),
            Text = item.Text,
            Image = item.Image,
            onActivatedData = item.OnActivatedData,
            onActivated = onActivated,
        })

        if position < #items then
            rowCount = rowCount + 1
            listContents[rowCount] = Roact.createElement(Divider, {
                LayoutOrder = nextLayoutOrder(),
            })
        end
    end

    return Roact.createElement("Frame", {
        Size = UDim2.new(1, X_PADDING, 0, rowHeight * #items),
        BackgroundTransparency = 0,
        BackgroundColor3 = Constants.Color.WHITE,
        BorderColor3 = Constants.Color.WHITE,
        LayoutOrder = LayoutOrder
    }, listContents)
end

return MoreTable