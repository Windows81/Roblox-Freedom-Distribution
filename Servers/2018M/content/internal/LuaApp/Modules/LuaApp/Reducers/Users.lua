local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Immutable = require(Modules.Common.Immutable)

local AddUser = require(Modules.LuaApp.Actions.AddUser)
local AddUsers = require(Modules.LuaApp.Actions.AddUsers)
local SetUserIsFriend = require(Modules.LuaApp.Actions.SetUserIsFriend)
local SetUserPresence = require(Modules.LuaApp.Actions.SetUserPresence)
local SetUserThumbnail = require(Modules.LuaApp.Actions.SetUserThumbnail)
local SetUserMembershipType = require(Modules.LuaApp.Actions.SetUserMembershipType)
local RemoveUser = require(Modules.LuaApp.Actions.RemoveUser)
local ReceivedUserPresence = require(Modules.LuaChat.Actions.ReceivedUserPresence)

local FFlagFixUsersReducerDataLoss = settings():GetFFlag("FixUsersReducerDataLoss")

return function(state, action)
	state = state or {}

	if action.type == AddUser.name then
		local user = action.user
		state = Immutable.Set(state, user.id, user)
	elseif action.type == AddUsers.name then
		if FFlagFixUsersReducerDataLoss then
			local addedUsers = action.users
			local usersUpdate = {}
			for userId, addedUser in pairs(addedUsers) do
				local existingUser = state[userId]
				if existingUser then
					usersUpdate[userId] = Immutable.JoinDictionaries(existingUser, addedUser)
				else
					usersUpdate[userId] = addedUser
				end
			end

			state = Immutable.JoinDictionaries(state, usersUpdate)
		else
			local users = action.users
			state = Immutable.JoinDictionaries(state, users)
		end

	elseif action.type == SetUserIsFriend.name then
		local user = state[action.userId]
		if user then
			local newUser = Immutable.Set(user, "isFriend", action.isFriend)
			state = Immutable.Set(state, user.id, newUser)
		else
			warn("Setting isFriend on user", action.userId, "who doesn't exist yet")
		end
	elseif action.type == SetUserPresence.name then
		local user = state[action.userId]
		if user then
			local newUser = Immutable.JoinDictionaries(user, {
				presence = action.presence,
				lastLocation = action.lastLocation,
			})
			state = Immutable.Set(state, user.id, newUser)
		else
			warn("Setting presence on user", action.userId, "who doesn't exist yet")
		end
	elseif action.type == ReceivedUserPresence.name then
		local user = state[action.userId]
		if user then
			state = Immutable.JoinDictionaries(state, {
				[action.userId] = Immutable.JoinDictionaries(user, {
					presence = action.presence,
					lastLocation = action.lastLocation,
					placeId = action.placeId,
				}),
			})
		end
	elseif action.type == SetUserThumbnail.name then
		local user = state[action.userId]
		if user then
			if FFlagFixUsersReducerDataLoss then
				local thumbnails = user.thumbnails or {}
				state = Immutable.JoinDictionaries(state, {
					[action.userId] = Immutable.JoinDictionaries(user, {
						thumbnails = Immutable.JoinDictionaries(thumbnails, {
							[action.thumbnailType] = Immutable.JoinDictionaries(thumbnails[action.thumbnailType] or {}, {
								[action.thumbnailSize] = action.image,
							}),
						}),
					}),
				})
			else
				state = Immutable.JoinDictionaries(state, {
					[action.userId] = Immutable.JoinDictionaries(user, {
						thumbnails = Immutable.JoinDictionaries(user.thumbnails, {
							[action.thumbnailType] = Immutable.JoinDictionaries(user.thumbnails[action.thumbnailType] or {}, {
								[action.thumbnailSize] = action.image,
							}),
						}),
					}),
				})
			end
		end
	elseif action.type == SetUserMembershipType.name then
		local user = state[action.userId]
		if user then
			state = Immutable.JoinDictionaries(state, {
				[action.userId] = Immutable.JoinDictionaries(user, {
					membership = action.membershipType,
				}),
			})
		end
	elseif action.type == RemoveUser.name then
		if state[action.userId] then
			state = Immutable.RemoveFromDictionary(state, action.userId)
		end
	end

	return state
end