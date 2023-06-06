local CoreGui = game:GetService("CoreGui")
local Actions = CoreGui.RobloxGui.Modules.Shell.Actions
local Common = CoreGui.RobloxGui.Modules.Common

local InsertScreen = require(Actions.InsertScreen)
local RemoveScreen = require(Actions.RemoveScreen)

local Immutable = require(Common.Immutable)

return function(state, action)
	state = state or {}

	if action.type == InsertScreen.name then
		local newList = Immutable.Append(state, action.item)

		table.sort(newList, function(item1, item2)
			if item1.priority == item2.priority then
				return item1.createdAt > item2.createdAt
			end

			return item1.priority > item2.priority
		end)

		return newList
	elseif action.type == RemoveScreen.name then
		return Immutable.RemoveValueFromList(state, action.item)
	end

	return state
end
