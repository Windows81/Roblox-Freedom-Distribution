local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

local ProjectRoot = script:FindFirstAncestor("ExperienceChat").Parent

local App = require(script.Parent.App)
local createStore = require(script.Parent.createStore)

return function()
	local store = createStore()

	-- bind mock event listeners @TODO clean up later
	if ReplicatedStorage:WaitForChild("MockCoreGuiChatEvents", 3) then
		local SendChatMessage = require(ProjectRoot.ExperienceChat.ChatMessages.Actions.SendChatMessage)
		local mockEvents = ReplicatedStorage.MockCoreGuiChatEvents

		-- MockMessageReceived is a RemoteEvent to process received messages
		mockEvents.MockMessageReceived.OnClientEvent:Connect(function(textChatMessage)
			local textChannelId = textChatMessage.TextChannel.Name
			local messageId = textChatMessage.Metadata
			local playerName = textChatMessage.TextSource.Name
			local message = textChatMessage.Text
			store:dispatch(SendChatMessage(textChannelId, messageId, playerName, message))
		end)

		-- MockSendAsync is a BindableFunction to mock both client and server component
		mockEvents.MockSendAsync.OnInvoke = function(textChannel: Folder, message: string, metadata: string)
			-- Mock client SendingMessage event
			mockEvents.MockSendingMessage:Fire(textChannel, message, metadata)

			-- Mock server return result from SendAsync
			return mockEvents.MockServerSendAsync:InvokeServer(textChannel, message, metadata)
		end

		mockEvents.MockSendingMessage.Event:Connect(function(textChannel, outgoingString, outgoingMetadata)
			local textChannelId = textChannel.Name
			local messageId = outgoingMetadata
			local playerName = Players.LocalPlayer.Name
			local message = outgoingString
			store:dispatch(SendChatMessage(textChannelId, messageId, playerName, message))
		end)
	end

	return App
end
