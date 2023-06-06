return function()
	local Modules = game:GetService("CoreGui").RobloxGui.Modules
	local AppReducer = require(Modules.LuaApp.AppReducer)

	it("has the expected fields, and only the expected fields", function()
		local state = AppReducer(nil, {})

		local expectedKeys = {
			ChatAppReducer = true,
			ConnectionState = true,
			DeviceOrientation = true,
			ScreenSize = true,
			FormFactor = true,
			FriendCount = true,
			Games = true,
			GameSortGroups = true,
			GameSorts = true,
			GameSortsContents = true,
			GameThumbnails = true,
			RequestsStatus = true,
			LocalUserId = true,
			Navigation = true,
			NextTokenRefreshTime = true,
			NotificationBadgeCounts = true,
			PlaceIdsToUniverseIds = true,
			Platform = true,
			Search = true,
			Startup = true,
			TopBar = true,
			TabBarVisible = true,
			Users = true,
			UsersAsync = true,
			UserStatuses = true,
		}

		for key in pairs(expectedKeys) do
			assert(state[key] ~= nil, string.format("Expected field %q", key))
		end

		for key in pairs(state) do
			assert(expectedKeys[key] ~= nil, string.format("Did not expect field %q", key))
		end
	end)
end