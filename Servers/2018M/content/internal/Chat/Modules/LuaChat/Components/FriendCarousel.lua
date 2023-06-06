--
-- FriendCarousel
--
-- This is a scrollable list of friend icons.
--

local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local Common = Modules.Common
local LuaApp = Modules.LuaApp

local ApiFetchUsersThumbnail = require(LuaApp.Thunks.ApiFetchUsersThumbnail)
local Constants = require(LuaApp.Constants)
local Roact = require(Common.Roact)
local RoactRodux = require(Common.RoactRodux)
local UserModel = require(LuaApp.Models.User)

local FriendCarousel = Roact.Component:extend("FriendCarousel")

local IMAGE_DOT_INGAME = "rbxasset://textures/ui/LuaApp/icons/ic-green-dot.png"
local IMAGE_DOT_ONLINE = "rbxasset://textures/ui/LuaApp/icons/ic-blue-dot.png"
local IMAGE_DOT_STUDIO = "rbxasset://textures/ui/LuaApp/icons/ic-orange-dot.png"
local DEFAULT_DOT_SIZE = 8

local IMAGE_MASK = "rbxasset://textures/ui/LuaChat/graphic/friendmask.png"
local MASK_WIDTH = 10

-- Frame around the profile image:
local IMAGE_PROFILE_BORDER = "rbxasset://textures/ui/LuaChat/graphic/gr-profile-border-36x36.png"
local IMAGE_PROFILE_DEFAULT = "rbxasset://textures/ui/LuaChat/icons/ic-profile.png"

function FriendCarousel:init()
	self.state = {
		fadeScrollLeft = false,
		fadeScrollRight = false,
	}
end

function FriendCarousel:onPositionChanged(rbx)
	-- Programatically show / hide the fade bars at either side of the carousel.
	-- This hides items that are partly visible, but completely reveals the
	-- first / last items when they're present.

	-- Early return if we're not set up yet:
	if (rbx.CanvasSize.X.Offset == 0) or (rbx.CanvasSize.Y.Offset == 0) or
		(rbx.AbsoluteWindowSize.X == 0) or (rbx.AbsoluteWindowSize.Y == 0) then
		return
	end

	local fadeLeft = (0 < rbx.CanvasPosition.X)
	local fadeRight = (rbx.CanvasSize.X.Offset - rbx.CanvasPosition.X) > rbx.AbsoluteWindowSize.X

	if (fadeLeft ~= self.state.fadeScrollLeft) or
		(fadeRight ~= self.state.fadeScrollRight) then
		spawn(function()
			self:setState( {
				fadeScrollLeft = fadeLeft,
				fadeScrollRight = fadeRight,
			})
		end)
	end
end

function FriendCarousel:didMount()
	if self.rbxScroller then
		self:onPositionChanged(self.rbxScroller)
	end
end

