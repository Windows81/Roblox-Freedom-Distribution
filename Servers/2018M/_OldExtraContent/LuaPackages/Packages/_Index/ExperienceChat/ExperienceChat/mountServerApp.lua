-- will house channel creation logic
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TextService = game:GetService("TextService")

-- @TODO TextChatService should pass through here as a parameter, use when completed
return function()
	-- @TODO replace all mock events with actual API
	local mockEvents = {
		{ "MockSendAsync", "BindableFunction" },
		{ "MockServerSendAsync", "RemoteFunction" },
		{ "MockMessageReceived", "RemoteEvent" },
		{ "MockSendingMessage", "BindableEvent" },
	}

	local eventsFolder = Instance.new("Folder")
	eventsFolder.Name = "MockCoreGuiChatEvents"
	eventsFolder.Parent = ReplicatedStorage
	for _, eventData in ipairs(mockEvents) do
		local event = Instance.new(eventData[2])
		event.Name = eventData[1]
		event.Parent = eventsFolder
	end

	-- Mock server logic for SendAsync
	eventsFolder.MockServerSendAsync.OnServerInvoke =
		function(sendingPlayer: Player, textChannel: Folder, message: string, metadata: string)
			local returnTextChatMessage

			for _, toPlayer in pairs(Players:GetPlayers()) do
				-- Filter text
				message = TextService
					:FilterStringAsync(message, sendingPlayer.UserId)
					:GetChatForUserAsync(toPlayer.UserId)

				-- Create a mock TextSource
				local textSource = {
					Name = sendingPlayer.Name,
					UserId = sendingPlayer.UserId,
					CanSend = true,
				}

				-- Create a mock TextChatMessage
				local textChatMessage = {
					Text = message,
					TextSource = textSource,
					TextChannel = textChannel,
					Metadata = metadata,
					Status = "",
					Timestamp = 0,
					PrefixText = "",
				}
				if sendingPlayer == toPlayer then
					returnTextChatMessage = textChatMessage
				end

				eventsFolder.MockMessageReceived:FireClient(toPlayer, textChatMessage)
			end

			return returnTextChatMessage
		end

	-- @TODO replace create default channels folders with actual channels
	local defaultChannels = {
		{ "RBXGeneral" },
	}

	local channelsFolder = Instance.new("Folder")
	channelsFolder.Name = "MockCoreGuiChatChannels"
	channelsFolder.Parent = ReplicatedStorage

	for _, channelData in ipairs(defaultChannels) do
		local channel = Instance.new("Folder")
		channel.Name = channelData[1]
		channel.Parent = channelsFolder
	end
end
