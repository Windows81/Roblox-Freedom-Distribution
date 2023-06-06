-- Package v1.1.6
-- See http://wiki.roblox.com/index.php?title=R15_Compatibility_Guide#Package_Parts for details on how body parts work with R15

local assetUrls, baseUrl, fileExtension, x, y, R6RigUrl, customTextureUrls = ...
local R15RigUrl = "http://www.roblox.com/Asset/?id=516159357" 

pcall(function() game:GetService("ContentProvider"):SetBaseUrl(baseUrl) end) 
game:GetService("ScriptContext").ScriptsDisabled = true

function split(str, delim)
    local results = {}
    local lastMatchEnd = 0
    
    local matchStart, matchEnd = string.find(str, delim, --[[init = ]] 1, --[[plain = ]] true)
    while matchStart and matchEnd do
        if matchStart - lastMatchEnd > 1 then
            table.insert(results, string.sub(str, lastMatchEnd + 1, matchStart - 1))
        end

        lastMatchEnd = matchEnd
        matchStart, matchEnd = string.find(str, delim, --[[init = ]] lastMatchEnd + 1, --[[plain = ]] true)
    end

    if string.len(str) - lastMatchEnd > 1 then
        table.insert(results, string.sub(str, lastMatchEnd + 1))
    end
    return results
end

local R15Assets = {}
local R6Assets = {}
local bothAssets = {}

local useR15 = true
local poseAnimationId = nil

local poseValueFound = false
local function processR15Anim(animFolder)
	local function processStrValue(strValue)
		local animation = strValue:FindFirstChildOfClass("Animation")
		if not animation then
			return
		end
		
		-- By default the pose animation will be used for the thumbnail
		-- If the pose animation doesn't exist then the idle will be used, otherwise the first animation will be used.
		if string.lower(strValue.Name) == "pose" then
			poseValueFound = true
			poseAnimationId = animation.AnimationId
		elseif not poseValueFound and string.lower(strValue.Name) == "idle" then
			poseAnimationId = animation.AnimationId
		elseif not poseAnimationId then
			poseAnimationId = animation.AnimationId
		end
	end


	for _, obj in pairs(animFolder:GetChildren()) do
		if obj:IsA("StringValue") then
			processStrValue(obj)
		end
    end
end

local assetUrlsList = split(assetUrls, ";")

for _, assetUrl in pairs(assetUrlsList) do
    local currObjects = game:GetObjects(assetUrl)
    
    for _,object in pairs(currObjects) do
        if object:IsA("Folder") and object.Name == "R15" then
            for _, child in pairs(object:GetChildren()) do
                table.insert(R15Assets, child)
            end
        elseif object:IsA("Folder") and object.Name == "R6" then
            foundR6CompatibleParts = true
            for _, child in pairs(object:GetChildren()) do
                table.insert(R6Assets, child)
            end
        elseif object:IsA("CharacterMesh") then
            -- Legacy body part format using a CharacterMesh
            table.insert(R6Assets, object)
        elseif object:IsA("Folder") and object.Name == "R15Anim" then
            processR15Anim(object)
        else
            table.insert(bothAssets, object)
        end		
    end
end

-- if the package doesn't contain animations, use this pose.
poseAnimationId = poseAnimationId or "http://www.roblox.com/asset/?id=532421348"

-- Only use R6 if we found body parts that are only compatible with R15
if #R6Assets ~= 0 and #R15Assets == 0 then
    useR15 = false
end

local mannequin = nil
if useR15 then
    mannequin = game:GetObjects(R15RigUrl)[1]
    for _,obj in pairs(R15Assets) do 
        table.insert(bothAssets, obj)
    end
else
    mannequin = game:GetObjects(R6RigUrl)[1]	
    for _,obj in pairs(R6Assets) do 
        table.insert(bothAssets, obj)
    end
end
mannequin.Humanoid.DisplayDistanceType = Enum.HumanoidDisplayDistanceType.None
mannequin.Parent = workspace

local tool = nil
local accoutrements = {}

for _, currObject in pairs(bothAssets) do
    if currObject:IsA("BasePart") then
        local existingBodyPart = mannequin:FindFirstChild(currObject.Name)
        if existingBodyPart ~= nil then
            existingBodyPart:Destroy()
        end
    end
    
    if currObject:IsA("Tool") then
        if useR15 then 
            tool = currObject
        else
            mannequin.Torso["Right Shoulder"].CurrentAngle = math.rad(90)
            currObject.Parent = mannequin
        end
    elseif currObject:IsA("DataModelMesh") then
        local headMesh = mannequin.Head:FindFirstChild("Mesh")
        if headMesh then
            headMesh:Destroy()
        end
        currObject.Parent = mannequin.Head
    elseif currObject:IsA("Decal") then
        local face = mannequin.Head:FindFirstChild("face")
        if face then
            face:Destroy()
        end
        currObject.Parent = mannequin.Head
    elseif currObject:IsA("Accoutrement") then
        table.insert(accoutrements, currObject)
    else
        currObject.Parent = mannequin
    end    
end

local textureUrls = split(customTextureUrls, ";")
for _, url in pairs(textureUrls) do
    local obj = game:GetObjects(url)[1]
    if obj:IsA("Shirt") then
        -- Don't add a texture Shirt if package already has a Shirt
        if not mannequin:FindFirstChildOfClass("Shirt") then
            obj.Parent = mannequin
        end
    elseif obj:IsA("Pants") then
        -- Don't add a texture Pants if package already has a Pants
        if not mannequin:FindFirstChildOfClass("Pants") then
            obj.Parent = mannequin
        end
    else
        obj.Parent = mannequin
    end
