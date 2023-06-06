local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Signal = require(Modules.Common.Signal)

local RobloxEventReceiver = {}
RobloxEventReceiver.__index = RobloxEventReceiver

function RobloxEventReceiver:observeEvent(namespace, detailType, callback)
	assert(type(namespace) == "string", "Expected namespace to be a string")
	assert(type(detailType) == "string", "Expected detailtType to be a string")
	assert(type(callback) == "function", "Expected callback to be a function")

	local detailTable = self.namespaceSingularTable[namespace]
	if detailTable == nil then
		detailTable = {}
		self.namespaceSingularTable[namespace] = detailTable
	end
	-- Check and make sure that someone is observing this detailType under said namespace
	local signal = detailTable[detailType]
	if signal == nil then
		signal = Signal.new()
		detailTable[detailType] = signal
	end
	-- return the signal's connection function
	return signal:Connect(callback)
end

function RobloxEventReceiver:observeBulkEvent(namespace, callback)
	assert(type(namespace) == "string", "Expected namespace to be a string")
	assert(type(callback) == "function", "Expected callback to be a function")

	local signal = self.namespaceBulkTable[namespace]
	if signal == nil then
		signal = Signal.new()
		self.namespaceBulkTable[namespace] = signal
	end

	-- return the signal's connection function
	return signal:Connect(callback)
end

function RobloxEventReceiver.new(notificationService)
	local self = {
		namespaceSingularTable = {},
		namespaceBulkTable = {},
	}
	setmetatable(self, RobloxEventReceiver)

	local notifySingularObservers = function(namespace, detailType, message)
		-- Check and make sure that someone is observing this namespace
		local detailTable = self.namespaceSingularTable[namespace]
		if detailTable == nil then
			return
		end
		-- Check and make sure that someone is observing this detailType under said namespace
		local signal = detailTable[detailType]
		if signal == nil then
			return
		end
		signal:Fire(message)
	end

	local notifyBulkObservers = function(namespace, messages)
		-- Check and make sure that someone is observing this namespace
		local signal = self.namespaceBulkTable[namespace]
		if signal == nil then
			return
		end
		signal:Fire(messages)
	end

	self.connection = notificationService.RobloxEventReceived:Connect(function(event)
		-- handle bulk and singular events
		if event.detailType == nil or event.detailType == "" then
			notifyBulkObservers(event.namespace, event.detail)
		else
			notifySingularObservers(event.namespace, event.detailType, event.detail)
		end

	end)
	return self
end


return RobloxEventReceiver