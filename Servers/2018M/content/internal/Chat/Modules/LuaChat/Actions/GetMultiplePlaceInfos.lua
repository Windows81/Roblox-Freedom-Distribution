local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local LuaChat = Modules.LuaChat

local WebApi = require(LuaChat.WebApi)
local PlaceInfoModel = require(LuaChat.Models.PlaceInfoModel)

local RequestMultiplePlaceInfos = require(LuaChat.Actions.RequestMultiplePlaceInfos)
local FailedToFetchMultiplePlaceInfos = require(LuaChat.Actions.FailedToFetchMultiplePlaceInfos)
local ReceivedMultiplePlaceInfos = require(LuaChat.Actions.ReceivedMultiplePlaceInfos)

return function(placeIdList)
	return function(store)
		local state = store:getState()
		local placesToFetch = {}

		if state.ChatAppReducer.PlaceInfos then
			for _, placeId in pairs(placeIdList) do
				if not state.ChatAppReducer.PlaceInfosAsync[placeId] then
					table.insert(placesToFetch, placeId)
				end
			end
			if #placesToFetch == 0 then
				return
			end
		end

		store:dispatch(RequestMultiplePlaceInfos(placesToFetch))

		spawn(function()
			local status, result = WebApi.GetMultiplePlaceInfos(placesToFetch)

			if status ~= WebApi.Status.OK then
				warn("WebApi failure in GetMultiplePlaceInfos")
				store:dispatch(FailedToFetchMultiplePlaceInfos(placesToFetch))
				return
			end

			local placeInfos = {}
			for _, placeInfoData in pairs(result) do
				table.insert(placeInfos, PlaceInfoModel.fromWeb(placeInfoData))
			end
			store:dispatch(ReceivedMultiplePlaceInfos(placeInfos))
		end)
	end
end
