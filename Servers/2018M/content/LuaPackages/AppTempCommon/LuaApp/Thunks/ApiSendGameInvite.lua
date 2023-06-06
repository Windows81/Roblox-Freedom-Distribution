local CorePackages = game:GetService("CorePackages")
local Players = game:GetService("Players")

local AppTempCommon = CorePackages.AppTempCommon
local Requests = CorePackages.AppTempCommon.LuaApp.Http.Requests

local ChatSendMessage = require(Requests.ChatSendMessage)
local ChatStartOneToOneConversation = require(Requests.ChatStartOneToOneConversation)
local Url = require(CorePackages.AppTempCommon.LuaApp.Http.Url)

local trimCharacterFromEndString = require(AppTempCommon.Temp.trimCharacterFromEndString)

local INVITE_MESSAGE = "Come join me in %s %s/games/%s"

return function(networkImpl, userId, placeInfo)
	local clientId = Players.LocalPlayer.UserId

	local trimmedUrl = trimCharacterFromEndString(Url.BASE_URL, "/")
	-- Construct the invite message based on place info
	local messageText = string.format(INVITE_MESSAGE,
		placeInfo.name, trimmedUrl, placeInfo.universeRootPlaceId
	)

	return function(store)
		return ChatStartOneToOneConversation(networkImpl, userId, clientId):andThen(function(result)
			local conversation = result.responseBody.conversation

			return ChatSendMessage(networkImpl, conversation.id, messageText):andThen(function(result)
				local data = result.responseBody
				local wasModerated = data.resultType ~= "Success"
				if wasModerated then
					warn("Game invite was moderated")
				end
				return {
					conversationId = conversation.id,
					placeId = placeInfo.universeRootPlaceId,
					wasModerated = wasModerated
				}
			end)
		end)
	end
end