local Modules = game:GetService("CoreGui").RobloxGui.Modules
local HttpService = game:GetService("HttpService")
local PlatformService = nil
pcall(function() PlatformService = game:GetService("PlatformService") end)
local Roact = require(Modules.Common.Roact)

local Components = Modules.Shell.Components
local PresenceCard = require(Components.Social.PresenceCard)
local WindowedScrollingFrame = require(Components.Common.WindowedScrollingFrame)
local Immutable = require(Modules.Common.Immutable)
local Spinner = require(Components.Common.Spinner)
local SideBarComponent = require(Components.Common.SideBar)
local Utility = require(Modules.Shell.Utility)
local EventHub = require(Modules.Shell.EventHub)
local GameJoinModule = require(Modules.Shell.GameJoin)
local Strings = require(Modules.Shell.LocalizedStrings)
local SoundManager = require(Modules.Shell.SoundManager)
local RedirectComponent = require(Modules.Shell.Components.Common.RedirectComponent)
local UserThumbnailLoader = require(Components.Common.UserThumbnailLoader)

local SIDE_BAR_ITEMS = {
	JoinGame = Strings:LocalizedString("JoinGameWord"),
	ViewDetails = Strings:LocalizedString("ViewGameDetailsWord"),
	ViewProfile = Strings:LocalizedString("ViewGamerCardWord"),
	EmptyFriendSideBar = Strings:LocalizedString("EmptyFriendSideBarWord"),
}

local FriendsScrollingView = Roact.PureComponent:extend("FriendsScrollingView")

function FriendsScrollingView:init()
	self.state = {
		sideBarInFocus = false,
		sideBarShow = false,
		currentSelectedIndex = 1,
	}

	self.onSideBarClose = function()
		self:setState({
			sideBarInFocus = false,
			sideBarShow = false,
		})
	end
	self.onSideBarOpen = function(data)
		Utility.SetSelectedCoreObject(nil)
		self:setState({
			sideBarInFocus = true,
			sideBarShow = true,
		})
	end

	self.groupKey = HttpService:GenerateGUID(false)
end

