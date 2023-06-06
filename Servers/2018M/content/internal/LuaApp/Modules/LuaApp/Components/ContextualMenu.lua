--
-- ContextualMenu
--
-- This module wraps the drop-down pop-out and pop-up menus and provides some
-- common functionality for managing those menus.
-- (Contains some code from PlayTogetherContextualMenu but made more generic.)
--

local CoreGui = game:GetService("CoreGui")
local Modules = CoreGui.RobloxGui.Modules
local LuaApp = Modules.LuaApp

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)

local Constants = require(LuaApp.Constants)
local FormFactor = require(LuaApp.Enum.FormFactor)
local FramePopOut = require(LuaApp.Components.FramePopOut)
local FramePopup = require(LuaApp.Components.FramePopup)
local ListPicker = require(LuaApp.Components.ListPicker)

local ContextualMenu = Roact.Component:extend("ContextualMenu")

local ITEM_HEIGHT = 54
local ITEM_WIDTH = 320
local VISIBLE_ITEMS = 5.58
local ITEM_FONT_SIZE = 23
local ITEM_TEXT_FONT = Enum.Font.SourceSans
local ITEM_TEXT_COLOR = Constants.Color.GRAY1

function ContextualMenu:render()
    -- Unpack props:
    local callbackCancel = self.props.callbackCancel
    local callbackSelect = self.props.callbackSelect
    local formFactor = self.props.formFactor
    local itemHeight = self.props.itemHeight or ITEM_HEIGHT
    local itemWidth = self.props.itemWidth or ITEM_WIDTH
    local menuItems = self.props.menuItems or {}
    local screenShape = self.props.screenShape

    -- Calculate local vars from props:
    local isTablet = (formFactor == FormFactor.TABLET)
    local itemCount = #menuItems

    local listContentsWidth = 0
    if isTablet then
        listContentsWidth = itemWidth
    end

    local listContents = {
        ListPicker = Roact.createElement(ListPicker, {
            onSelectItem = callbackSelect,
            items = menuItems,

            itemHeight = ITEM_HEIGHT,
            itemWidth = listContentsWidth,

            textColor = ITEM_TEXT_COLOR,
            textFont = ITEM_TEXT_FONT,
            textSize = ITEM_FONT_SIZE,
        }),
    }

    local portalContents
    if isTablet then
        portalContents = Roact.createElement(FramePopOut, {
            heightAllItems = itemHeight * itemCount,
            itemWidth = itemWidth,
            onCancel = callbackCancel,
            parentShape = screenShape,
        }, listContents)
    else
        portalContents = Roact.createElement(FramePopup, {
            heightAllItems = itemHeight * itemCount,
            heightScrollContainer = itemHeight * math.min(itemCount, VISIBLE_ITEMS),
            onCancel = callbackCancel,
        }, listContents)
    end

    return Roact.createElement(Roact.Portal, {
        target = CoreGui,
    }, {
        PortalUI = Roact.createElement("ScreenGui", {
            ZIndexBehavior = Enum.ZIndexBehavior.Sibling,
            DisplayOrder = 3
        }, {
            Contents = portalContents
        }),
    })
end

ContextualMenu = RoactRodux.connect(function(store, props)
    local state = store:getState()

    return {
        formFactor = state.FormFactor,
    }
end)(ContextualMenu)

return ContextualMenu