-- AnimationManifest.txt
-- V 1.0.2

-- Exports multiple frames 
-- https://spocktopus.roblox.local/Internals_of_3D_Animated_Thumbnails

baseUrl, characterAppearanceUrl, animationUrl = ...

pcall(function() game:GetService("ContentProvider"):SetBaseUrl(baseUrl) end)
game:GetService("ScriptContext").ScriptsDisabled = true

local player = game:GetService("Players"):CreateLocalPlayer(0)
player.CharacterAppearance = characterAppearanceUrl
player:LoadCharacterBlocking()

local FRAME_RATE = 60
local MAX_TIME = 2
local originalJointCFramesMap = {}
local originalPartsCFramesMap = {}

local function getOriginalJointCFrames(object)
	for _, child in pairs(object:GetChildren()) do
		if child:IsA("Motor6D") then
			originalJointCFramesMap[child] = child.C1
		end
		if child:IsA("BasePart") then
			originalPartsCFramesMap[child] = child.CFrame
		end
		getOriginalJointCFrames(child)
	end
end

local character = player.Character
local humanoid = character:FindFirstChildOfClass("Humanoid")
getOriginalJointCFrames(character)

local animator = humanoid:FindFirstChild("Animator")
local animationObj = Instance.new("Animation")

local animationObjects = game:GetObjects(animationUrl)
local animations = {}
local rotateCharacter = false

local function getAnimations(model)
	for _, child in pairs(model:GetChildren()) do
		if child:IsA("StringValue") and child.Name == "swim" then
			rotateCharacter = true
		elseif child:IsA("StringValue") and child.Name == "swimidle" then
			-- Don't include swimidle if we are thumnailing the swim animation
			if child.Parent and child.Parent:FindFirstChild("swim") then
				return
			end
		end
	
		if child:IsA("Animation") then
			table.insert(animations, child)
		else
			getAnimations(child)
		end
	end
end

for _, animationModel in pairs(animationObjects) do
	getAnimations(animationModel)
end

if rotateCharacter then
	local rootPart = character:FindFirstChild("HumanoidRootPart")
	if rootPart then
		rootPart.CFrame = rootPart.CFrame * CFrame.Angles(math.rad(-90), 0, 0)
	end
end

local animationId = ""
local bestWeight = -1
for _, anim in pairs(animations) do
	local weight = anim:FindFirstChild("Weight")
	if weight then
		if weight.Value > bestWeight then
			bestWeight = weight.Value
			animationId = anim.AnimationId
		end
	else
		animationId = anim.AnimationId
	end
end

local KeyframeSequenceProvider = game:GetService("KeyframeSequenceProvider")
local keyframeSequence = KeyframeSequenceProvider:GetKeyframeSequence(animationId)
animationObj.AnimationId = KeyframeSequenceProvider:RegisterActiveKeyframeSequence(keyframeSequence)

for _, track in pairs(humanoid:GetPlayingAnimationTracks())	 do
	track:Stop(0)
end

local track = humanoid:LoadAnimation(animationObj)
track:Play(0)

local finished = false

local function stepNextFrame()	
	local delta = 1/FRAME_RATE

	if track.TimePosition + delta > track.Length then
		delta = track.Length - track.TimePosition
	end

	if delta <= 0.005 or track.TimePosition >= track.Length or finished then
		return false
	end

	local preStepTimePosition = track.TimePosition
	animator:StepAnimations(delta)
	
	if track.TimePosition <= preStepTimePosition then
		finished = true
	end
	
	return true
end

local math_floor = math.floor
local math_sin = math.sin
local math_cos = math.cos
local math_min = math.min
local math_max = math.max
local function round(number)
	return math_floor(number*10000 + 0.5)/10000
end

local function vector3ToTable(vector)
	return {
		x = round(vector.X),
		y = round(vector.Y),
		z = round(vector.Z)
	}
end

local animationData = {}

while stepNextFrame() do
	local frameAnimationData = {}
	
	for _, obj in pairs(character:GetChildren()) do
		if obj:IsA("BasePart") or obj:IsA("Accoutrement") then
			local part = obj
			if obj:IsA("Accoutrement") then
				part = obj:FindFirstChild("Handle")
			end
			if part and part.Name ~= "HumanoidRootPart" then
				local posAndRotation = {}
				posAndRotation["Position"] = vector3ToTable(part.Position)
				local axis, angle = part.CFrame:toAxisAngle()
				local halfAngle = angle/2
				posAndRotation["Rotation"] = {
					x = round(math_sin(halfAngle)*axis.X),
					y = round(math_sin(halfAngle)*axis.Y),
					z = round(math_sin(halfAngle)*axis.Z),
					w = round(math_cos(halfAngle))
				}
				
				frameAnimationData[obj.Name] = posAndRotation
			end
		end
	end
	table.insert(animationData, frameAnimationData)
end

-- Take note of finishing CFrames for the animation
-- The CameraResult position will be transformed based on this
local animatedPartPositionsMap = {}

for part, _ in pairs(originalPartsCFramesMap) do
	animatedPartPositionsMap[part] = part.Position
end

-- Restore original CFrames
for motor, origC1 in pairs(originalJointCFramesMap) do
	motor.C1 = origC1
end

for part, cframe in pairs(originalPartsCFramesMap) do
	part.Anchored = true
	part.CFrame = cframe
end

