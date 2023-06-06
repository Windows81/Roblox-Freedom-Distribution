return function(state, _)
	return {
		isChatInputBarVisible = state.ChatVisibility.isChatInputBarVisible,
		isChatWindowVisible = state.ChatVisibility.isChatWindowVisible,
		messages = state.ChatMessages.byMessageId,
		messageHistory = state.ChatMessages.byTextChannelId,
	}
end
