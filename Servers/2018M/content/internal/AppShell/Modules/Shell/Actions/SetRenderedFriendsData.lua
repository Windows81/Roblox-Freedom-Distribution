local CoreGui = game:GetService("CoreGui")
local Action = require(CoreGui.RobloxGui.Modules.Common.Action)
--[[
	// friendsData is table
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

return Action("SetRenderedFriendsData", function(friendsData)
	return {
		data = friendsData
	}
end)