-- main AppShell reducer
local Reducers = script.Parent
local RobloxUser = require(Reducers.RobloxUser)
local ScreenList = require(Reducers.ScreenList)
local XboxUser = require(Reducers.XboxUser)
local UserThumbnails = require(Reducers.UserThumbnails)
local Friends = require(Reducers.Friends)
local RenderedFriends = require(Reducers.RenderedFriends)

return function(state, action)
	state = state or {}

	return {
		-- Use reducer composition to add reducers here
		RobloxUser = RobloxUser(state.RobloxUser, action),
		ScreenList = ScreenList(state.ScreenList, action),
		XboxUser = XboxUser(state.XboxUser, action),
		UserThumbnails = UserThumbnails(state.UserThumbnails, action),
		Friends = Friends(state.Friends, action),
		RenderedFriends = RenderedFriends(state.RenderedFriends, action),
	}
end
