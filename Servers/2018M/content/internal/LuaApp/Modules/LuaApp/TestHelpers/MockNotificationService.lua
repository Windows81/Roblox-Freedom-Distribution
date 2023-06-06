--[[
	A fake notification service for faking Notifications for tests
]]

local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Signal = require(Modules.Common.Signal)
local mockNotificationService = {}
mockNotificationService.__index = mockNotificationService

function mockNotificationService.ScheduleNotification(userId, alertId, alertMsg, minutesToFire)
end

function mockNotificationService.CancelNotification(userId, alertId)
end

function mockNotificationService.CancelAllNotification(userId)
end

function mockNotificationService.GetScheduledNotifications(userId)
end

function mockNotificationService.ActionEnabled(actionType)
end

function mockNotificationService.ActionTaken(actionType)
end

function mockNotificationService.new()
	local mns = {}

	mns.RobloxEventReceived = Signal.new()
	mns.RobloxConnectionChanged = Signal.new()

	setmetatable(mns, mockNotificationService)

	return mns
end

return mockNotificationService