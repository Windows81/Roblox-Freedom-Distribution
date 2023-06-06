local CoreGui = game:GetService("CoreGui")
local ExperienceChat = CoreGui:FindFirstChild("ExperienceChat", true)
local globals = require(ExperienceChat.Dev.Jest).Globals
local expect = globals.expect
local ChatMessages = ExperienceChat.ExperienceChat.ChatMessages
local SendChatMessage = require(ChatMessages.Actions.SendChatMessage)

return function()
	describe("SendChatMessage", function()
		it("should return correct action name", function()
			expect(SendChatMessage.name).toEqual("SendChatMessage")
		end)

		it("should return correct action type name", function()
			local action = SendChatMessage("", "", "", "")
			expect(action.type).toEqual(SendChatMessage.name)
		end)

		it("should return correct action prefixText and text", function()
			local action = SendChatMessage("textChannelId", "messageId", "prefixText", "text")
			expect(action.textChannelId).toEqual("textChannelId")
			expect(action.messageId).toEqual("messageId")
			expect(action.prefixText).toEqual("prefixText")
			expect(action.text).toEqual("text")
		end)
	end)
end
