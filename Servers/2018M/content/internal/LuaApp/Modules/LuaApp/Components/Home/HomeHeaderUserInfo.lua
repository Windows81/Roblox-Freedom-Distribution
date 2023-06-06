local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Common = Modules.Common
local LuaApp = Modules.LuaApp

local Constants = require(LuaApp.Constants)
local Roact = require(Common.Roact)
local Text = require(Common.Text)
local Url = require(Modules.LuaApp.Http.Url)
local NotificationType = require(Modules.LuaApp.Enum.NotificationType)
local FormFactor = require(Modules.LuaApp.Enum.FormFactor)

local AppGuiService = require(Modules.LuaApp.Services.AppGuiService)
local RoactServices = require(Modules.LuaApp.RoactServices)

local HomeHeaderUserAvatar = require(LuaApp.Components.Home.HomeHeaderUserAvatar)
local FitChildren = require(LuaApp.FitChildren)

local BUILDERCLUB_LOGO_WIDTH = 48
local BUILDERCLUB_LOGO_HEIGHT = 24
local BUILDERCLUB_LOGOS = {
	[Enum.MembershipType.BuildersClub] = "rbxasset://textures/ui/LuaApp/icons/ic-bc.png",
	[Enum.MembershipType.TurboBuildersClub] = "rbxasset://textures/ui/LuaApp/icons/ic-tbc.png",
	[Enum.MembershipType.OutrageousBuildersClub] = "rbxasset://textures/ui/LuaApp/icons/ic-obc.png",
}

local BUILDERCLUB_LOGO_WIDTH_PHONE = 24
local BUILDERCLUB_LOGO_HEIGHT_PHONE = 24
local BUILDERCLUB_LOGOS_PHONE = {
	[Enum.MembershipType.BuildersClub] = "rbxasset://textures/ui/LuaApp/icons/ic-bc-small.png",
	[Enum.MembershipType.TurboBuildersClub] = "rbxasset://textures/ui/LuaApp/icons/ic-tbc-small.png",
	[Enum.MembershipType.OutrageousBuildersClub] = "rbxasset://textures/ui/LuaApp/icons/ic-obc-small.png",
}

local USERNAME_BC_PADDING = 12
local USERNAME_TEXT_SIZE = 38
local TITLE_SECTION_HEIGHT = math.max(USERNAME_TEXT_SIZE, BUILDERCLUB_LOGO_HEIGHT)

local USERNAME_BC_VERTICAL_PADDING = 20
local PROFILE_PICTURE_TO_BC_PADDING = 24
local PROFILE_PICTURE_THUMBNAIL_TYPE = Constants.AvatarThumbnailTypes.HeadShot


local function createNormalHeaderInfo(props)
	local localUserModel = props.localUserModel
	local sidePadding = props.sidePadding
	local sectionPadding = props.sectionPadding
	local onUsernameActivated = props.onUsernameActivated
	local username = localUserModel.name
	local membership = localUserModel.membership

	local isLocalPlayerBC = membership ~= Enum.MembershipType.None

	-- clickable area is equal to the text bounds
	local textBounds = Text.GetTextBounds(username, Enum.Font.SourceSans, USERNAME_TEXT_SIZE, Vector2.new(10000, 10000))

	return Roact.createElement(FitChildren.FitFrame, {
		BackgroundTransparency = 1,
		Size = UDim2.new(1, 0, 0, 0),
		fitFields = { Size = FitChildren.FitAxis.Height, },
	}, {
		HorizontalLayout = Roact.createElement("UIListLayout", {
			SortOrder = Enum.SortOrder.LayoutOrder,
			FillDirection = Enum.FillDirection.Horizontal,
			VerticalAlignment = Enum.VerticalAlignment.Center,
			Padding = UDim.new(0, PROFILE_PICTURE_TO_BC_PADDING),
		}),
		Padding = Roact.createElement("UIPadding", {
			PaddingTop = UDim.new(0, sectionPadding),
			PaddingBottom = UDim.new(0, sectionPadding),
			PaddingLeft = UDim.new(0, sidePadding),
		}),
		UserAvatar = Roact.createElement(HomeHeaderUserAvatar, {
			localUserModel = localUserModel,
			thumbnailType = PROFILE_PICTURE_THUMBNAIL_TYPE,
			onActivated = onUsernameActivated,
			LayoutOrder = 1,
		}),
		BuildersClubUsernameFrame = Roact.createElement("Frame", {
			Size = UDim2.new(
				1, -BUILDERCLUB_LOGO_WIDTH - USERNAME_BC_PADDING,
				0, USERNAME_TEXT_SIZE + BUILDERCLUB_LOGO_HEIGHT
			),
			BackgroundTransparency = 1,
			LayoutOrder = 2,
		}, {
			VerticalLayout = Roact.createElement("UIListLayout", {
				SortOrder = Enum.SortOrder.LayoutOrder,
				FillDirection = Enum.FillDirection.Vertical,
				VerticalAlignment = Enum.VerticalAlignment.Center,
				Padding = UDim.new(0, USERNAME_BC_VERTICAL_PADDING),
			}),
			Username = Roact.createElement("TextButton", {
				Size = UDim2.new(0, textBounds.X, 0, textBounds.Y),
				BackgroundTransparency = 1,
				TextSize = USERNAME_TEXT_SIZE,
				TextColor3 = Constants.Color.GRAY1,
				Font = Enum.Font.SourceSans,
				Text = username,
				TextXAlignment = Enum.TextXAlignment.Left,
				LayoutOrder = 1,
				[Roact.Event.Activated] = onUsernameActivated,
			}),
			BuildersClub = isLocalPlayerBC and Roact.createElement("ImageLabel", {
				Size = UDim2.new(0, BUILDERCLUB_LOGO_WIDTH, 0, BUILDERCLUB_LOGO_HEIGHT),
				Image = BUILDERCLUB_LOGOS[membership],
				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				LayoutOrder = 2,
			}),
		})
	})
