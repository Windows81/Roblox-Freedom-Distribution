--[[
A scrolling frame wraps pages for pulling down to refresh
props:
currentPage -- identify if native mobile buttonclick events comes from current page
refresh -- refresh function for this page
Size -- Size of the content in the scrolling frame
BackgroundColor3
Position -- TopLeft Corner of ScrollingContent
_____________________
|					|
|		TopBar		|
|___________________|
|					|
|					|
|					|
| ScrollingContent	|
|___________________|
]]

local Modules = game:GetService("CoreGui").RobloxGui.Modules
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local HttpService = game:GetService("HttpService")

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local RoactServices = require(Modules.LuaApp.RoactServices)
local AppNotificationService = require(Modules.LuaApp.Services.AppNotificationService)
local ExternalEventConnection = require(Modules.Common.RoactUtilities.ExternalEventConnection)

local FitChildren = require(Modules.LuaApp.FitChildren)
local RoactMotion = require(Modules.LuaApp.RoactMotion)
local EndOfScroll = require(Modules.LuaApp.Components.EndOfScroll)
local LoadingBar = require(Modules.LuaApp.Components.LoadingBar)

local REFRESH_THRESHOLD = 25
local TWEEN_BACK_TIME = 0.5
local SPRING_STIFFNESS = 150
local SPRING_DAMPING = 18
local PRECISION = 2

local ROTATION_SCALE = 9.6
local ROTATION_ORIGIN = 240
local TRANSPARENCY_SCALE = 0.04
local DEFAULT_SPINNER_SIZE = 20
local CONFIRM_SCALE = 1.1
local ROTATING_SPEED = 540
local FADE_OUT_SCALE = 2
local BLUE_ARROW_PATH = "rbxasset://textures/ui/LuaApp/icons/ic-blue-arrow.png"
local GRAY_ARROW_PATH = "rbxasset://textures/ui/LuaApp/icons/ic-gray-arrow.png"

-- We would like to start loading more before user reaches the bottom.
-- The default distance from the bottom of that would be 2000.
local DEFAULT_PRELOAD_DISTANCE = 2000

local LOADING_BAR_PADDING = 20
local LOADING_BAR_HEIGHT = 16
local LOADING_BAR_TOTAL_HEIGHT = LOADING_BAR_PADDING * 2 + LOADING_BAR_HEIGHT

local function Spinner(props)
	-- should be spinning right now
	local activated = props.activated
	local offset = props.offset
	local position = props.Position
	local timer = props.timer
	local tween = props.tween

	local rotation = 0
	local scale = 1
	local image = BLUE_ARROW_PATH
	local imageTransparency = 0

	if offset > 0 then
		return
	end

	if activated then
		rotation = timer * ROTATING_SPEED
		offset = 0

	elseif tween then
		offset = 0
		imageTransparency = FADE_OUT_SCALE * timer
		image = GRAY_ARROW_PATH

	elseif offset > -REFRESH_THRESHOLD then
		offset = -offset
		rotation = ROTATION_SCALE * offset - ROTATION_ORIGIN
		imageTransparency = 1 - TRANSPARENCY_SCALE * offset
		image = GRAY_ARROW_PATH

	else
		scale = CONFIRM_SCALE
		offset = REFRESH_THRESHOLD
	end

	return Roact.createElement("ImageLabel", {
		Size = UDim2.new(0, DEFAULT_SPINNER_SIZE * scale, 0, DEFAULT_SPINNER_SIZE * scale),
		Position = position + UDim2.new(0.5, 0, 0, offset - DEFAULT_SPINNER_SIZE / 2),
		ImageTransparency = imageTransparency,
		Image = image,
		BackgroundTransparency = 1,
		Rotation = rotation,
		AnchorPoint = Vector2.new(0.5, 0.5),
	})
end

local RefreshScrollingFrame = Roact.Component:extend("RefreshScrollingFrame")

RefreshScrollingFrame.defaultProps = {
	preloadDistance = DEFAULT_PRELOAD_DISTANCE,
	createEndOfScrollElement = false,
}

function RefreshScrollingFrame:startTweenBack()

	-- refresh finishes, spinner stops spin, animate the spinner poping back
	self:setState({
		activated = false,
		tween = true,
		timer = 0,
		offset = 0,
	})
end

function RefreshScrollingFrame:startSpin()

	-- spinner hanging and spinning
	self:setState({
		activated = true,
		tween = false,
		timer = 0,
	})
end

function RefreshScrollingFrame:startTween()

	-- spinner appear with a tweened animation
	self:setState({
		activated = true,
		tween = true,
		timer = 0,
	})
end

function RefreshScrollingFrame:didMount()
	self._isMounted = true
