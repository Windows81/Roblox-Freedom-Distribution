--[[
		Creates a PresenceCard component
		Props:
			gamertag: string - Xbox Gamertag.
			robloxName: string - Roblox name.
			robloxuid: int - Roblox user id.
			xuid: int - Xbox user id.
			robloxStatus: string - User's roblox xboxStatus.
			xboxStatus: string - User's xbox xboxStatus.
			lastLocation: string - User's last location info.
			layoutOrder: int - Controls the sorting priority of this button.
			size: UDim2 - The size of the presence card.
			onSelectionGained : function(guiObject : Ref<GuiObject>) -
								Fires when the GuiObject is being focused on with the Gamepad selector.
			onSelectionLost : function(guiObject : Ref<GuiObject>) -
								Fires when the Gamepad selector stops focusing on the GuiObject.
			onActivated : function(guiObject : Ref<GuiObject>) -
								Fires when the button is activated.
]]
local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local GlobalSettings = require(Modules.Shell.GlobalSettings)
local Components = Modules.Shell.Components
local UserThumbnailLoader = require(Components.Common.UserThumbnailLoader)
local Strings = require(Modules.Shell.LocalizedStrings)
local Utility = require(Modules.Shell.Utility)
local SoundComponent = require(Modules.Shell.Components.Common.SoundComponent)

local PresenceCard = Roact.PureComponent:extend("PresenceCard")

function PresenceCard:init()
	self.selectionImageObject = Utility.Create "ImageLabel"({
		Name = "SelectorImage",
		Image = GlobalSettings.Images.ButtonSelector,
		Position = UDim2.new(0, -7, 0, -7),
		Size = UDim2.new(1, 14, 1, 14),
		BackgroundTransparency = 1,
		ScaleType = Enum.ScaleType.Slice,
		SliceCenter = Rect.new(31, 31, 63, 63),
	})
	self.onCreate = function(rbx)
		self.ref = rbx
	end
	self.defaultProps = {
		buttonColor3 = GlobalSettings.Colors.WhiteButton,
		buttonTransparency = 0.8,
		textColor3 = GlobalSettings.Colors.WhiteText,
		iconColor3 = GlobalSettings.Colors.WhiteText,
	}
	self.focusedProps = {
		buttonColor3 = GlobalSettings.Colors.BlueButton,
		buttonTransparency = 0,
		textColor3 = GlobalSettings.Colors.BlackText,
		iconColor3 = GlobalSettings.Colors.BlackText,
	}
	self.buttonImage = GlobalSettings.Images.ButtonDefault
end