end

local function buildJoint(parentAttachment, partForJointAttachment)
    local jointName = parentAttachment.Name:gsub("RigAttachment", "")
    local motor = partForJointAttachment.Parent:FindFirstChild(jointName)
    if not motor then
        motor = Instance.new("Motor6D")
    end
    motor.Name = jointName
 
    motor.Part0 = parentAttachment.Parent
    motor.Part1 = partForJointAttachment.Parent
 
    motor.C0 = parentAttachment.CFrame
    motor.C1 = partForJointAttachment.CFrame
 
    motor.Parent = partForJointAttachment.Parent
end
 
-- Builds an R15 rig from the attachments in the parts
function buildRigFromAttachments(currentPart, lastPart)
    local validSiblings = {}
    for _, sibling in pairs(currentPart.Parent:GetChildren()) do
        -- Don't find matching attachment in the current part being processed.
        -- Don't visit the last part visited again, this would cause an infinite loop.
        if sibling:IsA("BasePart") and sibling ~= currentPart and sibling ~= lastPart then
            table.insert(validSiblings, sibling)
        end
    end

    local function processRigAttachment(attachment)
        for _, sibling in pairs(validSiblings) do
            local matchingAttachment = sibling:FindFirstChild(attachment.Name)
            if matchingAttachment then
                buildJoint(attachment, matchingAttachment)
                buildRigFromAttachments(matchingAttachment.Parent, currentPart)
            end
        end
    end

    for _, object in pairs(currentPart:GetChildren()) do
        if object:IsA("Attachment") and string.find(object.Name, "RigAttachment") then
            processRigAttachment(object)
        end
    end
end

local function getJointBetween(part0, part1)
    for _, obj in pairs(part1:GetChildren()) do
        if obj:IsA("Motor6D") and obj.Part0 == part0 then
            return obj
        end
    end
end

local function applyR15ToolPose(rig)
    local upperTorso = rig:FindFirstChild("UpperTorso")
    local rightUpperArm = rig:FindFirstChild("RightUpperArm")
    if upperTorso and rightUpperArm then
        local rightShoulderJoint = getJointBetween(upperTorso, rightUpperArm)
        if rightShoulderJoint then
            rightShoulderJoint.C1 = rightShoulderJoint.C1 * CFrame.new(0, 0, 0, 1, 0, 0, 0, 0, -1, 0, 1, 0):inverse()
        end
    end
end

-- Applies the middle keyframe of a pose to a given character.
local function applyPoseToCharacter(character, poseAnimationId)
    local poseKeyframSequence = game:GetService("KeyframeSequenceProvider"):GetKeyframeSequence(poseAnimationId)
    local keyframes = poseKeyframSequence:GetKeyframes()
    local poseKeyframe = keyframes[math.max(1, math.floor(#keyframes/2))]

    local function recurApplyPoses(parentPose, poseObject)
        if parentPose then
            local joint = getJointBetween(character[parentPose.Name], character[poseObject.Name])
            if joint then
                joint.C1 = joint.C1 * poseObject.CFrame:inverse()
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

if useR15 then
    -- Build R15 rig
    local humanoidRootPart = mannequin:WaitForChild("HumanoidRootPart")
    humanoidRootPart.CFrame = CFrame.new(Vector3.new(0, 5, 0)) * CFrame.Angles(0, math.pi, 0)
    humanoidRootPart.Anchored = true
    buildRigFromAttachments(humanoidRootPart)

    if tool then
        applyR15ToolPose(mannequin)

        local hand = mannequin:FindFirstChild("RightHand")
        local handle = tool:FindFirstChild("Handle")
        if hand and handle then
            local handGrip = hand:FindFirstChild("RightGripAttachment")
            if handGrip then
                handle.CFrame = hand.CFrame * handGrip.CFrame * tool.Grip:inverse()
            end
        end
        tool.Parent = mannequin
    elseif poseAnimationId then
        applyPoseToCharacter(mannequin, poseAnimationId)
    end
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

for _, accoutrement in pairs(accoutrements) do
    local handle = accoutrement:FindFirstChild("Handle")
    if handle then
        local accoutrementAttachment = handle:FindFirstChildOfClass("Attachment")
        local characterAttachment = nil
        if accoutrementAttachment then
            characterAttachment = findFirstMatchingAttachment(mannequin, accoutrementAttachment.Name)
        end

        local attachmentPart = nil
        if characterAttachment then
            attachmentPart = characterAttachment.Parent
        else
            attachmentPart = mannequin:FindFirstChild("Head")
        end

        local attachmentCFrame = nil
        if characterAttachment then
            attachmentCFrame = characterAttachment.CFrame
        else
            attachmentCFrame = CFrame.new(0, 0.5, 0)
        end

        local hatCFrame = nil
        if accoutrementAttachment then
            hatCFrame = accoutrementAttachment.CFrame
        else
            hatCFrame = accoutrement.AttachmentPoint
        end

        handle.CFrame = attachmentPart.CFrame * attachmentCFrame * hatCFrame:inverse()
        handle.Anchored = true
        handle.Parent = mannequin
    end
end

return game:GetService("ThumbnailGenerator"):Click(fileExtension, x, y, --[[hideSky = ]] true)