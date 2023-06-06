local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local AppGuiService = require(Modules.LuaApp.Services.AppGuiService)
local RoactServices = require(Modules.LuaApp.RoactServices)


local UserThumbnailPortraitOrientation = require(Modules.LuaApp.Components.Home.UserThumbnailPortraitOrientation)
local UserThumbnailDefaultOrientation = require(Modules.LuaApp.Components.Home.UserThumbnailDefaultOrientation)
local Constants = require(Modules.LuaApp.Constants)
local Url = require(Modules.LuaApp.Http.Url)
local NotificationType = require(Modules.LuaApp.Enum.NotificationType)
local FormFactor = require(Modules.LuaApp.Enum.FormFactor)

local USER_ENTRY_WIDTH = 105
local USER_ENTRY_WIDTH_PHONE = 115
local VERTICAL_PADDING = 15
local HORIZONTAL_PADDING = 7.5

local UserCarouselEntry = Roact.PureComponent:extend("UserCarouselEntry")

function UserCarouselEntry:init()
	self.state = {
		highlighted = false
	}

	self.onInputBegan = function(_, inputObject)
		--TODO: Remove after CLIPLAYEREX-1468
		local inputStateChangedConnection = nil
		inputStateChangedConnection = inputObject:GetPropertyChangedSignal("UserInputState"):Connect(function()
			if inputObject.UserInputState == Enum.UserInputState.End
				or inputObject.UserInputState == Enum.UserInputState.Cancel then
				inputStateChangedConnection:Disconnect()
				self.onInputEnded()
			end
		end)
		self:setState({
			highlighted = true,
		})
	end

	self.onInputEnded = function()
		self:setState({
			highlighted = false,
		})
	end

	self.onInputChanged = self.onInputEnded

	self.onActivated = function(_, inputObject)
		if inputObject.UserInputState == Enum.UserInputState.End then
			local user = self.props.user
			if user then
				local url = Url:getUserProfileUrl(user.id)
				self.props.guiService:BroadcastNotification(url, NotificationType.VIEW_PROFILE)
			end
		end
	end
end

function UserCarouselEntry:render()
	local count = self.props.count
	local user = self.props.user
	local formFactor = self.props.formFactor
	local highlightColor = self.state.highlighted and Constants.Color.GRAY5 or Constants.Color.WHITE
	local thumbnailType = self.props.thumbnailType

	local totalHeight = UserCarouselEntry.height(formFactor)
	local thumbnailSize = UserCarouselEntry.thumbnailSize(formFactor)

	local isPhone = formFactor == FormFactor.PHONE
	local userThumbnailComponent = isPhone and UserThumbnailPortraitOrientation
		or UserThumbnailDefaultOrientation

	return Roact.createElement("ImageButton", {
		AutoButtonColor = false,
		Size = UDim2.new(0, isPhone and USER_ENTRY_WIDTH_PHONE or USER_ENTRY_WIDTH, 0, totalHeight),
		BackgroundColor3 = highlightColor,
		BorderSizePixel = 0,
		LayoutOrder = count,
		[Roact.Event.InputBegan] = self.onInputBegan,
		[Roact.Event.InputEnded] = self.onInputEnded,
		-- When Touch is used for scrolling, InputEnded gets sunk into scrolling action
		[Roact.Event.InputChanged] = self.onInputChanged,
		[Roact.Event.Activated] = self.onActivated,
	}, {
		ThumbnailFrame = Roact.createElement("Frame", {
			Size = UDim2.new(0, thumbnailSize, 0, thumbnailSize),
			Position = UDim2.new(0.5, 0, 0, VERTICAL_PADDING),
			AnchorPoint = Vector2.new(0.5, 0),
			BackgroundTransparency = 1,
		}, {
			Thumbnail = Roact.createElement(userThumbnailComponent, {
				user = user,
				formFactor = formFactor,
				maskColor = Constants.Color.WHITE,
				highlightColor = highlightColor,
				thumbnailType = thumbnailType,
			}),
		}),
	})
end

UserCarouselEntry = RoactServices.connect({
	guiService = AppGuiService
})(UserCarouselEntry)

function UserCarouselEntry.thumbnailSize(formFactor)
	return formFactor == FormFactor.PHONE and UserThumbnailPortraitOrientation.size(formFactor)
		or UserThumbnailDefaultOrientation.size(formFactor)
end

function UserCarouselEntry.height(formFactor)
	local component = formFactor == FormFactor.PHONE and UserThumbnailPortraitOrientation
		or UserThumbnailDefaultOrientation

	return VERTICAL_PADDING
		+ component.height(formFactor)
		+ VERTICAL_PADDING
end

function UserCarouselEntry.horizontalPadding()
	return HORIZONTAL_PADDING
end

return UserCarouselEntry