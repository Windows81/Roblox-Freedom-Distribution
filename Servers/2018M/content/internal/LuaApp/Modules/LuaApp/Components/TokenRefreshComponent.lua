--[[
	A component refreshes sort tokens so that they are up-to-date.
	Props:
	- sortToRefresh : target sort that needs token refresh
]]
local RunService = game:GetService("RunService")
local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local ApiFetchSortTokens = require(Modules.LuaApp.Thunks.ApiFetchSortTokens)
local RetrievalStatus = require(Modules.LuaApp.Enum.RetrievalStatus)
local ExternalEventConnection = require(Modules.Common.RoactUtilities.ExternalEventConnection)
local RoactNetworking = require(Modules.LuaApp.Services.RoactNetworking)
local RoactServices = require(Modules.LuaApp.RoactServices)

local TokenRefreshComponent = Roact.PureComponent:extend("TokenRefreshComponent")

function TokenRefreshComponent:init()
	self.steppedCallback = function()
		local sortToRefresh = self.props.sortToRefresh
		local nextTokenRefreshTime = self.props.nextTokenRefreshTime[sortToRefresh]
		local fetchingStatus = self.props.GameSortTokenFetchingStatus[sortToRefresh]

		--[[ if state is RetrievalStatus.NotStarted (uninitialized)/
						 RetrievalStatus.Fetching (is fetching data)/
						 RetrievalStatus.Failed (failed),
			stop the autorefresh until they get correctly handled. ]]
		if fetchingStatus ~= RetrievalStatus.Done then
			return
		end
		local currentTime = tick()
		if currentTime > nextTokenRefreshTime then
			self.props.refresh(sortToRefresh):catch(function()
				-- Failure handler only
			end)
		end
	end
end

function TokenRefreshComponent:render()
	return Roact.createElement(ExternalEventConnection, {
		event = RunService.stepped,
		callback = self.steppedCallback,
	})
end

TokenRefreshComponent = RoactRodux.connect(function(store, props)
	local state = store:getState()

	return {
		nextTokenRefreshTime = state.NextTokenRefreshTime,
		GameSortTokenFetchingStatus = state.RequestsStatus.GameSortTokenFetchingStatus,
		refresh = function(sortToRefresh)
			return store:dispatch(ApiFetchSortTokens(props.networking, sortToRefresh))
		end,
	}
end)(TokenRefreshComponent)

return RoactServices.connect({
	networking = RoactNetworking,
})(TokenRefreshComponent)