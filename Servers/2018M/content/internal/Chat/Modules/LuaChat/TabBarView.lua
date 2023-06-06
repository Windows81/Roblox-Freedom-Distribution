local CoreGui = game:GetService("CoreGui")

local Modules = CoreGui.RobloxGui.Modules
local LuaApp = Modules.LuaApp
local LuaChat = Modules.LuaChat

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)
local RoactMotion = require(LuaApp.RoactMotion)

local Constants = require(LuaApp.Constants)
local Device = require(LuaChat.Device)
local FormFactor = require(LuaApp.Enum.FormFactor)
local Text = require(LuaChat.Text)

local NO_TABS = "Tabbed frame has no tabs. If this functionality is desired, use a Frame."
local NO_CONTENT = "Content function didn't return a table. If no content is desired, return an empty table."

local DEFAULT_DROPS_SHADOW_HEIGHT = 5

local DEFAULT_INDICATOR_HEIGHT = 4
local DEFAULT_INDICATOR_COLOR = Constants.Color.BLUE_PRIMARY

local DEFAULT_TAB_BAR_HEIGHT = 44
local DEFAULT_TAB_BAR_BUTTON_MINIMUM_WIDTH = 72
local DEFAULT_TAB_BAR_BUTTON_PADDING = 12
local DEFAULT_TAB_BAR_BUTTON_BACKGROUND_COLOR = Constants.Color.WHITE

local DEFAULT_BUTTON_TEXT_SIZE = 20
local DEFAULT_BUTTON_TEXT_COLOR = Constants.Color.GRAY1
local DEFAULT_BUTTON_TEXT_FONT = Enum.Font.SourceSans

local DEFAULT_BACKGROUND_COLOR = Constants.Color.GRAY6
local DEFAULT_SELECTED_INDEX = 1
local DEFAULT_TAB_COUNT = 4

local DEFAULT_SPRING_DAMPING = 35
local DEFAULT_SPRING_STIFFNESS = 390
local DEFAULT_PRECISION = 4

local DROPS_SHADOW_IMAGE = "rbxasset://textures/ui/LuaChat/graphic/gr-overlay-shadow.png"

local function getButtonWidth(
		formFactor, text, buttonTextFont, buttonTextSize,
		tabBarButtonMinimumWidth, tabBarButtonPadding, frameWidth
	)
    if formFactor == FormFactor.TABLET then
        return frameWidth / DEFAULT_TAB_COUNT
    end

    local textWidth = Text.GetTextWidth(text, buttonTextFont, buttonTextSize)
    return 2 * tabBarButtonPadding + ((tabBarButtonMinimumWidth > textWidth) and  tabBarButtonMinimumWidth or textWidth)
end

local TabBarView = Roact.PureComponent:extend("TabBarView")

TabBarView.defaultProps = {
	BackgroundColor = DEFAULT_BACKGROUND_COLOR,
	ButtonTextColor = DEFAULT_BUTTON_TEXT_COLOR,
	ButtonTextFont = DEFAULT_BUTTON_TEXT_FONT,
	ButtonTextSize = DEFAULT_BUTTON_TEXT_SIZE,
	DropsShadowHeight = DEFAULT_DROPS_SHADOW_HEIGHT,
	IndicatorColor = DEFAULT_INDICATOR_COLOR,
	IndicatorHeight = DEFAULT_INDICATOR_HEIGHT,
	Precision = DEFAULT_PRECISION,
	SpringDamping = DEFAULT_SPRING_DAMPING,
	SpringStiffness = DEFAULT_SPRING_STIFFNESS,
	TabBarHeight = DEFAULT_TAB_BAR_HEIGHT,
	TabBarButtonColor = DEFAULT_TAB_BAR_BUTTON_BACKGROUND_COLOR,
	TabBarButtonMinimumWidth = DEFAULT_TAB_BAR_BUTTON_MINIMUM_WIDTH,
	TabBarButtonPadding = DEFAULT_TAB_BAR_BUTTON_PADDING,
}

