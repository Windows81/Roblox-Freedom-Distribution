local PlayerService = game:GetService("Players")

return function(eventStreamImpl, eventContext, conversationId, placeId)
	assert(type(eventContext) == "string", "Expected eventContext to be a string")
	assert(type(conversationId) == "string", "Expected conversationId to be a string")
	assert(type(placeId) == "string", "Expected placeId to be a string")

	local eventName = "loadGameLinkCardInChat"

	local player = PlayerService.LocalPlayer
	local userId = "UNKNOWN"
	if player then
		userId = tostring(player.UserId)
	end

	eventStreamImpl:setRBXEventStream(eventContext, eventName, {
		uid = userId,
		cid = conversationId,
		pid = placeId,
	})
end