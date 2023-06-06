local CoreGui = game:GetService("CoreGui")
local Modules = CoreGui.RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)

local Constants = require(Modules.LuaChat.Constants)
local Create = require(Modules.LuaChat.Create)
local GameShareComponent = require(Modules.LuaChat.Components.GameShareComponent)
local FormFactor = require(Modules.LuaApp.Enum.FormFactor)
local FlagSettings = require(Modules.LuaApp.FlagSettings)

local isLoadingHUDOniOSEnabledForGameShare = FlagSettings.IsLoadingHUDOniOSEnabledForGameShare()
local RoactGameShareWrapper = Roact.PureComponent:extend("RoactGameShareWrapper")

function RoactGameShareWrapper:init()
	self.appState = self.props.chatMaster._appState
end

function RoactGameShareWrapper:didMount()
	local placeId = self.props.placeId
	local formFactor = self.props.formFactor

	local innerFrame = Create.new"Frame" {
		Name = "InnerFrame",
		Size = UDim2.new(1, 0, 1, 0),
		Position = UDim2.new(0.5, 0, 0, 0),
		AnchorPoint = Vector2.new(0.5, 0),
		BackgroundColor3 = Constants.Color.GRAY5,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		LayoutOrder = 2,
		Create.new("UIListLayout") {
			Name = "ListLayout",
			SortOrder = Enum.SortOrder.LayoutOrder,
		},
	}

	if formFactor == FormFactor.TABLET then
		local dividerHeight = Constants.GameShareView.TABLET_HORIZONTAL_DIVIDER_HEIGHT
		local viewWidth = Constants.GameShareView.TABLET_VIEW_WIDTH

		innerFrame.Size = UDim2.new(0, viewWidth, 1, -dividerHeight)

		local tabletDivider = Create.new"Frame" {
			Name = "TabletDivider",
			BackgroundColor3 = Constants.Color.GRAY5,
			BorderSizePixel = 0,
			Size = UDim2.new(1, 0, 0, dividerHeight),
			LayoutOrder = 1,
		}
		tabletDivider.Parent = innerFrame
	end

	self.gameShareInstance = GameShareComponent.new(self.appState, placeId, innerFrame)
	self.gameShareInstance.rbx.Parent = self.shareGameWrapper
	self.gameShareInstance:Start()

	if isLoadingHUDOniOSEnabledForGameShare then
		spawn(function()
			wait(0.1)
			local GuiService = game:GetService("GuiService")
			local AppPage = require(Modules.LuaApp.AppPage)
			local NotificationType = require(Modules.LuaApp.Enum.NotificationType)
			-- Staging broadcasting of APP_READY to accomodate for unpredictable
			-- delay on the native side.
			-- Once Lua tab bar is integrated, there will be no use for this
			GuiService:BroadcastNotification(AppPage.ShareGameToChat, NotificationType.APP_READY)
		end)
	end
end

function RoactGameShareWrapper:render()
	return Roact.createElement("Frame", {
		Name = "ShareGameToChatFromGameDetails",
		Size = UDim2.new(1, 0, 1, 0),
		BackgroundColor3 = Constants.Color.GRAY5,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
		[Roact.Ref] = function(rbx)
			if not self.shareGameWrapper then
				self.shareGameWrapper = rbx
			end
		end,
	})
end

function RoactGameShareWrapper:willUnmount()
	self.gameShareInstance:Stop()
	self.gameShareInstance:Destruct()
	self.gameShareInstance = nil
end

RoactGameShareWrapper = RoactRodux.connect(function(store)
	local state = store:getState()

	return {
		store = store,
		formFactor = state.FormFactor,
	}
end)(RoactGameShareWrapper)

return RoactGameShareWrapper