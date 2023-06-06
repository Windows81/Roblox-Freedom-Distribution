--Avatar_R15_Standard v1.0.1
--Pose R6 characters in the normal way.  For R15, have them in the same pose, and raise their arm up if they have gear.

baseUrl, characterAppearanceUrl, fileExtension, x, y = ...

pcall(function() game:GetService("ContentProvider"):SetBaseUrl(baseUrl) end)
game:GetService("ScriptContext").ScriptsDisabled = true

local player = game:GetService("Players"):CreateLocalPlayer(0)
player.CharacterAppearance = characterAppearanceUrl
player:LoadCharacterBlocking()

local function getJointBetween(part0, part1)
	for _, obj in pairs(part1:GetChildren()) do
		if obj:IsA("Motor6D") and obj.Part0 == part0 then
			return obj
		end
	end
end

local function doR15ToolPose(rig)
	local rightShoulderJoint = getJointBetween(rig.UpperTorso, rig.RightUpperArm)
	if rightShoulderJoint then
		rightShoulderJoint.C1 = rightShoulderJoint.C1 * CFrame.new(0, 0, 0, 1, 0, 0, 0, 0, -1, 0, 1, 0):inverse()
	end
end

-- Raise right arm up to hold gear.
local character = player.Character
if character then
    if character:FindFirstChildOfClass("Tool") then
        local humanoid = character:FindFirstChildOfClass("Humanoid")
        if humanoid then
            if humanoid.RigType == Enum.HumanoidRigType.R6 then
                character.Torso['Right Shoulder'].CurrentAngle = math.rad(90)
            elseif humanoid.RigType == Enum.HumanoidRigType.R15 then			
				doR15ToolPose(character)
            end
        end
    end
end

return game:GetService('ThumbnailGenerator'):Click(fileExtension, x, y, --[[hideSky = ]] true)