local partsArray = {}
for _, obj in pairs(character:GetChildren()) do
	if obj:IsA("BasePart") or obj:IsA("Accoutrement") then
		if obj.Name ~= "HumanoidRootPart" then
			table.insert(partsArray, obj)
		end
	end
end

local string_sub = string.sub
local string_len = string.len
function strEndsWith(str, val)
   return string_sub(str, -string_len(val)) == val
end

function replaceChar(pos, str, r)
    return str:sub(1, pos - 1) ..r.. str:sub(pos + 1)
end

game:GetService("Selection"):Set(partsArray)
local objsStrOutput = nil
objsStrOutput, contentIdsUsed = game:GetService("ThumbnailGenerator"):Click("SplitObjs", 0, 0, true)

local decodedObjsStrOutput = game:GetService("HttpService"):JSONDecode(objsStrOutput)
local partObjsResult = {}
local textures = {}
local cameraResult = nil

local totalAABB = {
    ["min"] = {},
    ["max"] = {}
}

local function addToTotalAABB(partName, partAABB)
	local part = character:FindFirstChild(partName)
	if part and animatedPartPositionsMap[part] then
		local currentPosition = part.Position
		local animatedPosition = animatedPartPositionsMap[part]
		local offset = animatedPosition - currentPosition
		
		local minJSON = partAABB["min"]
		local currentMin = Vector3.new(minJSON.x, minJSON.y, minJSON.z)
		currentMin = Vector3.new(currentMin.X, currentMin.Y + offset.Y, currentMin.Z)
		partAABB["min"] = vector3ToTable(currentMin)
		
		local maxJSON = partAABB["min"]
		local currentMax = Vector3.new(maxJSON.x, maxJSON.y, maxJSON.z)
		currentMax = Vector3.new(currentMax.X, currentMax.Y + offset.Y, currentMax.Z)
		partAABB["min"] = vector3ToTable(currentMax)
	end	
	
	for xyzkey, val in pairs(partAABB["min"]) do
		if not totalAABB["min"][xyzkey] then
			totalAABB["min"][xyzkey] = val
		else
			totalAABB["min"][xyzkey] = math_min(totalAABB["min"][xyzkey], val)
		end
	end

	for xyzkey, val in pairs(partAABB["max"]) do
		if not totalAABB["max"][xyzkey] then
			totalAABB["max"][xyzkey] = val
		else
			totalAABB["max"][xyzkey] = math_max(totalAABB["max"][xyzkey], val)
		end
	end
end

local function resolveCameraResult(partName, cameraJSON)
	local part = character:FindFirstChild(partName)
	if part and animatedPartPositionsMap[part] then
		local currentPosition = part.Position
		local animatedPosition = animatedPartPositionsMap[part]
		local offset = animatedPosition - currentPosition
		
		local positionJSON = cameraJSON["position"]
		local cameraPosition = Vector3.new(positionJSON.x, positionJSON.y, positionJSON.z)
		cameraPosition = cameraPosition + offset
		cameraJSON["position"] = vector3ToTable(cameraPosition)
	end
	
	if partName == "Head" then
		cameraResult = cameraJSON
	elseif cameraResult == nil then -- Fallback if Head doesn't exist for some reason
		cameraResult = cameraJSON
	end
end

-- Process the SplitObjs output to consolidate it for the animation output.
-- The data for common textures is mapped to the same output in the textures table. 
-- The Camera and AABB fields are consolidated into global fields.
for key, val in pairs(decodedObjsStrOutput) do
	local decodedPartObj = game:GetService("HttpService"):JSONDecode(val)
	if decodedPartObj["files"] then
		local files = decodedPartObj["files"]
		for fileName, fileInfo in pairs(files) do
			local fileContent = fileInfo.content
			if strEndsWith(fileName, ".png") then
				local newFileName = fileName
				while textures[newFileName] and textures[newFileName].content ~= fileContent do
					local charsFromEnd = string_len("Tex.png")
					local replacePos = string_len(newFileName) - charsFromEnd
					local newNumber = tostring(tonumber(newFileName:sub(replacePos, replacePos)) + 1)
					newFileName = replaceChar(replacePos, newFileName, newNumber)
				end
				textures[newFileName] = {
					content = fileContent
				}
				files["texture"] = newFileName				
				files[fileName] = nil
			end
		end
	end

	-- Calculate total aabb
	if decodedPartObj["AABB"] then
		addToTotalAABB(key, decodedPartObj["AABB"])
		decodedPartObj["AABB"] = nil
	end
	
	-- Resolve overall Camera JSON.
	if decodedPartObj["camera"] then
		resolveCameraResult(key, decodedPartObj["camera"])
		decodedPartObj["camera"] = nil
	end
	partObjsResult[key] = decodedPartObj
end

-- Special camera position and direction for rotated character
if rotateCharacter then
	local rootPart = character:FindFirstChild("HumanoidRootPart")
	if rootPart then
		local cameraOffset = Vector3.new(6, 5, 7) * .7
		local cameraPosition = Vector3.new(rootPart.Position.X, rootPart.Position.Y, rootPart.Position.Z) - cameraOffset
		local cameraDirection = (rootPart.Position - cameraPosition).unit
		cameraResult["position"] = vector3ToTable(cameraPosition)
		cameraResult["direction"] = vector3ToTable(cameraDirection)
	end
end

local resultData = {
	Frames = animationData,
	Camera = cameraResult,
	AABB = totalAABB,
	PartObjs = partObjsResult,
	Textures = textures
}

return game:GetService("HttpService"):JSONEncode(resultData), contentIdsUsed