local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Roact = require(Modules.Common.Roact)
local Constants = require(Modules.LuaApp.Constants)
local LocalizedTextBox = require(Modules.LuaApp.Components.LocalizedTextBox)
local LocalizedTextButton = require(Modules.LuaApp.Components.LocalizedTextButton)

local SEARCH_BAR_HEIGHT = 28
local SEARCH_BAR_PADDING = 12
local SEARCH_BAR_TEXT_SIZE = 20
local SEARCH_BAR_ICON_PADDING = 9
local SEARCH_BAR_TEXT_PADDING_WITH_ICON = 36
local SEARCH_BAR_TEXT_PADDING_WITHOUT_ICON = 12
local CLEAR_IMAGE_SIZE = 16
local CLEAR_IMAGE_PADDING = 6
local CLEAR_BUTTON_SIZE = CLEAR_IMAGE_PADDING*2 + CLEAR_IMAGE_SIZE
local CANCEL_BUTTON_WIDTH = 88
local CANCEL_TEXT_SIZE = 23
local SEARCH_BAR_FONT = Enum.Font.SourceSans
local SEARCH_FRAME_IMAGE = "rbxasset://textures/ui/LuaApp/9-slice/gr-search.png"
local SEARCH_BAR_ICON = "rbxasset://textures/ui/LuaApp/icons/ic-search.png"
local CLEAR_BUTTON_IMAGE = "rbxasset://textures/ui/LuaApp/icons/ic-clear.png"

local SearchBar = Roact.PureComponent:extend("SearchBar")

SearchBar.defaultProps = {
	Size = UDim2.new(1, 0, 1, 0),
}

function SearchBar:init()
	self.state = {
		clearButtonVisible = false
	}
	self.searchBoxRef = Roact.createRef()
	self.searchBoxTextChangedConn = nil

	self.onFocused = function()
		if self.props.onFocused then
			self.props.onFocused()
		end
		if self.searchBoxRef.current and not self.searchBoxTextChangedConn then
			self.searchBoxTextChangedConn = self.searchBoxRef.current:GetPropertyChangedSignal("Text"):Connect(function()
				if self.searchBoxRef.current then
					local clearButtonVisible = self.searchBoxRef.current.Text ~= ""
					if clearButtonVisible ~= self.state.clearButtonVisible then
						self:setState({
							clearButtonVisible = clearButtonVisible
						})
					end
				end
			end)
		end
	end

	self.onFocusLost = function(rbx, enterPressed)
		if enterPressed then
			self.props.confirmSearch(rbx.Text)
		end
	end

	self.onCancelButtonActivated = self.props.cancelSearch

	self.onClearText = function()
		if self.searchBoxRef.current then
			self.searchBoxRef.current.Text = ""
			self.searchBoxRef.current:captureFocus()
		end
	end
end

function SearchBar:didMount()
	if self.props.isPhone and self.searchBoxRef.current then
		self.searchBoxRef.current:captureFocus()
	end
end

function SearchBar:render()
	local size = self.props.Size
	local isPhone = self.props.isPhone
	local clearButtonVisible = self.state.clearButtonVisible
	local searchTextOffset = isPhone and SEARCH_BAR_TEXT_PADDING_WITHOUT_ICON or SEARCH_BAR_TEXT_PADDING_WITH_ICON
	local searchBoxMargin = clearButtonVisible and searchTextOffset + CLEAR_BUTTON_SIZE or searchTextOffset

	return Roact.createElement("Frame", {
		Size = size,
		BackgroundTransparency = 1,
		BorderSizePixel = 0,
	},{
		Layout = isPhone and Roact.createElement("UIListLayout", {
			FillDirection = Enum.FillDirection.Horizontal,
			HorizontalAlignment = Enum.HorizontalAlignment.Right,
			SortOrder = Enum.SortOrder.LayoutOrder,
			VerticalAlignment = Enum.VerticalAlignment.Center,
		}),
		SearchBoxBackground = Roact.createElement("ImageLabel",{
			AnchorPoint = Vector2.new(0, 0.5),
			Size = UDim2.new(1, isPhone and -SEARCH_BAR_PADDING - CANCEL_BUTTON_WIDTH or 0, 0, SEARCH_BAR_HEIGHT),
			Position = UDim2.new(0, 0, 0.5, 0),
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Image = SEARCH_FRAME_IMAGE,
			ScaleType = Enum.ScaleType.Slice,
			SliceCenter = Rect.new(14, 14, 14, 14),
			LayoutOrder = 1,
		},{
			SearchIcon = not isPhone and Roact.createElement("ImageLabel",{
				Size = UDim2.new(0, SEARCH_BAR_TEXT_SIZE, 0, SEARCH_BAR_TEXT_SIZE),
				Position = UDim2.new(0, SEARCH_BAR_ICON_PADDING, 0.5, 0),
				Image = SEARCH_BAR_ICON,
				BackgroundTransparency = 1,
				AnchorPoint = Vector2.new(0, 0.5),
				ImageColor3 = Constants.Color.GRAY2,
			}),
			SearchBox = Roact.createElement(LocalizedTextBox, {
				Size = UDim2.new(1, -searchBoxMargin, 1, 0),
				Position = UDim2.new(0, searchTextOffset, 0.5, 0),
				AnchorPoint = Vector2.new(0, 0.5),
				BackgroundTransparency = 1,
				BorderSizePixel = 0,
				Text = "",
				TextWrapped = true,
				TextXAlignment = Enum.TextXAlignment.Left,
				TextSize = SEARCH_BAR_TEXT_SIZE,
				Font = SEARCH_BAR_FONT,
				PlaceholderText = "Search.GlobalSearch.Example.SearchGames",
				PlaceholderColor3 = Constants.Color.GRAY2,
				OverlayNativeInput = true,
				ClearTextOnFocus = false,
				LayoutOrder = 1,
				[Roact.Ref] = self.searchBoxRef,
				[Roact.Event.FocusLost] = self.onFocusLost,
				[Roact.Event.Focused] = self.onFocused,
			}),
			ClearButton = Roact.createElement("ImageButton", {
				AnchorPoint = Vector2.new(1, 0.5),
				Size = UDim2.new(0, CLEAR_BUTTON_SIZE, 1, 0),
				Position = UDim2.new(1, 0, 0.5, 0),
				BackgroundTransparency = 1,
				Visible = clearButtonVisible,
				[Roact.Event.Activated] = self.onClearText,
			}, {
				ClearImage = Roact.createElement("ImageLabel", {
					AnchorPoint = Vector2.new(1, 0.5),
					Size = UDim2.new(0, CLEAR_IMAGE_SIZE, 0, CLEAR_IMAGE_SIZE),
					Position = UDim2.new(1, -CLEAR_IMAGE_PADDING, 0.5, 0),
					Image = CLEAR_BUTTON_IMAGE,
					BackgroundTransparency = 1,
				}),
			}),
		}),
		CancelButton = isPhone and Roact.createElement(LocalizedTextButton, {
			Size = UDim2.new(0, CANCEL_BUTTON_WIDTH, 1, 0),
			BackgroundTransparency = 1,
			BorderSizePixel = 0,
			Font = SEARCH_BAR_FONT,
			Text = "Feature.GamePage.LabelCancelField",
			TextSize = CANCEL_TEXT_SIZE,
			TextColor3 = Constants.Color.WHITE,
			LayoutOrder = 2,
			[Roact.Event.Activated] = self.onCancelButtonActivated,
		}),
	})
end

return SearchBar