end

function RefreshScrollingFrame:willUnmount()
	self._isMounted = false
end


function RefreshScrollingFrame:init()
	self._inputCount = 0
	self._shouldRefreshOnScroll = false
	self._isMounted = false

	self.state = {
		-- for refresh spinner:
		activated = false,
		tween = false,
		timer = 0,
		offset = 0,
		-- for loadMore:
		isLoadingMore = false
	}
	self.fitFieldCanvasSize = {
		CanvasSize = FitChildren.FitAxis.Height,
	}

	-- store ref so the [Roact.Ref] doesn't change everyupdate
	self._refCallBack = function(rbx)
		self.ref = rbx
	end

	self.scrollBack = function()
		if self.ref then
			self.ref:ScrollToTop()
		end
	end

	self.onCanvasPositionChanged = function(rbx)
		local preloadDistance = self.props.preloadDistance
		local refresh = self.props.refresh
		local onLoadMore = self.props.onLoadMore
		local isLoadingMore = self.state.isLoadingMore

		local newPosition = rbx.CanvasPosition.Y

		-- Offset is used for the refreshing spinner.
		if refresh and self._shouldRefreshOnScroll and
			newPosition < REFRESH_THRESHOLD or self.state.offset < REFRESH_THRESHOLD then
			self:setState({
				offset = newPosition,
			})
		end

		-- Check if we want to load more things
		if onLoadMore and not isLoadingMore then
			if rbx.CanvasSize.Y.Scale ~= 0 then
				warn([[RefreshScrollingFrame: Scrollingframe.CanvasSize.Y.Scale is not 0!
				Content loading would not work properly.]])
				return
			end

			local loadMoreThreshold = rbx.CanvasSize.Y.Offset - rbx.AbsoluteWindowSize.Y - preloadDistance

			if newPosition > loadMoreThreshold then
				self:setState({
					isLoadingMore = true
				})

				onLoadMore():andThen(
					-- Succeed:
					function()
						if self._isMounted then
							self:setState({
								isLoadingMore = false
							})
						end
					end,

					-- Failed:
					function()
						-- Allow us to retry.
						if self._isMounted then
							self:setState({
								isLoadingMore = false
							})
						end
					end
				)
			end
		end
	end

	self.renderSteppedCallback = function(dt)
		if self.state.activated or self.state.tween then
			local nextState = {
				timer = self.state.timer + dt,
			}
			if self.state.tween and self.state.timer > TWEEN_BACK_TIME then
				nextState.tween = false
			end
			self:setState(nextState)
		end
	end

	self.inputBeganCallback = function(input)

		-- To support desktop apps this check should be dependent on platform
		if input.UserInputType ~= Enum.UserInputType.Touch then
			return
		end
		self._shouldRefreshOnScroll = true
		self._inputCount = self._inputCount + 1
	end

	self.inputEndedCallback = function(input)
		local refresh = self.props.refresh

		if input.UserInputType ~= Enum.UserInputType.Touch then
			return
		end

		-- Count should always > 0 whenever input ended, otherwise we missed a begin here.
		if self._inputCount > 0 then
			self._inputCount = self._inputCount - 1
		end

		-- only determine refresh or not when input count drops back to 0 again (end of multi-touch)
		if self._inputCount > 0 then
			return
		end

		self._shouldRefreshOnScroll = false

		if self.state.offset < -REFRESH_THRESHOLD and not self.state.activated then
			self:startSpin()

			refresh():andThen(
				function()
					if self._isMounted then
						self:startTweenBack()
					end
				end,

				-- failure handler
				function()
					if self._isMounted then
						self:startTweenBack()
					end
				end
			)
		elseif self.state.offset < 0 then
			self._shouldRefreshOnScroll = true
		end
	end

	self.statusBarTapCallback = function()
		self.scrollBack()
	end

	-- Hooking to rbxevent is a temp solution and signals will be passed in by the new lua bottom bar
	self.bottomBarButtonPressedCallback = function(event)
		local refresh = self.props.refresh

		if self.state.activated then
			return
		end

		local currentRoute = self.props.currentRoute

		if event.namespace == "Navigations" and event.detailType == "Reload" then
			local eventDetails = HttpService:JSONDecode(event.detail)
			if eventDetails.appName == currentRoute[1].name then
				self.scrollBack()

				if refresh then
					self._shouldRefreshOnScroll = true
					self:startTween()
					refresh():andThen(
						function()
							self:startTweenBack()
						end,

						-- failure handler
						function()
							self:startTweenBack()
						end
					)
				end
			end
		end
	end
end