function TabBarView:init()
    self.state = {
		autoScroll = false,
		frameWidth = 0,
		frameHeight = 0,
        selectedTabIndex = self.props.SelectedTabIndex or DEFAULT_SELECTED_INDEX,
		scrollingFrameXOffset = 0,
    }

    self.onRef = function(rbx)
        if rbx then
            if self.onAbsoluteSizeChanged then
                self.onAbsoluteSizeChanged:Disconnect()
            end
            self.onAbsoluteSizeChanged = rbx:GetPropertyChangedSignal("AbsoluteSize"):Connect(function()
                if self.state.frameWidth ~= rbx.AbsoluteSize.X then
                    self:setState({
                        frameWidth = rbx.AbsoluteSize.X,
						frameHeight = rbx.AbsoluteSize.Y,
                    })
                end
            end)
        else
            if self.onAbsoluteSizeChanged then
                self.onAbsoluteSizeChanged:Disconnect()
                self.onAbsoluteSizeChanged = nil
            end
        end
    end

	self.onScrollingFrameRef = function(rbx)
		if rbx then
			self.onScrollingFrameCanvasPositionChanged = rbx:GetPropertyChangedSignal("CanvasPosition"):Connect(function()
				if not self.state.autoScroll then
					self:setState({
						scrollingFrameXOffset = rbx.CanvasPosition.X
					})
				end
			end)
		else
			if self.onScrollingFrameCanvasPositionChanged then
				self.onScrollingFrameCanvasPositionChanged:Disconnect()
				self.onScrollingFrameCanvasPositionChanged = nil
			end
		end
	end

	self.onSelected = function(rbx, index)
		if index == self.state.index then
			return
		end

		local scrollingFrameXOffsetCorrection = 0
		if rbx.AbsolutePosition.X < 0 then
			scrollingFrameXOffsetCorrection = rbx.AbsolutePosition.X
		elseif rbx.AbsolutePosition.X + rbx.AbsoluteSize.X > self.state.frameWidth then
			scrollingFrameXOffsetCorrection = (rbx.AbsolutePosition.X + rbx.AbsoluteSize.X) - self.state.frameWidth
		end

		self:setState({
			selectedTabIndex = index,
			autoScroll = scrollingFrameXOffsetCorrection ~= 0,
			scrollingFrameXOffset = self.state.scrollingFrameXOffset + scrollingFrameXOffsetCorrection,
		})
	end
end

