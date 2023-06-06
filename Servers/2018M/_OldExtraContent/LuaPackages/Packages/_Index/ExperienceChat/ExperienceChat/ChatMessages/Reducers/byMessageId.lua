local ProjectRoot = script:FindFirstAncestor("ExperienceChat").Parent
local Rodux = require(ProjectRoot.Rodux)
local Dictionary = require(ProjectRoot.llama).Dictionary

return Rodux.createReducer({}, {
	SendChatMessage = function(state: table, action: table): table
		return Dictionary.joinDeep(state, {
			[action.messageId] = {
				PrefixText = action.prefixText,
				Text = action.text,
			},
		})
	end,
})
