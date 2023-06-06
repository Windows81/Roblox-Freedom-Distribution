local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Immutable = require(Modules.Common.Immutable)

local SetTopBarHeight = require(Modules.LuaApp.Actions.SetTopBarHeight)

local Constants = require(Modules.LuaApp.Constants)

return function(state, action)
	state = state or {
		topBarHeight = Constants.TOP_BAR_SIZE,
	}

	if action.type == SetTopBarHeight.name then
		if state.topBarHeight ~= action.topBarHeight then
			local newProperties = {
				topBarHeight = action.topBarHeight,
			}
			state = Immutable.JoinDictionaries(state, newProperties)
		end
	end

	return state
end