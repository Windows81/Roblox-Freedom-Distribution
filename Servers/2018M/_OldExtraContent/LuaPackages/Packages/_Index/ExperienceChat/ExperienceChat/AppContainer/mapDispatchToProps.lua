local HttpService = game:GetService("HttpService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local ExperienceChat = script:FindFirstAncestor("ExperienceChat")
local Packages = ExperienceChat.Parent
local Promise = require(Packages.Promise)

local ChatTopBarButtonActivated = require(ExperienceChat.ChatVisibility.Actions.ChatTopBarButtonActivated)
local TextChatServiceChatWindowPropertyChanged = require(
	ExperienceChat.ChatVisibility.Actions.TextChatServiceChatWindowPropertyChanged
)
local SendChatMessage = require(ExperienceChat.ChatMessages.Actions.SendChatMessage)

return function(dispatch)
	return {
		chatTopBarButtonActivated = function()
			dispatch(ChatTopBarButtonActivated)
		end,

		textChatServiceChatWindowPropertyChanged = function()
			dispatch(TextChatServiceChatWindowPropertyChanged)
		end,

		-- * @TODO remove SendChatMessage action and related elements when bridge to SendAsync is done
		onSendChat = function(message)
			local playerName = game.Players.LocalPlayer.Name

			-- generate messageId
			local textChannelId = "RBXGeneral"
			local messageId = HttpService:GenerateGUID(false)

			if ReplicatedStorage:FindFirstChild("MockCoreGuiChatEvents") then
				local targetTextChannel = ReplicatedStorage.MockCoreGuiChatChannels.RBXGeneral

				-- metadata is messageId for now
				Promise.try(function()
					ReplicatedStorage.MockCoreGuiChatEvents.MockSendAsync:Invoke(targetTextChannel, message, messageId)
				end)
			else
				dispatch(SendChatMessage(textChannelId, messageId, playerName, message))
			end
		end,
	}
end