function RefreshScrollingFrame:render()
	local size = self.props.Size
	local backgroundColor3 = self.props.BackgroundColor3
	local targetYPadding = self.props.Position.Y.Offset
	local currentRoute = self.props.currentRoute
	local notificationService = self.props.NotificationService
	local isLoadingMore = self.state.isLoadingMore

	local refreshOnNavBar = #currentRoute == 1

	if self.state.activated then
		if self.state.offset > 0 and self.state.offset < REFRESH_THRESHOLD then
			targetYPadding = targetYPadding - self.state.offset + REFRESH_THRESHOLD
		elseif self.state.offset <= 0 then
			targetYPadding = targetYPadding + REFRESH_THRESHOLD
		end
	end

	return Roact.createElement("Frame", {
		Size = UDim2.new(1, 0, 1, 0),
		BackgroundColor3 = backgroundColor3,
	}, {
		layout = Roact.createElement("UIListLayout", {
			SortOrder = Enum.SortOrder.LayoutOrder,
			FillDirection = Enum.FillDirection.Vertical,
			VerticalAlignment = Enum.VerticalAlignment.Top,
		}),
		spinnerFrame = Roact.createElement(RoactMotion.SimpleMotion, {
			style = {
				sizeY = RoactMotion.spring(targetYPadding, SPRING_STIFFNESS, SPRING_DAMPING, PRECISION),
			},
			render = function(values)
				local spinnerPosition = self.state.tween and values.sizeY or targetYPadding
				return Roact.createElement("Frame", {
					Size = UDim2.new(1, 0, 0, values.sizeY),
					BackgroundTransparency = 1,
					LayoutOrder = 1,
				},{
					spinner = Spinner({
						Position = UDim2.new(0, 0, 0, spinnerPosition),
						offset = self.state.offset,
						activated = self.state.activated,
						timer = self.state.timer,
						tween = self.state.tween,
					})
				})
			end,
		}),
		scrollingFrame = Roact.createElement(FitChildren.FitScrollingFrame, {
			Size = size,
			ScrollBarThickness = 0,
			BorderSizePixel = 0,
			BackgroundTransparency = 1,
			LayoutOrder = 2,
			ElasticBehavior = Enum.ElasticBehavior.Always,
			ScrollingDirection = Enum.ScrollingDirection.Y,
			fitFields = self.fitFieldCanvasSize,
			[Roact.Ref] = self._refCallBack,
			[Roact.Change.CanvasPosition] = self.onCanvasPositionChanged,
		}, {
			Layout = Roact.createElement("UIListLayout", {
				FillDirection = Enum.FillDirection.Vertical,
				HorizontalAlignment = Enum.HorizontalAlignment.Center,
				SortOrder = Enum.SortOrder.LayoutOrder,
			}),
			Content = Roact.createElement(FitChildren.FitFrame, {
				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				LayoutOrder = 1,
				Size = UDim2.new(1, 0, 1, 0),
				fitFields = {
					Size = FitChildren.FitAxis.Height,
				},
			}, self.props[Roact.Children]),
			LoadingBarFrame = isLoadingMore and Roact.createElement("Frame", {
				BackgroundTransparency = 1,
				LayoutOrder = 2,
				Size = UDim2.new(1, 0, 0, LOADING_BAR_TOTAL_HEIGHT),
			}, {
				LoadingBar = Roact.createElement(LoadingBar),
			}),
			EndOfScroll = self.props.createEndOfScrollElement and Roact.createElement(EndOfScroll, {
				backToTopCallback = self.scrollBack,
				LayoutOrder = 3,
			}),
		}),
		renderStepped = Roact.createElement(ExternalEventConnection, {
			event = RunService.renderStepped,
			callback = self.renderSteppedCallback,
		}),
		inputBegan = Roact.createElement(ExternalEventConnection, {
			event = UserInputService.InputBegan,
			callback = self.inputBeganCallback,
		}),
		inputEnded = Roact.createElement(ExternalEventConnection, {
			event = UserInputService.InputEnded,
			callback = self.inputEndedCallback,
		}),
		statusBarTapped = (not _G.__TESTEZ_RUNNING_TEST__) and Roact.createElement(ExternalEventConnection, {
			event = UserInputService.StatusBarTapped,
			callback = self.statusBarTapCallback,
		}),
		bottomBarButtonPressed = refreshOnNavBar and
			Roact.createElement(ExternalEventConnection, {
				event = notificationService.RobloxEventReceived,
				callback = self.bottomBarButtonPressedCallback,
			}),
	})
end

RefreshScrollingFrame = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			currentRoute = state.Navigation.history[#state.Navigation.history]
		}
	end
)(RefreshScrollingFrame)

return RoactServices.connect({
	NotificationService = AppNotificationService,
})(RefreshScrollingFrame)