local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local Create = require(LuaChat.Create)
local getInputEvent = require(LuaChat.Utils.getInputEvent)
local GetMultiplePlaceInfos = require(LuaChat.Actions.GetMultiplePlaceInfos)
local GetPlaceThumbnail = require(LuaChat.Actions.GetPlaceThumbnail)
local Signal = require(Modules.Common.Signal)
local SortedActivelyPlayedGames = require(LuaChat.SortedActivelyPlayedGames)
local User = require(LuaApp.Models.User)

local ICON_MASK = "rbxasset://textures/ui/LuaChat/graphic/gr-mask-game-icon-48x48.png"
local STACKED_ICON_MASK = "rbxasset://textures/ui/LuaChat/graphic/gr-gamealbum-icon-52x52.png"
local BORDER_ICON_MASK = "rbxasset://textures/ui/LuaChat/graphic/gr-game-border-24x24.png"
local DEFAULT_THUMBNAIL = "rbxasset://textures/ui/LuaChat/icons/share-game-thumbnail.png"

local LARGE_GAME_ICON_OUTER_SIZE = UDim2.new(0, 48, 0, 48)
local LARGE_GAME_STACK_ICON_SIZE = UDim2.new(0, 52, 0, 52)

local SMALL_GAME_ICON_OUTER_SIZE = UDim2.new(0, 40, 0, 40)
local SMALL_GAME_ICON_CHILD_SIZE = UDim2.new(0, 24, 0, 24)

local PLACE_INFO_THUMBNAIL_SIZE = 48

local UrlSupportNewGamesAPI = settings():GetFFlag("UrlSupportNewGamesAPI")

local PlayTogetherGameIcon = {}
PlayTogetherGameIcon.__index = PlayTogetherGameIcon

PlayTogetherGameIcon.Size = {
    SMALL = "SMALL",
    LARGE = "LARGE",
}

PlayTogetherGameIcon.Type = {
    DEFAULT = "DEFAULT",
    ACTIVE = "ACTIVE"
}

function PlayTogetherGameIcon.new(appState, conversation, iconSize, iconType)
    local self = {
        appState = appState,
    }
    self.cachedConversation = nil
    self.cachedThumbnailPlaceInfo = nil
    self.conversationId = nil
    self.conversationUsers = {}
    self.fetchedMostRecentlyPlayedGames = false
    self.setIconPending = false
    self.type = iconType or PlayTogetherGameIcon.Type.DEFAULT
    self.updateConnection = nil

    local childImage = BORDER_ICON_MASK
    local childSize = SMALL_GAME_ICON_CHILD_SIZE
    local size = SMALL_GAME_ICON_CHILD_SIZE
    local outerSize = SMALL_GAME_ICON_OUTER_SIZE
    if iconSize == PlayTogetherGameIcon.Size.LARGE then
        childImage = ICON_MASK
        childSize = LARGE_GAME_STACK_ICON_SIZE
        size = LARGE_GAME_ICON_OUTER_SIZE
        outerSize = LARGE_GAME_ICON_OUTER_SIZE
    end

    self.rbx = Create.new "Frame" {
        Name = "Frame",
        BackgroundTransparency = 1,
        Size = outerSize,

        Create.new "ImageButton" {
            Name = "TopGameIcon",
            AnchorPoint = Vector2.new(0.5, 0.5),
            BackgroundTransparency = 1,
            Image = DEFAULT_THUMBNAIL,
            Position = UDim2.new(0.5, 0, 0.5, 0),
            Size = size,

            Create.new "ImageLabel" {
                Name = "Mask",
                AnchorPoint = Vector2.new(0.5, 0.5),
                BackgroundTransparency = 1,
                Image = childImage,
                Position = UDim2.new(0.5, 0, 0.5, 0),
                Size = childSize,
            }
        }
    }

    self.iconSize = iconSize
    self.mask = self.rbx.TopGameIcon.Mask

    setmetatable(self, PlayTogetherGameIcon)

    self:SetVisible(false)

    if conversation ~= nil then
        self.conversationId = conversation.id
        self.cachedConversation = conversation
        self:Update(conversation)

        self.updateConnection = appState.store.Changed:Connect(function(state, oldState)
            -- Update if there's a change in which conversation we're viewing:
            local newConversation = state.ChatAppReducer.Conversations[self.conversationId]

            -- Note conversations can be nil if we're a dummy 1:1 conversation
            -- which was removed and replaced by a server conversation:
            if newConversation == nil then
                return
            end

            if self.cachedConversation ~= newConversation then
                self.cachedConversation = newConversation
                self:Update(self.cachedConversation)
                return
            end

            -- Update if there's any change in our conversation participants:
            local users = state.Users
            local participantsCache = self.cachedConversation.participants
            for _, id in ipairs(conversation.participants) do
                if participantsCache[id] ~= users[id] then
                    self:Update(self.cachedConversation)
                    return
                end
            end

            -- Update if we were waiting for our icon to load:
            if self.setIconPending then
                self:Update(self.cachedConversation)
                return
            end
        end)
    end

    self.Pressed = Signal.new()
    getInputEvent(self.rbx.TopGameIcon):Connect(function()
        self.Pressed:Fire()
    end)

    return self
