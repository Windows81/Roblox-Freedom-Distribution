local CoreGui = game:GetService("CoreGui")
local Players = game:GetService("Players")

local Modules = CoreGui.RobloxGui.Modules

local ApiFetchUsersFriendCount = require(Modules.LuaApp.Thunks.ApiFetchUsersFriendCount)
local ApiFetchUsersData = require(Modules.LuaApp.Thunks.ApiFetchUsersData)
local AddUser = require(Modules.LuaApp.Actions.AddUser)
local UserModel = require(Modules.LuaApp.Models.User)


local ConversationModel = require(Modules.LuaChat.Models.Conversation)
local ReceivedConversation = require(Modules.LuaChat.Actions.ReceivedConversation)

local Constants = require(Modules.LuaApp.Constants)

return function(networking, addedFriendUserId)
	return function(store)
		return store:Dispatch(ApiFetchUsersFriendCount(networking)):andThen(function()
			-- Unfortunately this event does not pass in the username of the new friend.
			local username = Players:GetNameFromUserIdAsync(tonumber(addedFriendUserId))

			local newUser = UserModel.fromData(addedFriendUserId, username, true)
			store:Dispatch(AddUser(newUser))
			store:Dispatch(ApiFetchUsersData(
				networking,
				{addedFriendUserId},
				Constants.AvatarThumbnailRequests.USER_CAROUSEL
			)):andThen(function()

				-- LuaChat needs to create a mock 1:1 conversation for new friends
				local state = store:GetState()

				local needsMockConversation = true
				for _, conversation in pairs(state.ChatAppReducer.Conversations) do
					if conversation.conversationType == ConversationModel.Type.ONE_TO_ONE_CONVERSATION then
						for _, participantId in ipairs(conversation.participants) do
							if participantId == addedFriendUserId then
								needsMockConversation = false
								break
							end
						end
					end
				end

				if needsMockConversation then
					local conversation = ConversationModel.fromUser(newUser)
					store:Dispatch(ReceivedConversation(conversation))
				end
			end)

		end)
	end
end