function PresenceCard:render()
	local props = self.props

	local focused = self.props.focused
	local currProps = focused and self.focusedProps or self.defaultProps
	local gamertagText = props.gamertag or ""
	local robloxNameText = props.robloxName or ""
	local showGamertag = gamertagText ~= ""
	local showRobloxName = robloxNameText ~= ""
	local statusText = ""
	local statusImageColor3 = GlobalSettings.Colors.GreySelectedButton

	local function setPresence(statusStr, statusColor)
		statusImageColor3 = statusColor
		if statusStr and statusStr ~= "" then
			statusText = statusStr
		end
	end
	if props.robloxStatus == "InGame" then
		setPresence(props.lastLocation, GlobalSettings.Colors.GreenText)
	elseif props.robloxStatus == "InStudio" then
		setPresence(props.lastLocation, GlobalSettings.Colors.OrangeText)
	elseif props.robloxStatus == "Online" then
		setPresence("Roblox", GlobalSettings.Colors.BlueText)
	else
		if props.xboxStatus and props.xboxStatus == "Online" then
			setPresence(Strings:LocalizedString("OnlineWord"), GlobalSettings.Colors.BlueText)
		else
			setPresence(Strings:LocalizedString("OfflineWord"), GlobalSettings.Colors.GreyText)
		end
	end

	return Roact.createElement("ImageButton", {
		Image = self.buttonImage,
		Position = UDim2.new(0.5, 0, 0.5, 0),
		AnchorPoint = Vector2.new(0.5, 0.5),
		LayoutOrder = props.layoutOrder,
		Size = props.size or UDim2.new(0, 440, 0, 120),
		ImageColor3 = currProps.buttonColor3,
		ImageTransparency = currProps.buttonTransparency,
		ScaleType = Enum.ScaleType.Slice,
		SliceCenter = Rect.new(8, 8, 9, 9),
		SelectionImageObject = self.selectionImageObject,
		BackgroundTransparency = 1,
		[Roact.Event.SelectionGained] = props.onSelectionGained,
		[Roact.Event.SelectionLost] = props.onSelectionLost,
		[Roact.Event.Activated] = props.onActivated,
		[Roact.Ref] = self.onCreate,
	},{
		MoveSelection = Roact.createElement(SoundComponent, {
			SoundName = "MoveSelection",
		}),

		AvatarImage = Roact.createElement(UserThumbnailLoader, {
			rbxuid = props.robloxuid,
			thumbnailType = Enum.ThumbnailType.HeadShot,
			thumbnailSize = Enum.ThumbnailSize.Size100x100,
			position = UDim2.new(0, 10, 0, 10),
			size = UDim2.new(0, 100, 0, 100),
		}),

		ContentContainer = Roact.createElement("Frame",{
			Size = UDim2.new(1, -140, 1, 0),
			Position = UDim2.new(0, 126, 0, 0),
			BackgroundTransparency = 1,
			ClipsDescendants = true,
		}, {
			UIPadding = Roact.createElement("UIPadding", {
				PaddingTop = UDim.new(0, 10),
				PaddingBottom = UDim.new(0, 10)
			}),

			UIListLayout = Roact.createElement("UIListLayout", {
				Padding = UDim.new(0, 7),
				SortOrder = Enum.SortOrder.LayoutOrder,
				HorizontalAlignment = Enum.HorizontalAlignment.Left,
				VerticalAlignment = Enum.VerticalAlignment.Center,
			}),

			GamertagContainer = showGamertag and Roact.createElement("Frame", {
				Size = UDim2.new(1, 0, 0, 30),
				LayoutOrder = 1,
				BackgroundTransparency = 1
			},{
				GamertagLabel = Roact.createElement("TextLabel", {
					Text = gamertagText,
					Size = UDim2.new(1, 0, 1, 0),
					Position = UDim2.new(0, 0, 0, 0),
					TextXAlignment = Enum.TextXAlignment.Left,
					TextColor3 = currProps.textColor3,
					Font = GlobalSettings.Fonts.Regular,
					TextSize = 30,
					TextScaled = true,
					BackgroundTransparency = 1,
				}),
			}),

			RobloxNameContainer = showRobloxName and Roact.createElement("Frame", {
				Size = UDim2.new(1, 0, 0, 30),
				LayoutOrder = 2,
				BackgroundTransparency = 1
			},{
				RobloxIcon = Roact.createElement("ImageLabel", {
					BackgroundTransparency = 1,
					Image = GlobalSettings.Images.RobloxIcon,
					ImageColor3 = currProps.iconColor3,
					Position = UDim2.new(0, 0, 0, 1),
					Size = UDim2.new(0, 28, 0, 28),
				}),
				RobloxNameLabel = Roact.createElement("TextLabel", {
					Text = robloxNameText,
					Size = UDim2.new(1, -38, 1, 0),
					Position = UDim2.new(0, 38, 0, 0),
					TextXAlignment = Enum.TextXAlignment.Left,
					TextColor3 = currProps.textColor3,
					Font = GlobalSettings.Fonts.Regular,
					TextSize = 30,
					TextScaled = true,
					BackgroundTransparency = 1,
				})
			}),

			StatusContainer = Roact.createElement("Frame", {
				Size = UDim2.new(1, 0, 0, 26),
				LayoutOrder = 3,
				BackgroundTransparency = 1
			},{
				PresenceStatusImage = Roact.createElement("ImageLabel", {
					BackgroundTransparency = 1,
					Image = GlobalSettings.Images.OnlineStatusIcon,
					Size = UDim2.new(0, 18, 0, 18),
					Position = UDim2.new(0, 5, 0, 4),
					ImageColor3 = statusImageColor3,
				}),
				PresenceLabel = Roact.createElement("TextLabel", {
					Text = statusText,
					Size = UDim2.new(1, -38, 1, 0),
					Position = UDim2.new(0, 33, 0, 0),
					TextXAlignment = Enum.TextXAlignment.Left,
					TextColor3 = currProps.textColor3,
					Font = GlobalSettings.Fonts.Regular,
					TextSize = 26,
					BackgroundTransparency = 1,
				})
			}),
		})
	})
end

function PresenceCard:didMount()
	delay(0, function()
		if self.props.selected then
			Utility.SetSelectedCoreObject(self.ref)
		end
	end)
end

function PresenceCard:didUpdate(previousProps, previousState)
	if not previousProps.selected and self.props.selected then
		Utility.SetSelectedCoreObject(self.ref)
	end
end

return PresenceCard