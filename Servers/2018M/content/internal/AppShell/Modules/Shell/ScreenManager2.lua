--[[
	This manager class allows the current screens to work with Roact screens
	using the new screen list that is implemented in Rodux. This allows
	certain screen lifecycle events to be respected when crossing the boundaries
	of the two systems.

	For example, when the controller lost overlay pops up, this allows both
	a Roact screen and a current screen to correctly take focus when
	the overlay is dismissed.

	This will only be used by the older screen system. It will keep the API
	compatable with the current ScreenManager
]]
local Analytics = require(script.Parent.Analytics)
local AppState = require(script.Parent.AppState)
local GlobalSettings = require(script.Parent.GlobalSettings)
local ScreenItem = require(script.Parent.Models.ScreenItem)

local InsertScreen = require(script.Parent.Actions.InsertScreen)
local RemoveScreen = require(script.Parent.Actions.RemoveScreen)

local ScreenManager = {}

local ScreenMap = {}

local function setRBXEventStream_Screen(screen, status)
	if screen and type(screen.GetAnalyticsInfo) == "function" then
		local screenAnalyticsInfo = screen:GetAnalyticsInfo()
		if type(screenAnalyticsInfo) == "table" and screenAnalyticsInfo[Analytics.WidgetNames('WidgetId')] then
			screenAnalyticsInfo.Status = status
			Analytics.SetRBXEventStream("Widget",  screenAnalyticsInfo)
		end
	end
end

local function getScreenPriority(screen)
	local priority = GlobalSettings.DefaultPriority
	if screen.GetPriority ~= nil then
		priority = screen:GetPriority()
	end

	return priority
end

function ScreenManager:ContainsScreen(desiredScreen)
	for _,item in pairs(ScreenMap) do
		if item.screen == desiredScreen then
			return true
		end
	end

	return false
end

function ScreenManager:GetTopScreen()
	local screenList = AppState.store:getState().ScreenList
	if screenList and #screenList > 0 then
		local frontScreen = screenList[1]
		return ScreenMap[frontScreen.id].screen
	end

	return nil
end

function ScreenManager:OpenScreen(screen, hidePrevious)
	if hidePrevious == nil then
		hidePrevious = true
	end

	local data = {
		hidePrevious = hidePrevious,
	}

	local id = tostring(screen)
	ScreenMap[id] = {
		screen = screen,
		isShown = false,
	}

	local screenItem = ScreenItem.new(id, getScreenPriority(screen), data)
	AppState.store:dispatch(InsertScreen(screenItem))
end

function ScreenManager:CloseCurrent()
	local screenList = AppState.store:getState().ScreenList
	local frontScreen = #screenList > 0 and screenList[1]

	if not frontScreen or not ScreenMap[frontScreen.id] then
		return
	end

	AppState.store:dispatch(RemoveScreen(frontScreen))
end

local function handleScreensRemoved(screenList)
	local currentListToMap = {}
	for _, item in ipairs(screenList) do
		currentListToMap[item.id] = true
	end

	local idsToRemove = {}
	for id,_ in pairs(ScreenMap) do
		if not currentListToMap[id] then
			table.insert(idsToRemove, id)
		end
	end

	for _, id in ipairs(idsToRemove) do
		local screenItem = ScreenMap[id]
		if screenItem then
			local screen = screenItem.screen

			screen:RemoveFocus()
			screen:Hide()

			if screen.ScreenRemoved then
				screen:ScreenRemoved()
			end

			setRBXEventStream_Screen(screen, "Close")
		end

		ScreenMap[id] = nil
	end
end

local function handleScreensAdded(screenList)
	for i = #screenList, 1, -1 do
		local screenListItem = screenList[i]

		local screenMapItem = ScreenMap[screenListItem.id]
		if screenMapItem then
			local screen = screenMapItem.screen
			if i > 1 then
				local doHide = true
				local prevListItem = screenList[i - 1]
				if prevListItem and prevListItem.data then
					doHide = prevListItem.data.hidePrevious
				end

				screen:RemoveFocus()
				if doHide then
					screen:Hide()
					screenMapItem.isShown = false
				end

				if not screenMapItem.isShown and not doHide then
					screen:Show()
					screenMapItem.isShown = true
				end
			else
				if not screenMapItem.isShown then
					screen:Show()
					screenMapItem.isShown = true
					setRBXEventStream_Screen(screen, "Show")
				end
				screen:Focus()
				setRBXEventStream_Screen(screen, "Focus")
			end
		end
	end
end

local function update(screenList)
	handleScreensRemoved(screenList)
	handleScreensAdded(screenList)
end

AppState.store.changed:connect(function(newState, oldState)
	local currentScreenList = newState.ScreenList
	local previousScreenList = oldState.ScreenList

	if currentScreenList == previousScreenList then
		return
	end

	update(currentScreenList)
end)

return ScreenManager
