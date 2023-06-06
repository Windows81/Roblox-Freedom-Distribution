local CoreGui = game:GetService("CoreGui")
local Modules = CoreGui.RobloxGui.Modules

local FormFactor = require(Modules.LuaApp.Enum.FormFactor)

local DialogInfo = {}

DialogInfo.Intent = {
	BrowseGames = "BrowseGames",
	ConversationHub = "ConversationHub",
	Conversation = "Conversation",
	GroupDetail = "GroupDetail",
	NewChatGroup = "NewChatGroup",
	CreateChat = "CreateChat",
	EditChatGroup = "EditChatGroup",
	EditGroupName = "EditGroupName",
	ParticipantOptions = "ParticipantOptions",
	RemoveUser = "RemoveUser",
	LeaveGroup = "LeaveGroup",
	DefaultScreen = "DefaultScreen",
	GenericDialog = "GenericDialog",
	GameShare = "GameShare",
}

DialogInfo.DialogType = {
	Centered = "Centered",
	Left = "Left",
	Right = "Right",
	Modal = "Modal",
	Popup = "Popup",
}

DialogInfo.DialogTypeMap = {
	[FormFactor.PHONE] = {
		[DialogInfo.Intent.BrowseGames] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.ConversationHub] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.Conversation] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.GroupDetail] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.NewChatGroup] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.CreateChat] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.EditChatGroup] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.EditGroupName] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.ParticipantOptions] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.RemoveUser] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.LeaveGroup] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.DefaultScreen] = DialogInfo.DialogType.Centered,
		[DialogInfo.Intent.GenericDialog] = DialogInfo.DialogType.Popup,
		[DialogInfo.Intent.GameShare] = DialogInfo.DialogType.Popup,
	},
	[FormFactor.TABLET] = {
		[DialogInfo.Intent.BrowseGames] = DialogInfo.DialogType.Modal,
		[DialogInfo.Intent.ConversationHub] = DialogInfo.DialogType.Left,
		[DialogInfo.Intent.Conversation] = DialogInfo.DialogType.Right,
		[DialogInfo.Intent.GroupDetail] = DialogInfo.DialogType.Right,
		[DialogInfo.Intent.NewChatGroup] = DialogInfo.DialogType.Modal,
		[DialogInfo.Intent.CreateChat] = DialogInfo.DialogType.Modal,
		[DialogInfo.Intent.EditChatGroup] = DialogInfo.DialogType.Modal,
		[DialogInfo.Intent.EditGroupName] = DialogInfo.DialogType.Right,
		[DialogInfo.Intent.ParticipantOptions] = DialogInfo.DialogType.Right,
		[DialogInfo.Intent.RemoveUser] = DialogInfo.DialogType.Right,
		[DialogInfo.Intent.LeaveGroup] = DialogInfo.DialogType.Right,
		[DialogInfo.Intent.DefaultScreen] = DialogInfo.DialogType.Right,
		[DialogInfo.Intent.GenericDialog] = DialogInfo.DialogType.Popup,
		[DialogInfo.Intent.GameShare] = DialogInfo.DialogType.Popup,
	},
}

function DialogInfo.GetTypeBasedOnIntent(formFactor, intent)
	local formFactorTypeMap = DialogInfo.DialogTypeMap[formFactor]
	local dialogType = formFactorTypeMap[intent]

	if not dialogType then
		return DialogInfo.DialogType.Centered
	end

	return dialogType
end

return DialogInfo
