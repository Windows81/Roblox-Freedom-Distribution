local CoreGui = game:GetService("CoreGui")
local ExperienceChat = CoreGui:FindFirstChild("ExperienceChat", true)
local globals = require(ExperienceChat.Dev.Jest).Globals
local expect = globals.expect

return function()
	beforeAll(function(rootContext)
		local storyDefinition = require(script.Parent:FindFirstChild("ChatWindow.story"))
		rootContext.mount = rootContext.createMount(storyDefinition.story, function(c)
			return {
				messages = c.messages,
				messageHistory = c.messageHistory,
				messageLimit = c.messageLimit,
			}
		end)
	end)

	describe("GIVEN a short messageHistory", function()
		beforeAll(function(c)
			c.messages = {
				id1 = { PrefixText = "First", Text = "First" },
				id2 = { PrefixText = "Second", Text = "Second" },
				id3 = { PrefixText = "Third", Text = "Third" },
			}
			c.messageHistory = {
				RBXGeneral = { "id1", "id2", "id3" },
			}
		end)

		it("SHOULD mount the messages in descending order", function(c)
			local instance = c:mount().instance

			local firstMessage = c.findFirstInstance(instance, { Text = "First: First" })
			local secondMessage = c.findFirstInstance(instance, { Text = "Second: Second" })
			local thirdMessage = c.findFirstInstance(instance, { Text = "Third: Third" })
			expect(firstMessage).never.toBeNil()
			expect(secondMessage).never.toBeNil()
			expect(thirdMessage).never.toBeNil()

			expect(firstMessage).toBeAbove(secondMessage)
			expect(secondMessage).toBeAbove(thirdMessage)
		end)

		it("SHOULD only mount messages if TextChatMessage.Status is success", function(c)
			c.messages["id1"].Status = Enum.TextChatMessageStatus.Success
			c.messages["id2"].Status = Enum.TextChatMessageStatus.Success
			c.messages["id3"].Status = Enum.TextChatMessageStatus.InvalidPrivacySettings

			local instance = c:mount().instance
			local firstMessage = c.findFirstInstance(instance, { Text = "First: First" })
			local secondMessage = c.findFirstInstance(instance, { Text = "Second: Second" })
			local thirdMessage = c.findFirstInstance(instance, { Text = "Third: Third" })

			expect(firstMessage).never.toBeNil()
			expect(secondMessage).never.toBeNil()
			expect(thirdMessage).toBeNil()
		end)

		it("SHOULD order messages by TextChatMessage.Timestamp property", function(c)
			c.messages["id3"].Status = Enum.TextChatMessageStatus.Success
			c.messages["id1"].Timestamp = 1637621912
			c.messages["id2"].Timestamp = 1637621910
			c.messages["id3"].Timestamp = 1637621913
			-- Order of messages should be secondMessage, firstMessage, thirdMessage

			local instance = c:mount().instance
			local firstMessage = c.findFirstInstance(instance, { Text = "First: First" })
			local secondMessage = c.findFirstInstance(instance, { Text = "Second: Second" })
			local thirdMessage = c.findFirstInstance(instance, { Text = "Third: Third" })

			expect(secondMessage).toBeAbove(firstMessage)
			expect(firstMessage).toBeAbove(thirdMessage)
		end)
	end)

	describe("GIVEN a messageLimit", function()
		beforeAll(function(c)
			c.messages = {
				id1 = { PrefixText = "First", Text = "First" },
				id2 = { PrefixText = "Second", Text = "Second" },
				id3 = { PrefixText = "Third", Text = "Third" },
			}
			c.messageHistory = {
				RBXGeneral = { "id1", "id2", "id3" },
			}

			c.getNumMessages = function(instance)
				local scrollingFrame = c.findFirstInstance(instance, { ClassName = "ScrollingFrame" })
				local scrollingFrameChildren = scrollingFrame:GetChildren()
				local numMessages = 0
				for i = 1, #scrollingFrameChildren do
					if scrollingFrameChildren[i].ClassName == "TextLabel" then
						numMessages += 1
					end
				end
				return numMessages
			end
		end)

		it("SHOULD mount all messages when messageLimit not met", function(c)
			c.messageLimit = 100
			local mountResult = c:mount()
			expect(c.getNumMessages(mountResult.instance)).toEqual(3)
			mountResult.unmount()
		end)

		it("SHOULD never mount more messages than messageLimit", function(c)
			c.messageLimit = 1
			-- 3 messages in messageHistory but only 1 should be shown in chat
			local mountResult = c:mount()
			expect(c.getNumMessages(mountResult.instance)).toEqual(1)
			mountResult.unmount()
		end)

		it("SHOULD unmount older messages when messageLimit met", function(c)
			c.messageLimit = 2
			local mountResult = c:mount()
			local scrollingFrame = c.findFirstInstance(mountResult.instance, { ClassName = "ScrollingFrame" })
			local scrollingFrameChildren = scrollingFrame:GetChildren()
			for i = 1, #scrollingFrameChildren do
				expect(scrollingFrameChildren[i]).never.toEqual("message1")
				-- message1 should be not be rendered when there are 3 messages but 2 is the limit
			end
		end)
	end)
end
