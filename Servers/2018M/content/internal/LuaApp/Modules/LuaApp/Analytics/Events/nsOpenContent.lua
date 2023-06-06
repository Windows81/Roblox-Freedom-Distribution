-- nsOpenContent : fired when the Notification Stream button is tapped.
-- eventContext: (string) The current page that is opened or context
-- countOfUnreadNotification: (string) count of unread messages in the notification stream
return function(eventStreamImpl, eventContext, countOfUnreadNotification)
	assert(type(eventContext) == "string", "Expected eventContext to be a string")
	assert(type(countOfUnreadNotification) == "number", "Expected countOfUnreadNotification to be a number")

	local eventName = "nsOpenContent"
	eventStreamImpl:setRBXEventStream(eventContext, eventName, {
		property = countOfUnreadNotification,
	})
end