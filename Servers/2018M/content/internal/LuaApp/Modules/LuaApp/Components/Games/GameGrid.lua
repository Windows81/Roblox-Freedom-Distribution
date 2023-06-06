local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)

local Constants = require(Modules.LuaApp.Constants)
local getGameCardSize = require(Modules.LuaApp.getGameCardSize)

local GameCard = require(Modules.LuaApp.Components.Games.GameCard)

local CARD_MARGIN = Constants.GAME_GRID_CHILD_PADDING

local GameGrid = Roact.PureComponent:extend("GameGrid")

function GameGrid:init()
	self.state = {
		cardSize = Vector2.new(0, 0),
		cardsPerRow = 0,
		cardWindowStart = 1,
	}

	self.containerRef = Roact.createRef()

	self.isMounted = false

	self.updateCardWindowBounds = function()
		if not self.containerRef.current then
			return
		end

		local windowSize = self.props.windowSize
		local windowOffSet = -self.containerRef.current.AbsolutePosition.Y

		local newCardSize, newCardsPerRow = getGameCardSize(windowSize.X, 0, CARD_MARGIN, 0)
		local topInvisibleRows = math.max(0, math.floor(windowOffSet / (newCardSize.Y + CARD_MARGIN)))
		local newCardWindowStart = math.max(1, topInvisibleRows * newCardsPerRow + 1)

		local shouldUpdate = newCardSize ~= self.state.cardSize
			or newCardsPerRow ~= self.state.cardsPerRow
			or newCardWindowStart ~= self.state.cardWindowStart

		if shouldUpdate then
			-- QuantumGui bug: when using AbsolutePosition to trigger windowing,
			-- elements do not get updated correctly because the windowing is
			-- happening during a UILayout. This can be temporarly fixed by
			-- delaying the windowing for 1 frame.
			delay(0, function()
				if self.isMounted then
					self:setState({
						cardSize = newCardSize,
						cardsPerRow = newCardsPerRow,
						cardWindowStart = newCardWindowStart,
					})
				end
			end)
		end
	end
end

function GameGrid:render()
	local entries = self.props.entries
	local layoutOrder = self.props.LayoutOrder
	local numberOfRowsToShow = self.props.numberOfRowsToShow
	local reportGameDetailOpened = self.props.reportGameDetailOpened
	local windowSize = self.props.windowSize

	local cardSize = self.state.cardSize
	local cardsPerRow = self.state.cardsPerRow
	local cardWindowStart = self.state.cardWindowStart

	local totalRows = math.ceil(#entries / cardsPerRow)

	if numberOfRowsToShow ~= nil then
		totalRows = math.min(totalRows, numberOfRowsToShow)
	end

	local totalHeight = math.max(0, cardSize.Y * totalRows + CARD_MARGIN * (totalRows - 1))

	local cardsInWindow = (math.ceil(windowSize.Y / (cardSize.Y + CARD_MARGIN)) + 1) * cardsPerRow
	local cardWindowEnd = math.min(#entries, totalRows * cardsPerRow, cardWindowStart + cardsInWindow - 1)
	local topPadding = (cardWindowStart - 1) / cardsPerRow * (cardSize.Y + CARD_MARGIN)

	local gameCards = {
		Layout = Roact.createElement("UIGridLayout", {
			CellPadding = UDim2.new(0, CARD_MARGIN, 0, CARD_MARGIN),
			CellSize = UDim2.new(0, cardSize.X, 0, cardSize.Y),
			FillDirection = Enum.FillDirection.Horizontal,
			HorizontalAlignment = Enum.HorizontalAlignment.Center,
			SortOrder = Enum.SortOrder.LayoutOrder,
		}),
	}

	for index = cardWindowStart, cardWindowEnd do
		local entry = entries[index]
		local key = index % cardsInWindow

		gameCards[key] = Roact.createElement(GameCard, {
			entry = entry,
			size = cardSize,
			index = index,
			reportGameDetailOpened = reportGameDetailOpened,
			layoutOrder = index,
		})
	end

	return Roact.createElement("Frame", {
		-- There's a bug in UIGridLayout that, sometimes although the size
		-- fit perfectly, it would fit 1 element less than desired...
		-- This can be fixed with flags:
		--    FFlagQuantumGui and FFlagRoundInAdorn
		-- However since QuantumGui is not on for now, we will fix this
		-- by giving 1 extra pixel to the width of the grid.
		Size = UDim2.new(1, 1, 0, totalHeight),
		LayoutOrder = layoutOrder,
		BackgroundTransparency = 1,
		[Roact.Ref] = self.containerRef,
		[Roact.Change.AbsolutePosition] = self.updateCardWindowBounds,
	}, {
		-- There's some QuantumGui bug with UIPadding. So we're using Position
		-- for the padding.
		Roact.createElement("Frame", {
			Size = UDim2.new(1, 0, 1, 0),
			Position = UDim2.new(0, 0, 0, topPadding),
			BackgroundTransparency = 1,
		}, gameCards)
	})
end

function GameGrid:didMount()
	self.isMounted = true
	self.updateCardWindowBounds()
end

function GameGrid:willUnmount()
	self.isMounted = false
end

function GameGrid:didUpdate(prevProps)
	if self.props.windowSize ~= prevProps.windowSize then
		self.updateCardWindowBounds()
	end
end

return GameGrid