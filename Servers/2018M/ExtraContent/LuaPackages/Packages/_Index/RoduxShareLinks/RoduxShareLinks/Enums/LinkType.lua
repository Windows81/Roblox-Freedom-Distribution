local Packages = script.Parent.Parent.Parent
local enumerate = require(Packages.enumerate)

return enumerate(script.Name, {
	Unset = "Unset",
	ExperienceInvite = "ExperienceInvite",
	FriendInvite = "FriendInvite",
})
