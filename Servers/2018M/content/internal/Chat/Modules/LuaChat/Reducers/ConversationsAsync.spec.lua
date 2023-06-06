return function()

	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local LuaChat = Modules.LuaChat

	local ConversationsAsyncReducer = require(LuaChat.Reducers.ConversationsAsync)

	local ReceivedLatestMessages = require(LuaChat.Actions.ReceivedLatestMessages)
	local ReceivedOldestConversation = require(LuaChat.Actions.ReceivedOldestConversation)
	local ReceivedPageConversations = require(LuaChat.Actions.ReceivedPageConversations)
	local RequestLatestMessages = require(LuaChat.Actions.RequestLatestMessages)
	local RequestPageConversations = require(LuaChat.Actions.RequestPageConversations)

	describe("initial state", function()
		it("should return an initial table when passed nil", function()
			local state = ConversationsAsyncReducer(nil, {})
			expect(state).to.be.a("table")
		end)
	end)

	describe("RequestPageConversations", function()
		it("should set the async state to true", function()
			local state = ConversationsAsyncReducer(nil, {})
			state = ConversationsAsyncReducer(state, RequestPageConversations())

			expect(state.pageConversationsIsFetching).to.equal(true)
		end)
	end)

	describe("ReceivedPageConversations", function()
		it("should set the async state to false", function()
			local state = ConversationsAsyncReducer(nil, {})
			state = ConversationsAsyncReducer(state, ReceivedPageConversations())

			expect(state.pageConversationsIsFetching).to.equal(false)
		end)
	end)

	describe("RequestLatestMessages", function()
		it("should set the async state to true", function()
			local state = ConversationsAsyncReducer(nil, {})
			state = ConversationsAsyncReducer(state, RequestLatestMessages())

			expect(state.latestMessagesIsFetching).to.equal(true)
		end)
	end)

	describe("ReceivedLatestMessages", function()
		it("should set the async state to false", function()
			local state = ConversationsAsyncReducer(nil, {})
			state = ConversationsAsyncReducer(state, ReceivedLatestMessages())

			expect(state.latestMessagesIsFetching).to.equal(false)
		end)
	end)

	describe("ReceivedOldestConversation", function()
		it("should set the oldestConversationIsFetched flag to true", function()
			local state = ConversationsAsyncReducer(nil, {})
			state = ConversationsAsyncReducer(state, ReceivedOldestConversation())

			expect(state.oldestConversationIsFetched).to.equal(true)
		end)
	end)

end