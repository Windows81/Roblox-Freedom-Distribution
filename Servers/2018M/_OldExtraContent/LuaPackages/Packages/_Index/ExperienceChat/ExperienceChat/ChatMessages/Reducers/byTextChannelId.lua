local ProjectRoot = script:FindFirstAncestor("ExperienceChat").Parent
local Rodux = require(ProjectRoot.Rodux)
local Dictionary = require(ProjectRoot.llama).Dictionary
local List = require(ProjectRoot.llama).List

return Rodux.createReducer({}, {
	SendChatMessage = function(state: table, action: table): table
		local entry = state[action.textChannelId]
		if entry then
			-- check if message with messageId is already in the entry
			if not List.find(entry, action.messageId) then
				entry = List.append(entry, action.messageId)
			end
		else
			entry = { action.messageId }
		end

		return Dictionary.join(state, {
			[action.textChannelId] = entry,
		})
	end,
})
