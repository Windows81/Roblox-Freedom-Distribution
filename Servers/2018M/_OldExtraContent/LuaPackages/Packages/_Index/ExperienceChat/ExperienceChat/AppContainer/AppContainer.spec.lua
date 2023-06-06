local CoreGui = game:GetService("CoreGui")
local ExperienceChat = CoreGui:FindFirstChild("ExperienceChat", true)
local globals = require(ExperienceChat.Dev.Jest).Globals
local expect = globals.expect
local ChatVisibility = ExperienceChat.ExperienceChat.ChatVisibility
local ChatTopBarButtonActivated = require(ChatVisibility.Actions.ChatTopBarButtonActivated)
local TextChatServiceChatWindowPropertyChanged = require(
	ChatVisibility.Actions.TextChatServiceChatWindowPropertyChanged
)
local ChatMessages = ExperienceChat.ExperienceChat.ChatMessages
local SendChatMessage = require(ChatMessages.Actions.SendChatMessage)

local Timer = require(ExperienceChat.ExperienceChat.Timer)

return function()
	beforeAll(function(rootContext)
		local storyDefinition = require(script.Parent:FindFirstChild("AppContainer.story"))
		local installReducer = require(script.Parent.Parent.installReducer)
		rootContext.mount = function(initialState, context, createProps)
			createProps = createProps or function() end
			local Roact = context.Roact
			local RoactRodux = context.RoactRodux
			local storyMiddleware = context.storyMiddleware
			local instance = Instance.new("ScreenGui")
			instance.Parent = game:GetService("CoreGui")

			local middlewares = {
				context.Rodux.thunkMiddleware,
			}
			local store = context.Rodux.Store.new(installReducer(), initialState, middlewares)

			local tree = Roact.createElement(RoactRodux.StoreProvider, {
				store = store,
			}, {
				container = Roact.createElement(storyMiddleware(storyDefinition.story), createProps(context)),
			})
			local roactInstance = Roact.mount(tree, instance)
			return {
				instance = instance,
				unmount = function()
					Roact.unmount(roactInstance)
					instance:Destroy()
				end,
				store = store,
			}
		end

		rootContext.createChatVisibilityInitialState = function(isChatWindowVisible, isChatInputBarVisible)
			return {
				ChatVisibility = {
					isChatWindowVisible = isChatWindowVisible,
					isChatInputBarVisible = isChatInputBarVisible,
				},
			}
		end

		rootContext.createChatMessagesInitialState = function(messages)
			return {
				ChatMessages = {
					byMessageId = messages,
				},
			}
		end
	end)

	it("SHOULD mount AppContainer properly", function(c)
		local mountResult = c.mount({}, c)
		expect(mountResult.instance).never.toBeNil()
		mountResult.unmount()
	end)

	describe("WHEN mounted", function()
		it("SHOULD render Chat Window and Chat Input Bar on default", function(c)
			local mountResult = c.mount({}, c)
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatWindow" })).never.toBeNil()
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatInputBar" })).never.toBeNil()
			mountResult.unmount()
		end)

		it("SHOULD render Chat Window and Chat Input Bar depending on initial state", function(c)
			-- When state = { ChatVisibility = { isChatWindowVisible = false, isChatInputBarVisible = false} },
			-- then chatWindow and chatInputBar should not be rendered

			local initialState = c.createChatVisibilityInitialState(false, false)
			local mountResult = c.mount(initialState, c)
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatWindow" })).toBeNil()
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatInputBar" })).toBeNil()

			-- When state = { ChatVisibility = { isChatWindowVisible = true, isChatInputBarVisible = false} },
			-- then chatWindow should and chatInputBar should not be rendered
			initialState = c.createChatVisibilityInitialState(true, false)
			mountResult = c.mount(initialState, c)
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatWindow" })).never.toBeNil()
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatInputBar" })).toBeNil()

			-- When state = { ChatVisibility = { isChatWindowVisible = false, isChatInputBarVisible = true} },
			-- then chatWindow should not and chatInputBar should be rendered
			initialState = c.createChatVisibilityInitialState(false, true)
			mountResult = c.mount(initialState, c)
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatWindow" })).toBeNil()
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatInputBar" })).never.toBeNil()
			mountResult.unmount()
		end)

		it("SHOULD render chat messages depending on initial state", function(c)
			local messages = {
				{
					PrefixText = "prefixText",
					Text = "text",
				},
			}
			local initialState = c.createChatMessagesInitialState(messages)
			local mountResult = c.mount(initialState, c)
			expect(c.findFirstInstance(mountResult.instance, { Name = "message1" }))
		end)
	end)

	it(
		"SHOULD toggle ChatVisibility and rendering of chatWindow and chatInputBar when ChatTopBarButtonActivated action is dispatched",
		function(c)
			local mountResult = c.mount({}, c)
			local store = mountResult.store
			expect(store:getState().ChatVisibility).toEqual({
				isChatWindowVisible = true,
				isChatInputBarVisible = true,
			})
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatWindow" })).never.toBeNil()
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatInputBar" })).never.toBeNil()

			store:dispatch(ChatTopBarButtonActivated(false))
			expect(store:getState().ChatVisibility).toEqual({
				isChatWindowVisible = false,
				isChatInputBarVisible = false,
			})
			wait()
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatWindow" })).toBeNil()
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatInputBar" })).toBeNil()

			store:dispatch(ChatTopBarButtonActivated(true))
			expect(store:getState().ChatVisibility).toEqual({
				isChatWindowVisible = true,
				isChatInputBarVisible = true,
			})
			wait()
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatWindow" })).never.toBeNil()
			expect(c.findFirstInstance(mountResult.instance, { Name = "chatInputBar" })).never.toBeNil()
		end
	)

	it("SHOULD render chatWindow and chatInputBar based on TextChatServiceChatWindowPropertyChanged action", function(c)
		local mountResult = c.mount({}, c)
		local store = mountResult.store
		expect(store:getState().ChatVisibility).toEqual({
			isChatWindowVisible = true,
			isChatInputBarVisible = true,
		})
		expect(c.findFirstInstance(mountResult.instance, { Name = "chatWindow" })).never.toBeNil()
		expect(c.findFirstInstance(mountResult.instance, { Name = "chatInputBar" })).never.toBeNil()

		store:dispatch(TextChatServiceChatWindowPropertyChanged(false))
		expect(store:getState().ChatVisibility).toEqual({
			isChatWindowVisible = false,
			isChatInputBarVisible = false,
		})
		wait()
		expect(c.findFirstInstance(mountResult.instance, { Name = "chatWindow" })).toBeNil()
		expect(c.findFirstInstance(mountResult.instance, { Name = "chatInputBar" })).toBeNil()

		store:dispatch(TextChatServiceChatWindowPropertyChanged(true))
		expect(store:getState().ChatVisibility).toEqual({
			isChatWindowVisible = true,
			isChatInputBarVisible = true,
		})
		wait()
		expect(c.findFirstInstance(mountResult.instance, { Name = "chatWindow" })).never.toBeNil()
		expect(c.findFirstInstance(mountResult.instance, { Name = "chatInputBar" })).never.toBeNil()
	end)

	it("SHOULD render chat messages when SendChatMessage is dispatched", function(c)
		local mountResult = c.mount({}, c)
		local store = mountResult.store

		store:dispatch(SendChatMessage("RBXGeneral", "mockMessageId", "prefixText", "text"))
		expect(store:getState().ChatMessages.byMessageId).toEqual({
			mockMessageId = {
				PrefixText = "prefixText",
				Text = "text",
			},
		})
		wait()
		expect(c.findFirstInstance(mountResult.instance, { Name = "message1" })).never.toBeNil()
	end)

	it("SHOULD reset chat messages fading SendChatMessage is dispatched", function(c)
		c.textTimer = Timer.new(0)
		local mountResult = c.mount({}, c, function()
			return {
				textTimer = c.textTimer,
			}
		end)
		local store = mountResult.store

		store:dispatch(SendChatMessage("RBXGeneral", "mockMessageId1", "prefixText", "text"))
		wait()
		local message = c.findFirstInstance(mountResult.instance, { Name = "message1" })
		expect(message.TextTransparency).toBeCloseTo(0)
		expect(message.TextStrokeTransparency).toBeCloseTo(0.5)

		-- After the timer ends, the message should fade out over ~0.8s
		wait(1)
		expect(message.TextTransparency).toBeCloseTo(1)
		expect(message.TextStrokeTransparency).toBeCloseTo(1)

		-- When user receives new message, messages should fade in immediately despite inactivity
		store:dispatch(SendChatMessage("RBXGeneral", "mockMessageId2", "prefixText", "text"))
		wait()
		expect(message.TextTransparency).toBeCloseTo(0)
		expect(message.TextStrokeTransparency).toBeCloseTo(0.5)
	end)

	it("SHOULD scroll down to the most recent message automatically when user does not scroll", function(c)
		local mountResult = c.mount({}, c)
		local store = mountResult.store
		local scrollingFrame = c.findFirstInstance(mountResult.instance, { ClassName = "ScrollingFrame" })
		expect(scrollingFrame).never.toBeNil()

		for i = 1, 20 do
			local mockMessageId = "mockMessageId" .. tostring(i)
			store:dispatch(SendChatMessage("RBXGeneral", mockMessageId, "prefixText", "text"))
		end

		wait()
		expect(scrollingFrame).never.toHaveProperty("CanvasPosition.Y", 0)
	end)
end
