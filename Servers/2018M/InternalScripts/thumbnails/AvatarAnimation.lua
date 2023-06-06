-- AvatarAnimation V 1.0.3
-- Creates a thumbnail from the middle Keyframe of an animation.

-- Example arguments:
-- https://www.sitetest3.robloxlabs.com/Asset/AvatarAccoutrements.ashx?AvatarHash=80dcfa39a8e90f690d2be0e56239abbe&AssetIDs=42900214,32357663,32357631,32357619,32357584,32357558&ResolvedAvatarType=R15, 
-- http://www.sitetest3.robloxlabs.com/, 
-- Png, 
-- 600,
-- 600, 
-- http://www.sitetest3.robloxlabs.com/Asset/?hash=ca005a9e83ac95bd5068029afdc65496 

characterAppearanceUrl, baseUrl, fileExtension, x, y, animationUrl = ...

pcall(function() game:GetService("ContentProvider"):SetBaseUrl(baseUrl) end)
game:GetService("ScriptContext").ScriptsDisabled = true

local player = game:GetService("Players"):CreateLocalPlayer(0)
player.CharacterAppearance = characterAppearanceUrl
player:LoadCharacterBlocking()

local function getJointBetween(part0, part1)
	local foundJoint = nil
	for _, obj in pairs(part1:GetChildren()) do
		if obj:IsA("Motor6D") and obj.Part0 == part0 then
			return obj
		end
	end
end

local function applyR15Pose(character, poseKeyframe)	
	local function recurApplyPoses(parentPose, poseObject)
		if parentPose then
			local joint = getJointBetween(character[parentPose.Name], character[poseObject.Name])
			joint.C1 = joint.C1 * poseObject.CFrame:inverse()
		end
		for _, subPose in pairs(poseObject:GetSubPoses()) do
			recurApplyPoses(poseObject, subPose)
		end
	end

	for _, poseObj in pairs(poseKeyframe:GetPoses()) do
		recurApplyPoses(nil, poseObj)
	end
end

local animationObjects = game:GetObjects(animationUrl)

local poseAnimation = nil
local animations = {}
local rotateCharacter = false
local thumbnailCamera = nil

local function getAnimations(model)
	for _, child in pairs(model:GetChildren()) do
		if child:IsA("Animation") then
			if string.lower(model.Name) == "pose" then
				poseAnimation = child
			else
				table.insert(animations, child)
			end
		else
			getAnimations(child)
		end
		
		if child:IsA("Camera") and child.Name == "ThumbnailCamera" then
			thumbnailCamera = child:Clone()
		end
		
		if child:IsA("StringValue") and child.Name == "swim" then
			rotateCharacter = true
		end
	end
end

for _, animationModel in pairs(animationObjects) do
	getAnimations(animationModel)
end

local KeyframeSequenceProvider = game:GetService("KeyframeSequenceProvider")
local keyframes = {}

if poseAnimation then
	local kfs = KeyframeSequenceProvider:GetKeyframeSequence(poseAnimation.AnimationId)
	local animKeyframes = kfs:GetKeyframes()
	for _, keyframe in pairs(animKeyframes) do
		table.insert(keyframes, keyframe)
	end
else
	for _, animation in pairs(animations) do
		local kfs = KeyframeSequenceProvider:GetKeyframeSequence(animation.AnimationId)
		local animKeyframes = kfs:GetKeyframes()
		for _, keyframe in pairs(animKeyframes) do
			table.insert(keyframes, keyframe)
		end
	end
end

local keyframe = keyframes[math.max(1, math.floor(#keyframes/2))]
applyR15Pose(player.Character, keyframe)

if rotateCharacter then
	local rootPart = player.Character:FindFirstChild("HumanoidRootPart")
	if rootPart then
		rootPart.CFrame = rootPart.CFrame * CFrame.Angles(math.rad(-90), 0, 0)
		if not thumbnailCamera then
			local camera = Instance.new("Camera")
			camera.Name = "ThumbnailCamera"

			local rotatedCameraOffset = Vector3.new(6, 5, 7) * .7
			camera.CFrame = CFrame.new(Vector3.new(rootPart.Position.X, rootPart.Position.Y, rootPart.Position.Z) - rotatedCameraOffset, rootPart.Position)
			camera.Parent = player.Character
		end
	end
end

if thumbnailCamera then
	thumbnailCamera.Parent = player.Character
end

return game:GetService("ThumbnailGenerator"):Click(fileExtension, x, y, --[[hideSky = ]] true)