end

-- Mobile phone is a special case.
local function createPhoneHeaderInfo(props)
	local username = props.localUserModel.name
	local membership = props.localUserModel.membership
	local sidePadding = props.sidePadding
	local sectionPadding = props.sectionPadding
	local onUsernameActivated = props.onUsernameActivated

	local isLocalPlayerBC = membership ~= Enum.MembershipType.None

	-- clickable area is equal to the text bounds
	local textBounds = Text.GetTextBounds(username, Enum.Font.SourceSans, USERNAME_TEXT_SIZE, Vector2.new(10000, 10000))

	return Roact.createElement("Frame", {
			Size = UDim2.new(1, 0, 0, TITLE_SECTION_HEIGHT + sectionPadding * 2),
			BackgroundTransparency = 1,
		}, {
			Layout = Roact.createElement("UIListLayout", {
				SortOrder = Enum.SortOrder.LayoutOrder,
				FillDirection = Enum.FillDirection.Horizontal,
				VerticalAlignment = Enum.VerticalAlignment.Center,
				Padding = UDim.new(0, isLocalPlayerBC and USERNAME_BC_PADDING or 0),
			}),
			Padding = Roact.createElement("UIPadding", {
				PaddingLeft = UDim.new(0, sidePadding),
			}),
			BuildersClub = isLocalPlayerBC and Roact.createElement("ImageLabel", {
				Size = UDim2.new(0, BUILDERCLUB_LOGO_WIDTH_PHONE, 0, BUILDERCLUB_LOGO_HEIGHT_PHONE),
				Image = BUILDERCLUB_LOGOS_PHONE[membership],
				BackgroundTransparency = 1,
				LayoutOrder = 1,
			}),
			Username = Roact.createElement("TextButton", {
				Size = UDim2.new(0, textBounds.X, 0, textBounds.Y),
				BackgroundTransparency = 1,
				TextSize = USERNAME_TEXT_SIZE,
				TextColor3 = Constants.Color.GRAY1,
				Font = Enum.Font.SourceSans,
				Text = username,
				TextXAlignment = Enum.TextXAlignment.Left,
				LayoutOrder = 2,
				[Roact.Event.Activated] = onUsernameActivated,
			}),
	})
end

local HomeHeaderUserInfo = Roact.PureComponent:extend("HomeHeaderUserInfo")

function HomeHeaderUserInfo:init()
	self.onUsernameActivated = function()
		local localUserId = self.props.localUserModel.id
		local url = Url:getUserProfileUrl(localUserId)
		self.props.guiService:BroadcastNotification(url, NotificationType.VIEW_PROFILE)
	end
end

function HomeHeaderUserInfo:render()
	local localUserModel = self.props.localUserModel
	local formFactor = self.props.formFactor
	local sidePadding = self.props.sidePadding
	local sectionPadding = self.props.sectionPadding

	local isPhone = formFactor == FormFactor.PHONE
	return (isPhone and createPhoneHeaderInfo or createNormalHeaderInfo)({
		localUserModel = localUserModel,
		sidePadding = sidePadding,
		sectionPadding = sectionPadding,
		onUsernameActivated = self.onUsernameActivated,
	})
end

return RoactServices.connect({
	guiService = AppGuiService
})(HomeHeaderUserInfo)