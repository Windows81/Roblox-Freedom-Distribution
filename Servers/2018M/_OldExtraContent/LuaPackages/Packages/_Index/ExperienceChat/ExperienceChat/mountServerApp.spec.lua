local ReplicatedStorage = game:GetService("ReplicatedStorage")

-- @TODO add more suitable tests once the mocks are gone and actual APIs are inserted
return function()
	beforeAll(function(c)
		-- add TextChatService when it is ready
		c.textChatService = nil
		c.serverApp = require(script.Parent.mountServerApp)(c.textChatService)
		c.findChannel = function(channelName)
			if not c.textChatService then
				return ReplicatedStorage.MockCoreGuiChatChannels:FindFirstChild(channelName)
			end
		end
	end)

	it("SHOULD create RBXGeneral unconditionally", function(c)
		assert(c.findChannel("RBXGeneral"))
	end)
end
