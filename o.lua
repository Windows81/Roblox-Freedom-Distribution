local t = {
	"./Roblox/v463/Player/Content/avatar/character.rbxm",
	"./Roblox/v463/Player/Content/avatar/characterCaged.rbxm",
	"./Roblox/v463/Player/Content/avatar/characterCagedHSR.rbxm",
	"./Roblox/v463/Player/Content/avatar/characterCagedHSRV17-fixed-WrapTargets.rbxm",
	"./Roblox/v463/Player/Content/avatar/characterCagedHSRV17.rbxm",
	"./Roblox/v463/Player/Content/avatar/characterCagedHSRV18.rbxm",
	"./Roblox/v463/Player/Content/avatar/characterR15.rbxm",
	"./Roblox/v463/Player/Content/avatar/characterR15V2.rbxm",
	"./Roblox/v463/Player/Content/avatar/characterR15V3.rbxm",
	"./Roblox/v463/Player/Content/avatar/characterR15V4.rbxm",
	"./Roblox/v463/Player/Content/avatar/characterR15V5.rbxm",
	"./Roblox/v463/Player/Content/avatar/defaultDynamicHead.rbxm",
	"./Roblox/v463/Player/Content/avatar/defaultDynamicHeadV2.rbxm",
	"./Roblox/v463/Player/Content/avatar/defaultPants.rbxm",
	"./Roblox/v463/Player/Content/avatar/defaultShirt.rbxm",
}
print(#t)
for _, a in next, t do
	print(a)
	local b = a .. ".bak"
	local c = a .. "x"
	fs.rename(a, b)
	local v = fs.read(b, "rbxm")
	fs.write(a, v, "rbxmx")
end
