local Modules = game:GetService("CoreGui").RobloxGui.Modules

local DeviceOrientation = require(Modules.LuaApp.Reducers.DeviceOrientation)
local TopBar = require(Modules.LuaApp.Reducers.TopBar)
local TabBarVisible = require(Modules.LuaApp.Reducers.TabBarVisible)

local Games = require(Modules.LuaApp.Reducers.Games)
local GameSorts = require(Modules.LuaApp.Reducers.GameSorts)
local GameSortGroups = require(Modules.LuaApp.Reducers.GameSortGroups)
local GameThumbnails = require(Modules.LuaApp.Reducers.GameThumbnails)
local NextTokenRefreshTime = require(Modules.LuaApp.Reducers.NextTokenRefreshTime)
local GameSortsContents = require(Modules.LuaApp.Reducers.GameSortsContents)
local PlaceIdsToUniverseIds = require(Modules.LuaApp.Reducers.PlaceIdsToUniverseIds)
local LocalUserId = require(Modules.LuaApp.Reducers.LocalUserId)
local Users = require(Modules.LuaApp.Reducers.Users)
local UsersAsync = require(Modules.LuaChat.Reducers.UsersAsync)
local UserStatuses = require(Modules.LuaApp.Reducers.UserStatuses)
local Navigation = require(Modules.LuaApp.Reducers.Navigation)
local Search = require(Modules.LuaApp.Reducers.Search)
local Startup = require(Modules.LuaApp.Reducers.Startup)
local NotificationBadgeCounts = require(Modules.LuaApp.Reducers.NotificationBadgeCounts)
local RequestsStatus = require(Modules.LuaApp.Reducers.RequestsStatus)
local ScreenSize = require(Modules.LuaApp.Reducers.ScreenSize)
local FormFactor = require(Modules.LuaApp.Reducers.FormFactor)
local Platform = require(Modules.LuaApp.Reducers.Platform)

local FriendCount = require(Modules.LuaChat.Reducers.FriendCount)
local ConnectionState = require(Modules.LuaChat.Reducers.ConnectionState)

local ChatAppReducer = require(Modules.LuaChat.AppReducer)

return function(state, action)
	state = state or {}

	return {
		DeviceOrientation = DeviceOrientation(state.DeviceOrientation, action),
		TopBar = TopBar(state.TopBar, action),
		TabBarVisible = TabBarVisible(state.TabBarVisible, action),

		-- Users
		Users = Users(state.Users, action),
		UsersAsync = UsersAsync(state.UsersAsync, action),
		UserStatuses = UserStatuses(state.UserStatuses, action),
		LocalUserId = LocalUserId(state.LocalUserId, action),

		-- Game Data
		Games = Games(state.Games, action),
		GameSorts = GameSorts(state.GameSorts, action),
		GameSortGroups = GameSortGroups(state.GameSortGroups, action),
		GameThumbnails = GameThumbnails(state.GameThumbnails, action),
		NextTokenRefreshTime = NextTokenRefreshTime(state.NextTokenRefreshTime, action),
		GameSortsContents = GameSortsContents(state.GameSortsContents, action),
		PlaceIdsToUniverseIds = PlaceIdsToUniverseIds(state.PlaceIdsToUniverseIds, action),

		RequestsStatus = RequestsStatus(state.RequestsStatus, action),

		Navigation = Navigation(state.Navigation, action),

		Search = Search(state.Search, action),

		FriendCount = FriendCount(state.FriendCount, action),
		ConnectionState = ConnectionState(state.ConnectionState, action),

		ScreenSize = ScreenSize(state.ScreenSize, action),
		FormFactor = FormFactor(state.FormFactor, action),
		Platform = Platform(state.Platform, action),

		ChatAppReducer = ChatAppReducer(state.ChatAppReducer, action),

		Startup = Startup(state.Startup, action),
		NotificationBadgeCounts = NotificationBadgeCounts(state.NotificationBadgeCounts, action),
	}
end