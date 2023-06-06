local GuiService = game:GetService("GuiService")

local Success, EnumValues = pcall(GuiService.GetNotificationTypeList, GuiService)

--[[
	NOTE: This table is supposed to mirror the C++ enum values, when new types are added we will
	need to add we values to this table or tests may fail or produce unexpected results.
]]
local TESTEZ_ENUM_VALUES = {
    VIEW_PROFILE = 0,
    REPORT_ABUSE = 1,
    VIEW_GAME_DETAILS = 2,
    SHOW_TAB_BAR = 3,
    HIDE_TAB_BAR = 4,
    UNREAD_COUNT = 5,
    PRIVACY_SETTINGS = 6,
    BACK_BUTTON_NOT_CONSUMED = 7,
    PURCHASE_ROBUX = 8,
    VIEW_NOTIFICATIONS = 9,
    APP_READY = 10,
    CLOSE_MODAL = 11,
    VIEW_GAME_DETAILS_ANIMATED = 12,
    LAUNCH_GAME = 13,
    VIEW_MY_FEED = 14,
    SEARCH_GAMES = 15,
    GAMES_SEE_ALL = 16,
}

return Success and EnumValues or TESTEZ_ENUM_VALUES
