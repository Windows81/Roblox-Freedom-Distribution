local Modules = game:GetService("CoreGui").RobloxGui.Modules
local SetFriendsData = require(Modules.Shell.Actions.SetFriendsData)
local Immutable = require(Modules.Common.Immutable)

--[[
	// action is table
	// Table keys:
		// [index number] - table
			// xuid - number
			// robloxName - string
			// placeId - number
			// robloxStatus - string
			// robloxuid - number
			// lastLocation - string
			// gamertag - string
			// xboxStatus - string
			// friendsSource - string
]]

return function(state, action)
	state = state or {
		initialized = false,
		data = {}
	}

	if action.type == SetFriendsData.name then
		-- Use nil in setFriendsData to reset
		if not action.data then
			return {
				initialized = false,
				data = {}
			}
		end

		-- Make a copy of new friends
		local newFriendsData = {}
		for i in ipairs(action.data) do
			local friendDataTable = Immutable.JoinDictionaries(action.data[i])
			table.insert(newFriendsData, friendDataTable)
		end

		return {
			initialized = true,
			data = newFriendsData
		}
	end

	return state
end