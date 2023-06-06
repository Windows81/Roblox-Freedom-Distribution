local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Constants = require(Modules.LuaApp.Constants)
local Roact = require(Modules.Common.Roact)
local Text = require(Modules.Common.Text)
local User = require(Modules.LuaApp.Models.User)
local FlagSettings = require(Modules.LuaApp.FlagSettings)

local isPeopleListV1Enabled = FlagSettings.IsPeopleListV1Enabled()
local useCppTextTruncation = FlagSettings.UseCppTextTruncation()

local DEFAULT_THUMBNAIL_ICON = Constants.AVATAR_PLACEHOLDER_IMAGE
local OVERLAY_IMAGE_BIG = "rbxasset://textures/ui/LuaApp/graphic/gr-friend.png"
local PRESENCE_BORDER_IMAGE = "rbxasset://textures/ui/LuaApp/graphic/gr-card@2x.png"
local PRESENCE_FONT = Enum.Font.SourceSans
local THUMBNAIL_IMAGE_SIZE_ENUM = Constants.AvatarThumbnailSizes.Size100x100
local USER_NAME_FONT = Enum.Font.SourceSansLight
local DEFAULT_PRESENCE_TEXT = "Online"

local function getLastLocationText(lastLocation)
	local locationWithoutPlayingPrefix = lastLocation and lastLocation:gsub("^Playing%s*", "")
	return locationWithoutPlayingPrefix == "" and DEFAULT_PRESENCE_TEXT or locationWithoutPlayingPrefix
end

local UserThumbnail = Roact.PureComponent:extend("UserThumbnail")

function UserThumbnail:init()
	self.resize = function()
		if useCppTextTruncation then
			return
		end
		if self.usernameTextLabel then
			Text.TruncateTextLabel(self.usernameTextLabel, "...")
		end
		if self.presenceTextLabel then
			Text.TruncateTextLabel(self.presenceTextLabel, "...")
		end
	end
end

function UserThumbnail:render()
	local measurements = self.props.measurements
	local user = self.props.user
	local highlightColor = self.props.highlightColor
	local thumbnailType = self.props.thumbnailType

	local thumbnailSize = measurements.THUMBNAIL_SIZE
	local dropShadowSize = measurements.DROPSHADOW_SIZE
	local dropShadowMargin = measurements.PRESENCE.DROPSHADOW_MARGIN
	local totalHeight = measurements.TOTAL_HEIGHT

	local usernameLineHeight = measurements.USERNAME.TEXT_LINE_HEIGHT
	local usernameTopPadding = measurements.USERNAME.TEXT_TOP_PADDING
	local usernameTextFontSize = measurements.USERNAME.TEXT_FONT_SIZE

	local presenceIcons = measurements.PRESENCE.ICONS
	local presenceTextFontSize = measurements.PRESENCE.TEXT_FONT_SIZE
	local presenceTextLineHeight = measurements.PRESENCE.TEXT_LINE_HEIGHT
	local presenceTextTopPadding = measurements.PRESENCE.TEXT_TOP_PADDING
	local presenceIconSize = measurements.PRESENCE.ICON_SIZE
	local presenceBorderDiameter = measurements.PRESENCE.BORDER_DIAMETER
	local presenceIconMargin = dropShadowMargin + measurements.PRESENCE.ICON_OFFSET

	local userLastLocation = getLastLocationText(user.lastLocation)
	local isPresenceLabelVisible = isPeopleListV1Enabled and user.presence == User.PresenceType.IN_GAME

	return Roact.createElement("Frame", {
		Size = UDim2.new(0, thumbnailSize, 0, totalHeight),
		BackgroundTransparency = 1,
		[Roact.Ref] = function(rbx)
			self.mainFrame = rbx
		end,
	}, {
		Image = Roact.createElement("ImageLabel", {
			Size = UDim2.new(0, thumbnailSize, 0, thumbnailSize),
			BackgroundColor3 = Constants.Color.WHITE,
			BorderSizePixel = 0,
			Image = user and user.thumbnails and user.thumbnails[thumbnailType]
				and user.thumbnails[thumbnailType][THUMBNAIL_IMAGE_SIZE_ENUM] or DEFAULT_THUMBNAIL_ICON,
		}, {
			MaskFrame = Roact.createElement("ImageLabel", {
				Size = UDim2.new(0, dropShadowSize, 0, dropShadowSize),
				Position = UDim2.new(0.5, 0, 0.5, 0),
				AnchorPoint = Vector2.new(0.5, 0.5),
				BackgroundTransparency = 1,
				Image = OVERLAY_IMAGE_BIG,
				ImageColor3 = highlightColor,
			},{
				PresenceIconBorder = Roact.createElement("ImageLabel", {
					Size = UDim2.new(0, presenceBorderDiameter, 0, presenceBorderDiameter),
					AnchorPoint = Vector2.new(1, 1),
					Position = UDim2.new(1, -presenceIconMargin, 1, -presenceIconMargin),
					BackgroundTransparency = 1,
					Image = PRESENCE_BORDER_IMAGE,
					Visible = user.presence ~= User.PresenceType.OFFLINE,
				},{
					PresenceIcon = Roact.createElement("ImageLabel", {
						Size = UDim2.new(0, presenceIconSize, 0, presenceIconSize),
						AnchorPoint = Vector2.new(0.5, 0.5),
						Position = UDim2.new(0.5, 0, 0.5, 0),
						BackgroundTransparency = 1,
						Image = presenceIcons[user.presence],
					}),
				}),
			}),
		}),
		Username = Roact.createElement("TextLabel", {
			Size = UDim2.new(1, 0, 0, usernameLineHeight),
			Position = UDim2.new(0, 0, 0, thumbnailSize + usernameTopPadding),
			BackgroundTransparency = 1,
			Text = user.name,
			TextTruncate = Enum.TextTruncate.AtEnd,
			TextSize = usernameTextFontSize,
			TextColor3 = Constants.Color.GRAY1,
			Font = USER_NAME_FONT,
			-- Remove these functions when we take out useCppTextTruncation flag.
			[Roact.Ref] = function(rbx)
				self.usernameTextLabel = rbx
			end,
			[Roact.Change.Text] = self.resize,
		}),
		Presence = Roact.createElement("TextLabel", {
			Size = UDim2.new(1, 0, 0, presenceTextLineHeight),
			Position = UDim2.new(0, 0, 0, thumbnailSize + usernameTopPadding + usernameLineHeight + presenceTextTopPadding),
			BackgroundTransparency = 1,
			Text = userLastLocation,
			TextTruncate = Enum.TextTruncate.AtEnd,
			TextSize = presenceTextFontSize,
			TextColor3 = Constants.Color.GRAY2,
			Font = PRESENCE_FONT,
			Visible = isPresenceLabelVisible,
			-- Remove these functions when we take out useCppTextTruncation flag.
			[Roact.Ref] = function(rbx)
				self.presenceTextLabel = rbx
			end,
			[Roact.Change.Text] = self.resize,
		}),
	})
end

function UserThumbnail:didMount()
	self.resize()
end


return UserThumbnail
