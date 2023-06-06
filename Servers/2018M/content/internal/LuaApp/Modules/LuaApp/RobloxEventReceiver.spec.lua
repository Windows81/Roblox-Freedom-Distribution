local mockNotificationService = {}
mockNotificationService.__index = mockNotificationService

function mockNotificationService.new()
	local self = {}
	setmetatable(self, mockNotificationService)
	self.RobloxEventReceived = {}

	function self.RobloxEventReceived:Connect(callback)
		self.connection = callback
	end

	function self.RobloxEventReceived:send(event)
		self.connection(event)
	end
	return self
end

return function()
	local RobloxEventReceiver = require(game:GetService("CoreGui").RobloxGui.Modules.LuaApp.RobloxEventReceiver)
	it("should be able to be created", function()
		RobloxEventReceiver.new(mockNotificationService.new())
	end)

	describe("should have the correct api", function()
		it("should require a notificationService", function()
			expect(function()
				RobloxEventReceiver.new(nil)
			end).to.throw()
			expect(function()
				RobloxEventReceiver.new({})
			end).to.throw()
			RobloxEventReceiver.new(mockNotificationService.new())
		end)

		it("should throw on bad arguments for observeEvent", function()
			local eventReceiver = RobloxEventReceiver.new(mockNotificationService.new())
			expect(function()
				eventReceiver:observeEvent()
			end).to.throw()
			expect(function()
				eventReceiver:observeEvent({},"detailType", function()end)
			end).to.throw()
			expect(function()
				eventReceiver:observeEvent("namespace", {}, function()end)
			end).to.throw()
			expect(function()
				eventReceiver:observeEvent("namespace", "detailType", {})
			end).to.throw()
			expect(function()
				eventReceiver:observeEvent("namespace", function()end)
			end).to.throw()
			-- normal call
			local connection = eventReceiver:observeEvent("namespace", "detailType", function()end)
			connection:Disconnect()
		end)

		it("should throw on bad arguments for observeBulkEvent", function()
			local eventReceiver = RobloxEventReceiver.new(mockNotificationService.new())
			expect(function()
				eventReceiver:observeBulkEvent()
			end).to.throw()
			expect(function()
				eventReceiver:observeBulkEvent({}, function()end)
			end).to.throw()
			expect(function()
				eventReceiver:observeBulkEvent("namespace", {})
			end).to.throw()
			expect(function()
				eventReceiver:observeBulkEvent("namespace","detailType", function() end)
			end).to.throw()
			-- normal call
			local connection = eventReceiver:observeBulkEvent("namespace", function()end)
			connection:Disconnect()
		end)
	end)

	describe("handle observer", function()
		it("takes a singular observer", function()
			local eventReceiver = RobloxEventReceiver.new(mockNotificationService.new())
			local connection = eventReceiver:observeEvent("namespace", "detail", function()
				error("Should not call this callback")
			end)
			connection.Disconnect()
		end)

		it("takes a bulk observer", function()
			local eventReceiver = RobloxEventReceiver.new(mockNotificationService.new())
			local connection = eventReceiver:observeBulkEvent("namespaceBulk", function()
				error("Should not call this callback")
			end)
			connection.Disconnect()
		end)

		it("notifies and disconnects singular observer", function()
			local mns = mockNotificationService.new()
			local eventReceiver = RobloxEventReceiver.new(mns)
			local count = 0
			local test_message = "Test Message"
			local namespace = "namespaceSingular"
			local detailType = "detail"

			local connection = eventReceiver:observeEvent(namespace, detailType, function(message)
				count = count + 1
				expect(message).to.equal(test_message)
			end)
			mns.RobloxEventReceived:send({
				namespace = namespace,
				detailType = detailType,
				detail = test_message,
			})

			expect(count).to.equal(1)
			connection.Disconnect()

			mns.RobloxEventReceived:send({
				namespace = namespace,
				detailType = detailType,
				detail = test_message,
			})
			expect(count).to.equal(1)
		end)

		it("notifies and disconnects bulk observer", function()
			local mns = mockNotificationService.new()
			local eventReceiver = RobloxEventReceiver.new(mns)
			local count = 0
			local test_message = {"MESSAGE1", "MESSAGE2"}
			local namespace = "namespaceBulk"

			local connection = eventReceiver:observeBulkEvent(namespace, function(message)
				count = count + 1
				expect(message).to.equal(test_message)
			end)
			mns.RobloxEventReceived:send({
				namespace = namespace,
				detail = test_message,
			})

			expect(count).to.equal(1)
			connection.Disconnect()

			mns.RobloxEventReceived:send({
				namespace = namespace,
				detail = test_message,
			})
			expect(count).to.equal(1)
		end)
	end)

	describe("handle multiple observers", function()
		it("notifies and disconnects singular observers", function()
			local mns = mockNotificationService.new()
			local eventReceiver = RobloxEventReceiver.new(mns)
			local count = 0
			local test_message = "Test Message"
			local namespace = "namespaceSingular"
			local detailType = "detail"

			local connection = eventReceiver:observeEvent(namespace, detailType, function(message)
				count = count + 1
				expect(message).to.equal(test_message)
			end)
			local connection2 = eventReceiver:observeEvent(namespace, detailType, function(message)
				count = count + 1
				expect(message).to.equal(test_message)
			end)
			mns.RobloxEventReceived:send({
				namespace = namespace,
				detailType = detailType,
				detail = test_message,
			})

			expect(count).to.equal(2)
			connection.Disconnect()
			connection2.Disconnect()

			mns.RobloxEventReceived:send({
				namespace = namespace,
				detailType = detailType,
				detail = test_message,
			})
			expect(count).to.equal(2)
		end)

		it("notifies and disconnects bulk observers", function()
			local mns = mockNotificationService.new()
			local eventReceiver = RobloxEventReceiver.new(mns)
			local count = 0
			local test_message = {"MESSAGE1", "MESSAGE2"}
			local namespace = "namespaceBulk"

			local connection = eventReceiver:observeBulkEvent(namespace, function(message)
				count = count + 1
				expect(message).to.equal(test_message)
			end)
			local connection2 = eventReceiver:observeBulkEvent(namespace, function(message)
				count = count + 1
				expect(message).to.equal(test_message)
			end)

			mns.RobloxEventReceived:send({
				namespace = namespace,
				detail = test_message,
			})

			expect(count).to.equal(2)
			connection.Disconnect()
			connection2.Disconnect()

			mns.RobloxEventReceived:send({
				namespace = namespace,
				detail = test_message,
			})
			expect(count).to.equal(2)
		end)

		it("notifies and disconnects singular and bulk observers", function()
			local mns = mockNotificationService.new()
			local eventReceiver = RobloxEventReceiver.new(mns)
			local countSingular = 0
			local countBulk = 0
			local test_message = {"MESSAGE1", "MESSAGE2"}
			local namespaceSingular = "test_message"
			local detailType = "detailType"
			local namespaceBulk = "namespaceBulk"

			local connection = eventReceiver:observeEvent(namespaceSingular, detailType, function(message)
				countSingular = countSingular + 1
				expect(message).to.equal(test_message)
			end)
			local connection2 = eventReceiver:observeBulkEvent(namespaceBulk, function(message)
				countBulk = countBulk + 1
				expect(message).to.equal(test_message)
			end)

			mns.RobloxEventReceived:send({
				namespace = namespaceSingular,
				detailType = detailType,
				detail = test_message,
			})

			expect(countSingular).to.equal(1)
			expect(countBulk).to.equal(0)

			mns.RobloxEventReceived:send({
				namespace = namespaceBulk,
				detail = test_message,
			})

			expect(countSingular).to.equal(1)
			expect(countBulk).to.equal(1)
			connection.Disconnect()
			connection2.Disconnect()

			mns.RobloxEventReceived:send({
				namespace = namespaceSingular,
				detailType = detailType,
				detail = test_message,
			})
			mns.RobloxEventReceived:send({
				namespace = namespaceBulk,
				detail = test_message,
			})

			expect(countSingular).to.equal(1)
			expect(countBulk).to.equal(1)
		end)
	end)

	describe("should not call when", function()
		it("deals with different namespace for singular", function()
			local mns = mockNotificationService.new()
			local eventReceiver = RobloxEventReceiver.new(mns)
			local test_message = "Test Message"
			local namespace = "namespaceSingular"
			local detailType = "detail"

			local connection = eventReceiver:observeEvent("differentNameSpace", detailType, function(message)
				error("Should not call this callback")
			end)
			mns.RobloxEventReceived:send({
				namespace = namespace,
				detailType = detailType,
				detail = test_message,
			})

			connection.Disconnect()
		end)

		it("deals with different namespace for bulk", function()
			local mns = mockNotificationService.new()
			local eventReceiver = RobloxEventReceiver.new(mns)
			local test_message = "Test Message"
			local namespace = "namespaceSingular"

			local connection = eventReceiver:observeBulkEvent("differentNameSpace", function(message)
				error("Should not call this callback")
			end)
			mns.RobloxEventReceived:send({
				namespace = namespace,
				detail = test_message,
			})

			connection.Disconnect()
		end)

		it("deals with different detailTypes for singular", function()
			local mns = mockNotificationService.new()
			local eventReceiver = RobloxEventReceiver.new(mns)
			local test_message = "Test Message"
			local namespace = "namespaceSingular"
			local detailType = "detail"

			local connection = eventReceiver:observeEvent(namespace, "differentType", function(message)
				error("Should not call this callback")
			end)
			mns.RobloxEventReceived:send({
				namespace = namespace,
				detailType = detailType,
				detail = test_message,
			})

			connection.Disconnect()
		end)

		it("expects a singlular event", function()
			local mns = mockNotificationService.new()
			local eventReceiver = RobloxEventReceiver.new(mns)
			local test_message = "Test Message"
			local namespace = "namespaceSingular"

			local connection = eventReceiver:observeEvent(namespace, "differentType", function(message)
				error("Should not call this callback")
			end)
			mns.RobloxEventReceived:send({
				namespace = namespace,
				detail = test_message,
			})

			connection.Disconnect()
		end)

		it("expects a bulk event", function()
			local mns = mockNotificationService.new()
			local eventReceiver = RobloxEventReceiver.new(mns)
			local test_message = "Test Message"
			local namespace = "namespaceSingular"
			local detailType = "detail"

			local connection = eventReceiver:observeBulkEvent(namespace, function(message)
				error("Should not call this callback")
			end)
			mns.RobloxEventReceived:send({
				namespace = namespace,
				detailType = detailType,
				detail = test_message,
			})

			connection.Disconnect()
		end)
	end)
end