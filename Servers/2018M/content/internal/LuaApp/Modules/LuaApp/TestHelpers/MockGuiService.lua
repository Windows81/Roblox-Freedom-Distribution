local MockGuiService = {}

function MockGuiService.BroadcastNotification(data, notification)
end

function MockGuiService.GetNotificationTypeList()
    return { VIEW_SUB_PAGE_IN_MORE = "VIEW_SUB_PAGE_IN_MORE",
             ACTION_LOG_OUT = "ACTION_LOG_OUT", }
end
function MockGuiService.SetGlobalGuiInset(x1, y1, x2, y2)
end

function MockGuiService.SafeZoneOffsetsChanged()
end

return MockGuiService