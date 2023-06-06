--[[
The More page
_____________________
|                   |
|       TopBar      |
|___________________|
|                   |
|     List 1        |
|     List 2        |
|     List 3        |
|     List 4        |
|     Log Out       |
|___________________|
]]

local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)

local Constants = require(Modules.LuaApp.Constants)
local TopBar = require(Modules.LuaApp.Components.TopBar)
local FitChildren = require(Modules.LuaApp.FitChildren)

local MoreTable = require(Modules.LuaApp.Components.More.MoreTable)
local MoreRow = require(Modules.LuaApp.Components.More.MoreRow)

local AppGuiService = require(Modules.LuaApp.Services.AppGuiService)
local RoactServices = require(Modules.LuaApp.RoactServices)

local SECTION_PADDING = 25
local ROW_HEIGHT = 40
local X_PADDING = -10

local MorePage = Roact.PureComponent:extend("MorePage")

local function Spacer(props)
    local height = props.height or SECTION_PADDING
    local LayoutOrder = props.LayoutOrder

    return Roact.createElement("Frame", {
        Size = UDim2.new(1, 0, 0, height),
        BackgroundTransparency = 1,
        LayoutOrder = LayoutOrder,
    })
end

function MorePage:init()
    local notificationTypeList = self.props.guiService:GetNotificationTypeList()

    self.itemList1 = {
        {
            Text = "CommonUI.Features.Label.Catalog",
            Image = "rbxasset://textures/ui/LuaApp/icons/ic-catalog.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "Catalog"
            },
        },
        {
            Text = "CommonUI.Features.Label.BuildersClub",
            Image = "rbxasset://textures/ui/LuaApp/category/ic-bc.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "BuildersClub"
            },
        },
    }

    self.itemList2 = {
        {
            Text = "CommonUI.Features.Label.Profile",
            Image = "rbxasset://textures/ui/LuaApp/icons/ic-avatar.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "Profile"
            },
        },
        {
            Text = "CommonUI.Features.Label.Friends",
            Image = "rbxasset://textures/ui/LuaApp/icons/ic-friend.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "Friends"
            },
        },
        {
            Text = "CommonUI.Features.Label.Groups",
            Image = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "Groups"
            },
        },
        {
            Text = "CommonUI.Features.Label.Inventory",
            Image = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "Inventory"
            }
        },
        {
            Text = "CommonUI.Features.Label.Messages",
            Image = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "Messages"
            },
        },
        {
            Text = "CommonUI.Features.Label.CreateGames",
            Image = "rbxasset://textures/ui/LuaApp/icons/ic-games.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "CreateGames"
            },
        },
    }

    self.itemList3 = {
        {
            Text = "CommonUI.Features.Label.Events",
            Image = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "Events"
            },
        },
        {
            Text = "CommonUI.Features.Label.Blog",
            Image = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "Blog"
            },
        },
    }

    self.itemList4 = {
        {
            Text = "CommonUI.Features.Label.Settings",
            Image = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "Settings"
            },
        },
        {
            Text = "CommonUI.Features.Label.About",
            Image = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "About"
            },
        },
        {
            Text = "CommonUI.Features.Label.Help",
            Image = "rbxasset://textures/ui/LuaApp/category/ic-featured.png",
            OnActivatedData = {
                NotificationType = notificationTypeList.VIEW_SUB_PAGE_IN_MORE,
                NotificationData = "Help"
            },
        },
    }

    self.onActivated = function(activatedData)
        local notificationType = activatedData.NotificationType
        local notificationData = activatedData.NotificationData or ""
        self.props.guiService:BroadcastNotification(notificationData, notificationType)
    end
end

function MorePage:render()
    local topBarHeight = self.props.topBarHeight
    local currentLayoutOrder = 0
    local function nextLayoutOrder()
        currentLayoutOrder = currentLayoutOrder + 1
        return currentLayoutOrder
    end
    local notificationTypeList = self.props.guiService:GetNotificationTypeList()

    return Roact.createElement("Frame", {
        Size = UDim2.new(1, 0, 1, 0),
        BorderSizePixel = 0,
    }, {
        TopBar = Roact.createElement(TopBar, {
            showBackButton = false,
            showBuyRobux = true,
            showNotifications = true,
            showSearch = true,
            textKey = "CommonUI.Features.Label.More",
        }),
        Scroller = Roact.createElement(FitChildren.FitScrollingFrame, {
            Position = UDim2.new(0, 0, 0, topBarHeight),
            Size = UDim2.new(1, 0, 1, -topBarHeight),
            CanvasSize = UDim2.new(1, 0, 0, 0),
            BackgroundColor3 = Constants.Color.GRAY4,
            BorderSizePixel = 0,
            ScrollBarThickness = 0,
            fitFields = {
                CanvasSize = FitChildren.FitAxis.Height,
            },
        }, {
            Layout = Roact.createElement("UIListLayout", {
                SortOrder = Enum.SortOrder.LayoutOrder,
                HorizontalAlignment = Enum.HorizontalAlignment.Center,
            }),

            Roact.createElement(Spacer, {
                LayoutOrder = nextLayoutOrder(),
            }),

            Roact.createElement(MoreTable, {
                Items = self.itemList1,
                RowHeight = ROW_HEIGHT,
                LayoutOrder = nextLayoutOrder(),
                onActivated = self.onActivated,
            }),

            Roact.createElement(Spacer, {
                LayoutOrder = nextLayoutOrder(),
            }),

            Roact.createElement(MoreTable, {
                Items = self.itemList2,
                RowHeight = ROW_HEIGHT,
                LayoutOrder = nextLayoutOrder(),
                onActivated = self.onActivated,
            }),

            Roact.createElement(Spacer, {
                LayoutOrder = nextLayoutOrder(),
            }),

            Roact.createElement(MoreTable, {
                Items = self.itemList3,
                RowHeight = ROW_HEIGHT,
                LayoutOrder = nextLayoutOrder(),
                onActivated = self.onActivated,
            }),

            Roact.createElement(Spacer, {
                LayoutOrder = nextLayoutOrder(),
            }),

            Roact.createElement(MoreTable, {
                Items = self.itemList4,
                RowHeight = ROW_HEIGHT,
                LayoutOrder = nextLayoutOrder(),
                onActivated = self.onActivated,
            }),

            -- The last Log Out row.
            Roact.createElement(Spacer, {
                LayoutOrder = nextLayoutOrder(),
            }),

            Roact.createElement(MoreRow, {
                Text = "Application.Logout.Action.Logout",
                Size = UDim2.new(1, X_PADDING, 0, ROW_HEIGHT),
                Image = nil,
                LayoutOrder = nextLayoutOrder(),
                onActivatedData = {
                    NotificationType = notificationTypeList.ACTION_LOG_OUT,
                    NotificationData = ""
                },
                onActivated = self.onActivated,
            }),

            Roact.createElement(Spacer, {
                LayoutOrder = nextLayoutOrder(),
            }),
        }),
    })
end

MorePage = RoactRodux.connect(function(store, props)
    local state = store:getState()

    return {
        topBarHeight = state.TopBar.topBarHeight,
    }
end)(MorePage)

return RoactServices.connect({
	guiService = AppGuiService
})(MorePage)