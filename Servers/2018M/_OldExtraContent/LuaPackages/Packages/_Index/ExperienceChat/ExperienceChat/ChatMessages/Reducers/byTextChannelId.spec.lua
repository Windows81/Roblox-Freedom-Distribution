local CoreGui = game:GetService("CoreGui")
local ExperienceChat = CoreGui:FindFirstChild("ExperienceChat", true)
local globals = require(ExperienceChat.Dev.Jest).Globals
local expect = globals.expect
local ChatMessages = ExperienceChat.ExperienceChat.ChatMessages

return function()
	local SendChatMessage = require(ChatMessages.Actions.SendChatMessage)
	local byTextChannelId = require(ChatMessages.Reducers.byTextChannelId)

	describe("byMessageId", function()
		it("should be not nil by default", function()
			local defaultState = byTextChannelId(nil, {})

			expect(defaultState).never.toBeNil()
		end)

		it("should be unmodified by other actions", function()
			local oldState = byTextChannelId(nil, {})
			local newState = byTextChannelId(oldState, { type = "not a real action" })

			expect(oldState).toEqual(newState)
		end)

		it("should be changed using SendChatMessage", function()
			local state = byTextChannelId(nil, {})

			state = byTextChannelId(state, SendChatMessage("textChannelId", "messageId", "prefixText", "text"))
			expect(state.textChannelId[1]).toEqual("messageId")
		end)

		it("should handle existing messageId entries", function()
			local state = byTextChannelId(nil, {})

			state = byTextChannelId(state, SendChatMessage("textChannelId", "messageId", "prefixText", "text"))
			state = byTextChannelId(state, SendChatMessage("textChannelId", "messageId", "prefixText", "newText"))
			expect(state.textChannelId[1]).toEqual("messageId")
			expect(state.textChannelId[2]).toBeNil()
		end)
	end)
end
