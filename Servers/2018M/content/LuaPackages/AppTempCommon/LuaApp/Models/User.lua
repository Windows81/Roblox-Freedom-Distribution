local CorePackages = game:GetService("CorePackages")
local Players = game:GetService("Players")

local MockId = require(CorePackages.AppTempCommon.LuaApp.MockId)

local FFlagFixUsersReducerDataLoss = settings():GetFFlag("FixUsersReducerDataLoss")

local User = {}

User.PresenceType = {
	OFFLINE = "OFFLINE",
	ONLINE = "ONLINE",
	IN_GAME = "IN_GAME",
	IN_STUDIO = "IN_STUDIO",
}

function User.new()
	local self = {}

	return self
end

function User.mock()
	local self = User.new()

	self.id = MockId()

	self.isFetching = false
	self.isFriend = false
	self.lastLocation = nil
	self.name = "USER NAME"
	self.placeId = nil
	self.presence = User.PresenceType.OFFLINE
	self.membership = nil
	if not FFlagFixUsersReducerDataLoss then
		self.thumbnails = {}
	end

	return self
end

function User.fromData(id, name, isFriend)
	local self = User.new()

	self.id = tostring(id)

	self.isFetching = false
	self.isFriend = isFriend
	self.lastLocation = nil
	self.name = name
	self.placeId = nil
	if FFlagFixUsersReducerDataLoss then
		self.presence = (self.id == tostring(Players.LocalPlayer.UserId)) and User.PresenceType.ONLINE or nil
	else
		self.presence = (self.id == tostring(Players.LocalPlayer.UserId)) and User.PresenceType.ONLINE or
			User.PresenceType.OFFLINE
		self.thumbnails = {}
	end

	return self
end

function User.userPresenceToText(localization, user)
	local presence = user.presence
	local lastLocation = user.lastLocation

	if not presence then
		return ''
	end

	if presence == User.PresenceType.OFFLINE then
		return localization:Format("Common.Presence.Label.Offline")
	elseif presence == User.PresenceType.ONLINE then
		return localization:Format("Common.Presence.Label.Online")
	elseif (presence == User.PresenceType.IN_GAME) or (presence == User.PresenceType.IN_STUDIO) then
		if lastLocation ~= nil then
			return lastLocation
		else
			return localization:Format("Common.Presence.Label.Online")
		end
	end
end

return User