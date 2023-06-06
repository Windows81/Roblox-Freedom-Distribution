local Modules = game:GetService("CoreGui").RobloxGui.Modules

local RoactAnalyticsCommonGameEvents = require(Modules.LuaApp.Services.RoactAnalyticsCommonGameEvents)

local SearchPageAnalytics = {}

function SearchPageAnalytics.get(context)
	return RoactAnalyticsCommonGameEvents.get(context, {
		pageName = "gameSearch",
		createReferralCtx = function(indexInSort, sortId, timeFilter, genreFilter)
			local context = string.format("gamesort_SortFilter<%d>_TimeFilter<%d>_GenreFilter<%d>_Position<%d>",
				sortId,
				timeFilter,
				genreFilter,
				indexInSort)
			return context
		end
	})
end

return SearchPageAnalytics