function TabBarView:render()
    local tabs = self.props.tabs or {}
	if #tabs <= 0 then
		warn(NO_TABS)
		return nil
	end

	local backgroundColor = self.props.BackgroundColor
	local buttonTextColor = self.props.ButtonTextColor
	local buttonTextFont = self.props.ButtonTextFont
	local buttonTextSize = self.props.ButtonTextSize
	local dropsShadowHeight = self.props.DropsShadowHeight
	local formFactor = self.props.FormFactor or Device.FormFactor.PHONE
	local indicatorColor = self.props.IndicatorColor
	local indicatorHeight = self.props.IndicatorHeight
	local precision = self.props.Precision
	local selectedTabIndex = self.state.selectedTabIndex
	local springStiffness = self.props.SpringStiffness
	local springDamping = self.props.SpringDamping
	local tabBarButtonColor = self.props.TabBarButtonColor
	local tabBarButtonMinimumWidth = self.props.TabBarButtonMinimumWidth
	local tabBarButtonPadding = self.props.TabBarButtonPadding
	local tabBarHeight = self.props.TabBarHeight

	local tarBarContentWidth = 0

	local tabBarButtons = {}
    tabBarButtons["Layout"] = Roact.createElement("UIListLayout", {
        FillDirection = Enum.FillDirection.Horizontal,
        VerticalAlignment = Enum.VerticalAlignment.Center,
    })
    for index, tab in ipairs(tabs) do
        local buttonWidth = getButtonWidth(formFactor, tab.title, buttonTextFont, buttonTextSize,
				tabBarButtonMinimumWidth, tabBarButtonPadding, self.state.frameWidth)
        tarBarContentWidth = buttonWidth + tarBarContentWidth

        tabBarButtons[index] = Roact.createElement("Frame", {
            BackgroundColor3 = tabBarButtonColor,
			BorderSizePixel = 0,
			Size = UDim2.new(0, buttonWidth, 0, tabBarHeight),
        },{
            Roact.createElement("TextButton", {
				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				Font = buttonTextFont,
				Size = UDim2.new(1, 0, 1, 0),
				Text = tab.title,
				TextColor3 = buttonTextColor,
				TextSize = buttonTextSize,

				[Roact.Event.Activated] = function(rbx)
					self.onSelected(rbx, index)
				end
			}),

            Indicator = selectedTabIndex == index and Roact.createElement("Frame", {
				BackgroundColor3 = indicatorColor,
				Size = UDim2.new(1, 0, 0, indicatorHeight),
				BorderSizePixel = 0,
				AnchorPoint = Vector2.new(0, 1),
				Position = UDim2.new(0, 0, 1, 0),
			}),
        })
    end

    local scrollFrameWidth = (tarBarContentWidth < self.state.frameWidth)
								and tarBarContentWidth
								or self.state.frameWidth

	if tabs[selectedTabIndex].content.component == nil then
		warn(NO_CONTENT)
		return nil
	end

	tabs[selectedTabIndex].content.options.frameHeight = self.state.frameHeight
    return Roact.createElement("Frame", {
		BackgroundColor3 = backgroundColor,
		BorderSizePixel = 0,
        Size = UDim2.new(1, 0, 1, 0),

		[Roact.Ref] = self.onRef,
    }, {
        Layout = Roact.createElement("UIListLayout", {
            FillDirection = Enum.FillDirection.Vertical,
            SortOrder = Enum.SortOrder.LayoutOrder,
        }),

        TabBarMenusContainer = Roact.createElement("Frame", {
            BackgroundColor3 = tabBarButtonColor,
			BorderSizePixel = 0,
			LayoutOrder = 1,
			Size = UDim2.new(1, 0, 0, tabBarHeight),
        }, {
			TabBarMenus = Roact.createElement(RoactMotion.SimpleMotion, {
				style = {
					offsetX = RoactMotion.spring(self.state.scrollingFrameXOffset, springStiffness, springDamping, precision),
				},

				render = function (values)
					local canvasPositionX = self.state.autoScroll and values.offsetX or self.state.scrollingFrameXOffset
					return Roact.createElement("ScrollingFrame", {
						AnchorPoint = Vector2.new(0.5, 0),
						BackgroundTransparency = 1,
						BorderSizePixel = 0,
						CanvasSize = UDim2.new(0, tarBarContentWidth, 0, tabBarHeight),
						CanvasPosition = Vector2.new(canvasPositionX, 0),
						ClipsDescendants = true,
						Position = UDim2.new(0.5, 0, 0, 0),
						ScrollBarThickness = 0,
						Size = UDim2.new(0, scrollFrameWidth, 1, 0),
						[Roact.Ref] = self.onScrollingFrameRef,
					}, tabBarButtons)
				end
			})
        }),

        ContentContainer = Roact.createElement("Frame", {
            BackgroundColor3 = DEFAULT_BACKGROUND_COLOR,
			BorderSizePixel = 0,
			LayoutOrder = 2,
			Size = UDim2.new(1, 0, 1, -tabBarHeight),
        }, {
			Content = Roact.createElement(tabs[selectedTabIndex].content.component,
					tabs[selectedTabIndex].content.options),

			DropsShadow = Roact.createElement("ImageLabel", {
				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				Image = DROPS_SHADOW_IMAGE,
				Size = UDim2.new(1, 0, 0, dropsShadowHeight),
			}),
        })
    })
end

return RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			FormFactor = state.FormFactor,
		}
	end
)(TabBarView)
