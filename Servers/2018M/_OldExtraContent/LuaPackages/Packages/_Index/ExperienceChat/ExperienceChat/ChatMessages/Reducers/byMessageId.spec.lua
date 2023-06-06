local CoreGui = game:GetService("CoreGui")
local ExperienceChat = CoreGui:FindFirstChild("ExperienceChat", true)
local globals = require(ExperienceChat.Dev.Jest).Globals
local expect = globals.expect
local ChatMessages = ExperienceChat.ExperienceChat.ChatMessages

return function()
	local SendChatMessage = require(ChatMessages.Actions.SendChatMessage)
	local byMessageId = require(ChatMessages.Reducers.byMessageId)

	describe("byMessageId", function()
		it("should be not nil by default", function()
			local defaultState = byMessageId(nil, {})

			expect(defaultState).never.toBeNil()
		end)

		it("should be unmodified by other actions", function()
			local oldState = byMessageId(nil, {})
			local newState = byMessageId(oldState, { type = "not a real action" })

			expect(oldState).toEqual(newState)
		end)

		it("should be changed using SendChatMessage", function()
			local state = byMessageId(nil, {})

			state = byMessageId(state, SendChatMessage("textChannelId", "messageId", "prefixText", "text"))
			expect(state.messageId.PrefixText).toEqual("prefixText")
			expect(state.messageId.Text).toEqual("text")
		end)
	end)
end
