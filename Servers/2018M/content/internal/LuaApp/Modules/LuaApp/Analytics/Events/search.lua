-- search : sent when a user interacts with the search bar.
-- eventContext : (string) games, people, catalog, etc...
-- act : (string) The perfromed action. Can be open, submit, or cancel
-- keyword : (optional, string) what is being searched for
return function(eventStreamImpl, eventContext, act, keyword)
	assert(type(eventContext) == "string", "Expected eventContext to be a string")
	assert(type(act) == "string", "Expected act to be a string")
	if keyword then
		assert(type(keyword) == "string", "Expected keyword to be a string")
	end

	local eventName = "search"
	eventStreamImpl:setRBXEventStream(eventContext, eventName, {
		act = act,
		kwd = keyword,
	})
end