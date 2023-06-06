-- Avatar_R15_Action v1.1.0
-- For R6, this generates the normal with/without gear pose.  For R15 it positions their body in an action pose.
baseUrl, characterAppearanceUrl, fileExtension, x, y = ...

pcall(function() game:GetService("ContentProvider"):SetBaseUrl(baseUrl) end)
game:GetService("ScriptContext").ScriptsDisabled = true

local player = game:GetService("Players"):CreateLocalPlayer(0)
player.CharacterAppearance = characterAppearanceUrl
player:LoadCharacterBlocking()

local poseAnimationId = "http://www.roblox.com/asset/?id=532421348"

local function getJointBetween(part0, part1)
    for _, obj in pairs(part1:GetChildren()) do
        if obj:IsA("Motor6D") and obj.Part0 == part0 then
            return obj
        end
    end
end

local function applyKeyframe(character, poseKeyframe)
    local function recurApplyPoses(parentPose, poseObject)
        if parentPose then
            local joint = getJointBetween(character[parentPose.Name], character[poseObject.Name])
            if joint and poseObject.Weight ~= 0 then
                joint.C1 = poseObject.CFrame:inverse() + joint.C1.p
            end
        end
        for _, subPose in pairs(poseObject:GetSubPoses()) do
            recurApplyPoses(poseObject, subPose)
        end
    end

    for _, poseObj in pairs(poseKeyframe:GetPoses()) do
        recurApplyPoses(nil, poseObj)
    end
end

local function applyR15Pose(character)
    local poseKeyframSequence = game:GetService("KeyframeSequenceProvider"):GetKeyframeSequence(poseAnimationId)
    local poseKeyframe = poseKeyframSequence:GetKeyframes()[1]
    
	applyKeyframe(character, poseKeyframe)
end

local function findAttachmentsRecur(parent, resultTable, returnDictionary)
    for _, obj in pairs(parent:GetChildren()) do
        if obj:IsA("Attachment") then
            if returnDictionary then
                resultTable[obj.Name] = obj
            else
                resultTable[#resultTable + 1] = obj
            end
        elseif not obj:IsA("Tool") and not obj:IsA("Accoutrement") then -- Leave out tools and accoutrements in the character
            findAttachmentsRecur(obj, resultTable, returnDictionary)
        end
    end
end

local function findAttachmentsInTool(tool)
    local attachments = {}
    findAttachmentsRecur(tool, attachments, false)
    return attachments
end

local function findAttachmentsInCharacter(character)
    local attachments = {}
    findAttachmentsRecur(character, attachments, true)
    return attachments
end

local function weldAttachments(attach1, attach2)
    local weld = Instance.new("Weld")
    weld.Part0 = attach1.Parent
    weld.Part1 = attach2.Parent
    weld.C0 = attach1.CFrame
    weld.C1 = attach2.CFrame
    weld.Parent = attach1.Parent
    return weld
end

function findFirstMatchingAttachment(model, name)
    for _, child in pairs(model:GetChildren()) do
        if child:IsA("Attachment") and child.Name == name then
            return child
        elseif not child:IsA("Accoutrement") and not child:IsA("Tool") then
            local foundAttachment = findFirstMatchingAttachment(child, name)
            if foundAttachment then
                return foundAttachment
            end
        end
    end
end

local function doR15ToolPose(character, humanoid, tool)
    local characterAttachments = findAttachmentsInCharacter(character)
    local toolAttachments = findAttachmentsInTool(tool)
    local foundAttachments = false
    -- If matching attachments exist in the gear then weld them and do the "action" R15 pose.
    -- Otherwise keep the R15 in the T-Pose position and just raise the arm.
    for _, attachment in pairs(toolAttachments) do
        local matchingAttachment = characterAttachments[attachment.Name]
        if matchingAttachment then
            foundAttachments = true
            weldAttachments(matchingAttachment, attachment)
        end
    end
    
    if foundAttachments then
        tool.Parent = character
        applyR15Pose(character)

		local toolPose = tool:FindFirstChild("ThumbnailPose")
		if toolPose and toolPose:IsA("Keyframe") then
			applyKeyframe(character, toolPose)
		end
    else
        tool.Parent = nil
        local rightShoulderJoint = getJointBetween(character.UpperTorso, character.RightUpperArm)
        if rightShoulderJoint then
            rightShoulderJoint.C1 = rightShoulderJoint.C1 *  CFrame.new(0, 0, 0, 1, 0, 0, 0, 0, -1, 0, 1, 0):inverse()
        end
        if tool:FindFirstChild("Handle") then
            local attachment = findFirstMatchingAttachment(character, "RightGripAttachment")
            if attachment then
                tool.Handle.CFrame = attachment.Parent.CFrame * attachment.CFrame * tool.Grip:inverse()
            end
        end
        humanoid:EquipTool(tool)
    end
end

local character = player.Character
if character then
    local tool = character:FindFirstChildOfClass("Tool")
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    local animateScript = character:FindFirstChild("Animate")
    if animateScript then
        local equippedPoseValue = animateScript:FindFirstChild("Pose") or animateScript:FindFirstChild("pose")
        if equippedPoseValue then
            local poseAnim = equippedPoseValue:FindFirstChildOfClass("Animation")
            if poseAnim then
                poseAnimationId = poseAnim.AnimationId
            end
        end
    end
    
    if humanoid then
        if humanoid.RigType == Enum.HumanoidRigType.R6 then
            if tool then
                character.Torso["Right Shoulder"].CurrentAngle = math.rad(90)
            end
        elseif humanoid.RigType == Enum.HumanoidRigType.R15 then
            if tool then
                doR15ToolPose(character, humanoid, tool)
            else
                applyR15Pose(character)
            end
        end
    end
end

return game:GetService("ThumbnailGenerator"):Click(fileExtension, x, y, --[[hideSky = ]] true)