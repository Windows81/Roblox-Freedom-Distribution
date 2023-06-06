local Modules = game:GetService("CoreGui").RobloxGui.Modules

local Roact = require(Modules.Common.Roact)
local RoactRodux = require(Modules.Common.RoactRodux)

local Constants = require(Modules.LuaApp.Constants)

local TopBar = require(Modules.LuaApp.Components.TopBar)
local GamesSearch = require(Modules.LuaApp.Components.Search.GamesSearch)

local ComponentMap = {
	[Constants.SearchTypes.Games] = GamesSearch,
	-- [Constants.SearchTypes.Groups] = GroupsSearch,
	-- [Constants.SearchTypes.Players] = PlayersSearch,
	-- [Constants.SearchTypes.Catalog] = CatalogSearch,
	-- [Constants.SearchTypes.Library] = LibrarySearch,
}

local SearchPage = Roact.PureComponent:extend("SearchPage")

SearchPage.defaultProps = {
	searchType = Constants.SearchTypes.Games,
}

function SearchPage:render()
	local topBarHeight = self.props.topBarHeight
	local searchUuid = self.props.searchUuid
	local searchType = self.props.searchType

	return Roact.createElement("Frame", {
		Size = UDim2.new(1, 0, 1, 0),
		BorderSizePixel = 0,
	},{
		TopBar = Roact.createElement(TopBar, {
			ZIndex = 2,
			showBackButton = true,
			showBuyRobux = true,
			showNotifications = true,
			showSearch = true,
		}),
		SearchPage = Roact.createElement("Frame", {
			BackgroundColor3 = Constants.Color.GRAY4,
			Position = UDim2.new(0, 0, 0, topBarHeight),
			Size = UDim2.new(1, 0, 1, -topBarHeight),
		}, {
			Roact.createElement(ComponentMap[searchType], {
				searchUuid = searchUuid,
			})
		})
	})
end

SearchPage = RoactRodux.UNSTABLE_connect2(
	function(state, props)
		return {
			topBarHeight = state.TopBar.topBarHeight,
		}
	end
)(SearchPage)

return SearchPage