end

function PlayTogetherGameIcon:Update(conversation)
    if not UrlSupportNewGamesAPI then
        self.rbx.TopGameIcon.Image = DEFAULT_THUMBNAIL
        return
    end

    local state = self.appState.store:getState()

    local pinnedGameRootPlaceId = nil
    if conversation.pinnedGame and conversation.pinnedGame.rootPlaceId then
        pinnedGameRootPlaceId = conversation.pinnedGame.rootPlaceId
    end

    local inGameParticipants = {}
    local mostRecentPlayedPlayableGamePlaceId =
        self.appState.store:getState().ChatAppReducer.MostRecentlyPlayedGames.playableGamePlaceId

    for _, userId in pairs(conversation.participants) do
        local user = state.Users[userId]
        if user ~= nil then
            if (user.presence == User.PresenceType.IN_GAME) and user.placeId then
                table.insert(inGameParticipants, user)
            end
        end
    end

    if self.type == PlayTogetherGameIcon.Type.ACTIVE then
        if #inGameParticipants > 0 then
            local activelyPlayedGames = SortedActivelyPlayedGames.getSortedGames(pinnedGameRootPlaceId,
                inGameParticipants)
            local isMultiple = #activelyPlayedGames > 1
            self:SetThumbnail(state, activelyPlayedGames[1].placeId, isMultiple)
        else
            self:SetVisible(false)
        end
    else
        if #inGameParticipants > 0 then
            local activelyPlayedGames = SortedActivelyPlayedGames.getSortedGames(pinnedGameRootPlaceId,
                inGameParticipants)
            self:SetThumbnail(state, activelyPlayedGames[1].placeId, false)
        elseif pinnedGameRootPlaceId then
            self:SetThumbnail(state, pinnedGameRootPlaceId, false)
        elseif mostRecentPlayedPlayableGamePlaceId then
            self:SetThumbnail(state, mostRecentPlayedPlayableGamePlaceId, false)
        else
            self:SetVisible(false)
        end
    end
end

function PlayTogetherGameIcon:SetThumbnail(state, chosenPlaceId, isMultiple)
    local placeInfo = state.ChatAppReducer.PlaceInfos[chosenPlaceId]
    self:SetVisible(true)
    if placeInfo == nil then
        self.appState.store:dispatch(GetMultiplePlaceInfos({chosenPlaceId}))
        self.setIconPending = true
    else
        self.cachedThumbnailPlaceInfo = placeInfo
        local thumbnail = state.ChatAppReducer.PlaceThumbnails[placeInfo.imageToken]
        if thumbnail == nil then
            self.appState.store:dispatch(GetPlaceThumbnail(
                placeInfo.imageToken, PLACE_INFO_THUMBNAIL_SIZE, PLACE_INFO_THUMBNAIL_SIZE
            ))
            self.setIconPending = true
        else
            self:SetIsMultipleGames(isMultiple)
            self.setIconPending = false
            if thumbnail.image ~= '' then
                self.rbx.TopGameIcon.Image = thumbnail.image
            else
                self.rbx.TopGameIcon.Image = DEFAULT_THUMBNAIL
            end
        end
    end
end

function PlayTogetherGameIcon:SetVisible(value)
    self.rbx.Visible = value
end

function PlayTogetherGameIcon:SetIsMultipleGames(isMultiple)
    if self.iconSize == PlayTogetherGameIcon.Size.SMALL then
        return
    end

    if isMultiple then
        self.mask.Image = STACKED_ICON_MASK
        self.mask.Size = LARGE_GAME_STACK_ICON_SIZE
    else
        self.mask.Image = ICON_MASK
        self.mask.Size = LARGE_GAME_ICON_OUTER_SIZE
    end
end

function PlayTogetherGameIcon:Destruct()
    if self.updateConnection then
        self.updateConnection:Disconnect()
    end

    self.rbx:Destroy()
end

return PlayTogetherGameIcon