function FriendCarousel:render()
	-- Visual properties of this game card:
	local dotSize = self.props.dotSize or DEFAULT_DOT_SIZE
	local friends = self.props.friends or {}
	local getUserThumbnail = self.props.getUserThumbnail
	local horizontalAlignment = self.props.HorizontalAlignment or Enum.HorizontalAlignment.Left
	local itemGap = self.props.itemGap
	local itemSize = self.props.itemSize
	local layoutOrder = self.props.LayoutOrder
	local size = self.props.Size or UDim2.new(1, 0, 0, itemSize)
	local users = self.props.users

	-- Build up a horizontal list of items for our card:
	local friendItems = {}
	friendItems["Layout"] = Roact.createElement("UIListLayout", {
		FillDirection = Enum.FillDirection.Horizontal,
		HorizontalAlignment = horizontalAlignment,
		Padding = UDim.new(0, itemGap),
		SortOrder = Enum.SortOrder.LayoutOrder,
		VerticalAlignment = Enum.VerticalAlignment.Center,
	})

	local countFriends = #friends
	if countFriends > 0 then
		for index, friend in ipairs(friends) do
			-- Look up the presence information:
			local imageFriend = nil
			local iconDot = IMAGE_DOT_ONLINE
			local userFriend = users[friend.uid]
			if userFriend then
				if userFriend.presence == UserModel.PresenceType.IN_GAME then
					iconDot = IMAGE_DOT_INGAME
				elseif userFriend.presence == UserModel.PresenceType.IN_STUDIO then
					iconDot = IMAGE_DOT_STUDIO
				end

				-- Find images for the friend portraits:
				if userFriend.thumbnails and userFriend.thumbnails.HeadShot
					and userFriend.thumbnails.HeadShot.Size48x48 then
					imageFriend = userFriend.thumbnails.HeadShot.Size48x48
				end

				if imageFriend == nil then
					imageFriend = IMAGE_PROFILE_DEFAULT
					getUserThumbnail(friend.uid)
				end
			end

			friendItems[index] = Roact.createElement("Frame", {
				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				LayoutOrder = index,
				Size = UDim2.new(0, itemSize, 0, itemSize),
			}, {
				Profile = Roact.createElement("ImageButton", {
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
					Image = imageFriend,
					Size = UDim2.new(0, itemSize, 0, itemSize),
					ZIndex = 1,
				}),

				Border = Roact.createElement("ImageLabel", {
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
					Image = IMAGE_PROFILE_BORDER,
					Size = UDim2.new(0, itemSize, 0, itemSize),
					ZIndex = 2,
				}),

				Dot = Roact.createElement("ImageLabel", {
					BackgroundTransparency = 1,
					BorderSizePixel = 0,
					Image = iconDot,
					Position = UDim2.new(1, -dotSize, 1, -dotSize),
					Size = UDim2.new(0, dotSize, 0, dotSize),
					ZIndex = 3,
				}),
			})
		end
	end

	local maskLeft = nil
	if self.state.fadeScrollLeft then
		maskLeft = Roact.createElement("ImageLabel", {
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Image = IMAGE_MASK,
			Position = UDim2.new(0, 0, 0, 0),
			Rotation = 180,
			Size = UDim2.new(0, MASK_WIDTH, 1, 0),
			ZIndex = 2,
		})
	end

	local maskRight = nil
	if self.state.fadeScrollRight then
		maskRight = Roact.createElement("ImageLabel", {
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Image = IMAGE_MASK,
			Position = UDim2.new(1, -MASK_WIDTH, 0, 0),
			Size = UDim2.new(0, MASK_WIDTH, 1, 0),
			ZIndex = 2,
		})
	end

	-- This frame arrangement adds a semi-transparent overlay to
	-- fade out items at the edge of the frame:
	return Roact.createElement("Frame", {
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		LayoutOrder = layoutOrder,
		Position = UDim2.new(0, 0, 0, 0),
		Size = size,
	},{
		MaskLeft = maskLeft,

		MaskRight = maskRight,

		ScrollyFrame = Roact.createElement("ScrollingFrame", {
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			CanvasSize = UDim2.new(0, (itemSize + itemGap) * countFriends, 0, itemSize),
			ClipsDescendants = true,
			ScrollBarThickness = 0,
			Size = UDim2.new(1, 0, 1, 0),
			[Roact.Change.AbsolutePosition] = function(rbx, changed)
				self:onPositionChanged(rbx)
			end,
			[Roact.Ref] = function(rbx)
				self.rbxScroller = rbx
			end,
		}, friendItems)
	})
end

FriendCarousel = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			users = state.Users,
		}
	end,
	function(dispatch)
		return {
			getUserThumbnail = function(friendId)
				spawn(function()
					dispatch(ApiFetchUsersThumbnail(nil, { friendId },
						Constants.AvatarThumbnailRequests.FRIEND_CAROUSEL
					))
				end)
			end,
		}
	end
)(FriendCarousel)

return FriendCarousel