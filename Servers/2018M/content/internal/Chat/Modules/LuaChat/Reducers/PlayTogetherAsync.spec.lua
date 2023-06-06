local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat
local Actions = LuaChat.Actions

local MockId = require(LuaApp.MockId)

local PlayTogetherAsync = require(script.Parent.PlayTogetherAsync)

local FailedToFetchMostRecentlyPlayedGames = require(Actions.FailedToFetchMostRecentlyPlayedGames)
local FetchedMostRecentlyPlayedGames = require(Actions.FetchedMostRecentlyPlayedGames)
local FetchingMostRecentlyPlayedGames = require(Actions.FetchingMostRecentlyPlayedGames)
local GameFailedToPin = require(Actions.GameFailedToPin)
local GameFailedToUnpin = require(Actions.GameFailedToUnpin)
local PinnedGame = require(Actions.PinnedGame)
local PinningGame = require(Actions.PinningGame)
local UnpinnedGame = require(Actions.UnpinnedGame)
local UnpinningGame = require(Actions.UnpinningGame)

return function()

    describe("initial state", function()
        it("should return an initial table when passed nil", function()
            local state = PlayTogetherAsync(nil, {})
            expect(state).to.be.a("table")
            expect(state.pinningGames).to.be.a("table")
            expect(state.unPinningGames).to.be.a("table")
        end)
    end)

    describe("PinningGame", function()
        it("should set the pinning game async state to true", function()
            local state = PlayTogetherAsync(nil, {})
            local testConversationId = MockId()
            state = PlayTogetherAsync(state, PinningGame(testConversationId))

            expect(state.pinningGames[testConversationId]).to.equal(true)
        end)
    end)

    describe("PinnedGame", function()
        it("should set the pinning game async state to false", function()
            local state = PlayTogetherAsync(nil, {})
            local testConversationId = MockId()
            state = PlayTogetherAsync(state, PinnedGame(testConversationId))

            expect(state.pinningGames[testConversationId]).to.equal(false)
        end)
    end)

    describe("GameFailedToPin", function()
        it("should set the pinning game async state to false", function()
            local state = PlayTogetherAsync(nil, {})
            local testConversationId = MockId()
            state = PlayTogetherAsync(state, GameFailedToPin(testConversationId))

            expect(state.pinningGames[testConversationId]).to.equal(false)
        end)
    end)

    describe("UnpinningGame", function()
        it("should set the unpinning game async state to true", function()
            local state = PlayTogetherAsync(nil, {})
            local testConversationId = MockId()
            state = PlayTogetherAsync(state, UnpinningGame(testConversationId))

            expect(state.unPinningGames[testConversationId]).to.equal(true)
        end)
    end)

    describe("UnpinnedGame", function()
        it("should set the unpinning game async state to false", function()
            local state = PlayTogetherAsync(nil, {})
            local testConversationId = MockId()
            state = PlayTogetherAsync(state, UnpinnedGame(testConversationId))

            expect(state.unPinningGames[testConversationId]).to.equal(false)
        end)
    end)

    describe("GameFailedToUnpin", function()
        it("should set the unpinning game async state to false", function()
            local state = PlayTogetherAsync(nil, {})
            local testConversationId = MockId()
            state = PlayTogetherAsync(state, GameFailedToUnpin(testConversationId))

            expect(state.unPinningGames[testConversationId]).to.equal(false)
        end)
    end)
    describe("FetchingMostRecentlyPlayedGames", function()
        it("should update fecth state of most recently played games", function()
            local state = PlayTogetherAsync(nil, {})
            state = PlayTogetherAsync(state, FetchingMostRecentlyPlayedGames())

            expect(state.fetchingMostRecentlyPlayedGames).to.equal(true)
            expect(state.fetchedMostRecentlyPlayedGames).to.equal(false)
        end)
    end)
    describe("FetchedMostRecentlyPlayedGames", function()
        it("should update fecth state of most recently played games", function()
            local state = PlayTogetherAsync(nil, {})
            state = PlayTogetherAsync(state, FetchedMostRecentlyPlayedGames())

            expect(state.fetchingMostRecentlyPlayedGames).to.equal(false)
            expect(state.fetchedMostRecentlyPlayedGames).to.equal(true)
        end)
    end)
    describe("FailedToFetchMostRecentlyPlayedGames", function()
        it("should update fecth state of most recently played games", function()
            local state = PlayTogetherAsync(nil, {})
            state = PlayTogetherAsync(state, FailedToFetchMostRecentlyPlayedGames())

            expect(state.fetchingMostRecentlyPlayedGames).to.equal(false)
            expect(state.fetchedMostRecentlyPlayedGames).to.equal(false)
        end)
    end)
end