function FriendsScrollingView:render()
	local props = self.props
	local friendsData = props.friendsData
	local initialized = props.initialized
	local actionPriority = self.props.actionPriority or 0

	local hide = props.hide
	local inFocus = props.inFocus
	local sideBarInFocus = false
	local friendsScrollingFrameInFocus = false

	local children = {}
	if not hide and inFocus then
		sideBarInFocus = self.state.sideBarShow and self.state.sideBarInFocus
		if not sideBarInFocus and #friendsData > 0 then
			friendsScrollingFrameInFocus = true
		end
	end

	if initialized and friendsData then
		if #friendsData > 0 then
			local itemSize = Vector2.new(440, 120)
			local itemsPaddingOffset = 20
			local itemTotalSizeY = itemSize.Y + itemsPaddingOffset
			local itemsCount = math.floor(self.props.size.Y.Offset / itemTotalSizeY)
			assert(itemsCount ~= 0, "The scrolling window is too small to accommodate any presence card.")
			--We should have at least two items to ensure we can always select the top second item
			--while keep the top first item fully in view.
			--If the window is too small, we will always select the top first item.
			local itemOffsetStart = itemsCount > 2 and itemTotalSizeY or 0
			--This make sure when we scroll down the top card won't be clipped
			local itemOffsetEnd = self.props.size.Y.Offset - itemsCount * itemTotalSizeY + itemsPaddingOffset
			children.FriendsScrollingFrame = Roact.createElement(WindowedScrollingFrame, {
				items = friendsData,
				itemSize = itemSize,
				itemsPaddingOffset = itemsPaddingOffset,
				itemOffsetStart = itemOffsetStart,
				itemOffsetEnd = itemOffsetEnd,
				scrollingDirection = Enum.ScrollingDirection.Y,
				inFocus = friendsScrollingFrameInFocus,
				renderItem = function(data, index)
					local presenceCardProps = Immutable.JoinDictionaries(data, {
						layoutOrder = index,
						size = UDim2.new(0, itemSize.X, 0, itemSize.Y),
						focused = inFocus and self.state.currentSelectedIndex == index,
						selected = friendsScrollingFrameInFocus and self.state.currentSelectedIndex == index,
					})
					--Set up callbacks
					presenceCardProps.onActivated = function(bt)
						SoundManager:Play("SideMenuSlideIn")
						self.onSideBarOpen()
					end
					presenceCardProps.onSelectionGained = function()
						if self.state.currentSelectedIndex ~= index then
							self:setState({
								currentSelectedIndex = index,
							})
						end
					end
					return Roact.createElement(PresenceCard, presenceCardProps)
				end
			})


			local data = friendsData[self.state.currentSelectedIndex]
			if inFocus and data and data.robloxuid then
				children.ProfileImage = Roact.createElement(UserThumbnailLoader, {
					rbxuid = data.robloxuid,
					thumbnailType = Enum.ThumbnailType.AvatarThumbnail,
					thumbnailSize = Enum.ThumbnailSize.Size352x352,
					position = UDim2.new(1, 101, 0, 0),
					size = UDim2.new(0, 680, 0, 680),
					backgroundTransparency = 1,
					showSpinner = true
				})
			end

			if self.state.sideBarShow and data then
				local sideBarButtons = {}
				if data.robloxuid and data.robloxuid > 0 and data.robloxStatus == "InGame" then
					local placeId = data.placeId
					local lastLocation = data.lastLocation
					local robloxuid = data.robloxuid
					table.insert(sideBarButtons, {
						text = SIDE_BAR_ITEMS.JoinGame,
						callback = function()
							GameJoinModule:StartGame(GameJoinModule.JoinType.Follow, robloxuid)
						end
					})
					table.insert(sideBarButtons, {
						text = SIDE_BAR_ITEMS.ViewDetails,
						callback = function()
							EventHub:dispatchEvent(EventHub.Notifications["OpenGameDetail"], placeId, lastLocation, nil)
						end
					})
				end
				if data.xuid and #data.xuid > 0 and PlatformService then
					local xuid = data.xuid
					table.insert(sideBarButtons, {
						text = SIDE_BAR_ITEMS.ViewProfile,
						callback = function()
							-- NOTE: This will try to pop up the xbox system gamer card, failure will be handled by the xbox.
							pcall(function()
								PlatformService:PopupProfileUI(Enum.UserInputType.Gamepad1, xuid)
							end)
						end
					})
				end

				local sideBarText = nil
				if #sideBarButtons == 0 then
					sideBarText = SIDE_BAR_ITEMS.EmptyFriendSideBar
					sideBarButtons = nil
				end
				children.SideBar = Roact.createElement(SideBarComponent, {
					actionPriority = actionPriority + 1,
					text = sideBarText,
					buttons = sideBarButtons,
					inFocus = sideBarInFocus,
					onClose = self.onSideBarClose,
					onRemoveFocus = function()
						self:setState({
							sideBarInFocus = false
						})
					end,
				})
			end
		else
			children.NoFriendsView = props.noFriendsView
		end
	else
		children.Spinner = Roact.createElement(Spinner)
	end

	children.NavObj = Roact.createElement(RedirectComponent, {
		ActionPriority = actionPriority,
		Key = self.groupKey,
		InFocus = inFocus,
		RedirectBack = props.redirectBack,
		RedirectLeft = props.redirectLeft,
		RedirectRight = props.redirectRight,
		RedirectUp = props.redirectUp,
		RedirectDown = props.redirectDown,
	})

	return Roact.createElement("Frame", {
		BackgroundTransparency = 1,
		Size = self.props.size,
		Position = self.props.position,
		[Roact.Ref] = function(rbx)
			self.ref = rbx
		end,
		Visible = not hide,
	}, children)
end


function FriendsScrollingView:didMount()
	delay(0, function()
		if self.props.hide == false and self.props.inFocus then
			if self.ref ~= nil then
				Utility.RemoveSelectionGroup(self.groupKey)
				Utility.AddSelectionParent(self.groupKey, self.ref)
			end
		end
	end)
end

function FriendsScrollingView:didUpdate(previousProps, previousState)
	if self.props.hide or self.props.inFocus == previousProps.inFocus then
		return
	end
	if self.props.inFocus then
		if self.ref then
			Utility.RemoveSelectionGroup(self.groupKey)
			Utility.AddSelectionParent(self.groupKey, self.ref)
		end
	else
		Utility.RemoveSelectionGroup(self.groupKey)
	end
end

function FriendsScrollingView:willUnmount()
	Utility.RemoveSelectionGroup(self.groupKey)
end

return FriendsScrollingView