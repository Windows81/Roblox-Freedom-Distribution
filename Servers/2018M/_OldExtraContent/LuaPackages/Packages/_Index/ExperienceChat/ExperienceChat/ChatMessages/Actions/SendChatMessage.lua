local ProjectRoot = script:FindFirstAncestor("ExperienceChat").Parent
local Rodux = require(ProjectRoot.Rodux)

return Rodux.makeActionCreator(
	script.Name,
	function(textChannelId: string, messageId: string, prefixText: string, text: string): table
		return {
			textChannelId = textChannelId,
			messageId = messageId,
			prefixText = prefixText,
			text = text,
		}
	end
)
