local CoreGui = game:GetService("CoreGui")
local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")

local Modules = CoreGui.RobloxGui.Modules
local RoactRodux = require(Modules.Common.RoactRodux)
local FlagSettings = require(Modules.LuaApp.FlagSettings)

local Roact = require(Modules.Common.Roact)
local RoactServices = require(Modules.LuaApp.RoactServices)
local RoactNetworking = require(Modules.LuaApp.Services.RoactNetworking)
local isLuaAppFriendshipCreatedSignalREnabled = FlagSettings.IsLuaAppFriendshipCreatedSignalREnabled()

local SetNotificationCount = require(Modules.LuaApp.Actions.SetNotificationCount)
local SetUserIsFriend = require(Modules.LuaApp.Actions.SetUserIsFriend)
local ApiFetchUsersFriendCount = require(Modules.LuaApp.Thunks.ApiFetchUsersFriendCount)
local FriendshipCreated = require(Modules.LuaApp.Thunks.FriendshipCreated)

local BadgeEventReceiver = Roact.Component:extend("BadgeEventReceiver")

function BadgeEventReceiver:init()
	local setNotificationCount = self.props.setNotificationCount
	local setUserIsFriend = self.props.setUserIsFriend
	local apiFetchUsersFriendCount = self.props.apiFetchUsersFriendCount
	local friendshipCreated = self.props.friendshipCreated

	local networking = self.props.networking
	local robloxEventReceiver = self.props.RobloxEventReceiver

	if not isLuaAppFriendshipCreatedSignalREnabled then
		return -- Short circuit if flag is disabled
	end
	self.tokens = {
		robloxEventReceiver:observeEvent("UpdateNotificationBadge", "NotificationIcon", function(detail)
			local eventDetails = HttpService:JSONDecode(detail)
			setNotificationCount(eventDetails.badgeString)
		end),
		robloxEventReceiver:observeEvent("FriendshipNotifications", "FriendshipDestroyed", function(detail)
			local eventDetails = HttpService:JSONDecode(detail)
			local removedFriendUserId = tostring(Players.LocalPlayer.UserId) == tostring(eventDetails.EventArgs.UserId1)
				and tostring(eventDetails.EventArgs.UserId2) or tostring(eventDetails.EventArgs.UserId1)
			apiFetchUsersFriendCount(networking):andThen(
				function()
					setUserIsFriend(removedFriendUserId, false)
				end
			)
		end),
		robloxEventReceiver:observeEvent("FriendshipNotifications", "FriendshipCreated", function(detail)
			local eventDetails = HttpService:JSONDecode(detail)
			local addedFriendUserId = tostring(Players.LocalPlayer.UserId) == tostring(eventDetails.EventArgs.UserId1)
				and tostring(eventDetails.EventArgs.UserId2) or tostring(eventDetails.EventArgs.UserId1)
			friendshipCreated(networking, addedFriendUserId)
		end),
	}
end

function BadgeEventReceiver:render()
end

function BadgeEventReceiver:willUnmount()
	for _, connection in pairs(self.tokens) do
		connection:Disconnect()
	end
end

BadgeEventReceiver = RoactRodux.UNSTABLE_connect2(
	nil,
	function(dispatch)
		return {
			apiFetchUsersFriendCount = function(...)
				return dispatch(ApiFetchUsersFriendCount(...))
			end,
			friendshipCreated = function(...)
				return dispatch(FriendshipCreated(...))
			end,
			setNotificationCount = function(...)
				return dispatch(SetNotificationCount(...))
			end,
			setUserIsFriend = function(...)
				return dispatch(SetUserIsFriend(...))
			end,
		}
	end
)(BadgeEventReceiver)

BadgeEventReceiver = RoactServices.connect({
	networking = RoactNetworking,
})(BadgeEventReceiver)

return BadgeEventReceiver