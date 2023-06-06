--[[
	This object is designed to abstract all of the events fired by game components.
	Since game carousels, game cards, game lists, and game grids are shared across multiple contexts,
	these elements need a common reporting component.
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules

local gameDetailReferral = require(Modules.LuaApp.Analytics.Events.gameDetailReferral)
local gamesPageInteraction = require(Modules.LuaApp.Analytics.Events.gamesPageInteraction)
local RoactAnalytics = require(Modules.LuaApp.Services.RoactAnalytics)
local Constants = require(Modules.LuaApp.Constants)

local RoactAnalyticsCommonGameEvents = {}
function RoactAnalyticsCommonGameEvents.get(context, args)
	assert(type(args.createReferralCtx) == "function", "Expected createReferralCtx to be a function")
	assert(type(args.pageName) == "string", "Expected pageName to be a string")

	local analyticsImpl = RoactAnalytics.get(context)

	local createReferralCtx = args.createReferralCtx
	local pageName = args.pageName
	local pageNameSeeAll = pageName .. "SeeAll"

	local CGE = {}

	function CGE.reportSeeAll(sortName, indexOnPage)
		local sortId = Constants.LEGACY_GAME_SORT_IDS[sortName]
		if not sortId then
			sortId = Constants.LEGACY_GAME_SORT_IDS.default
		end

		local evtContext = "SeeAll"
		local actionType = "touch"
		local actionValue = tostring(sortId)
		local selectedIndex = tonumber(indexOnPage)

		gamesPageInteraction(analyticsImpl.EventStream, evtContext, actionType, actionValue, selectedIndex)
	end

	function CGE.reportFilterChange(sortName, indexOnPage)
		local sortId = Constants.LEGACY_GAME_SORT_IDS[sortName]
		if not sortId then
			sortId = Constants.LEGACY_GAME_SORT_IDS.default
		end

		local evtContext = "SFMenu"
		local actionType = "touch"
		local actionValue = tostring(sortId)
		local selectedIndex = tonumber(indexOnPage)

		gamesPageInteraction(analyticsImpl.EventStream, evtContext, actionType, actionValue, selectedIndex)
	end

	local function reportGameDetailReferral(referralPage,
		placeId,
		sortName,
		indexInSort,
		numItemsInSort,
		isAd,
		timeFilter,
		genreFilter)

		-- handle optional values
		if not timeFilter then
			timeFilter = 1
		end

		if not genreFilter then
			genreFilter = 1
		end

		-- lookup the legacy sortId based on the sortName
		local sortId = Constants.LEGACY_GAME_SORT_IDS[sortName]
		if not sortId then
			sortId = Constants.LEGACY_GAME_SORT_IDS.default
		end

		local referralContext = createReferralCtx(indexInSort, sortId, timeFilter, genreFilter)
		gameDetailReferral(analyticsImpl.EventStream, referralContext, referralPage, numItemsInSort, placeId, isAd)
	end

	function CGE.reportOpenGameDetail(placeId, sortName, indexInSort, itemsInSort, isAd, timeFilter, genreFilter)
		reportGameDetailReferral(pageName, placeId, sortName, indexInSort, itemsInSort, isAd, timeFilter, genreFilter)
	end

	function CGE.reportOpenGameDetailFromSeeAll(placeId, sortName, indexInSort, itemsInSort, isAd, timeFilter, genreFilter)
		reportGameDetailReferral(pageNameSeeAll, placeId, sortName, indexInSort, itemsInSort, isAd, timeFilter, genreFilter)
	end

	return CGE
end

return RoactAnalyticsCommonGameEvents