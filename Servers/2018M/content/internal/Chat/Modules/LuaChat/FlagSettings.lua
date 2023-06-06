local Modules = game:GetService("CoreGui").RobloxGui.Modules
local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")

local FormFactor = require(Modules.LuaApp.Enum.FormFactor)

-- Note: Can fail when called, GetPlatform requires restricted permissions:
local ok, platform = pcall(function()
	return UserInputService:GetPlatform()
end)
if not ok then
	platform = Enum.Platform.None
	warn("FlagSettings - couldn't identify platform.")
end

-- Read all the flags up front. This is to throw an exception at import time
-- if they don't exist, while also letting them get picked up by scanners:
local luaChatPlayTogetherThrottleiOSPhone = settings():GetFVariable("LuaChatPlayTogetherThrottleiOSPhone3")
local luaChatPlayTogetherThrottleiOSTablet = settings():GetFVariable("LuaChatPlayTogetherThrottleiOSTablet3")
local luaChatPlayTogetherThrottleAndroidPhone = settings():GetFVariable("LuaChatPlayTogetherThrottleAndroidPhone3")
local luaChatPlayTogetherThrottleAndroidTablet = settings():GetFVariable("LuaChatPlayTogetherThrottleAndroidTablet3")
local luaChatUseCppTextTruncation = settings():GetFFlag("LuaChatUseCppTextTruncation")
local textTruncationEnabled = settings():GetFFlag("TextTruncationEnabled")

local FlagSettings = {}

-- Helper function to throttle based on player Id:
function FlagSettings.ThrottleUserId(throttle, userId)
	assert(type(throttle) == "number")
	assert(type(userId) == "number")

	-- Determine userRollout using last two digits of user ID:
	-- (+1 to change range from 0-99 to 1-100 as 0 is off, 100 is full on):
	local userRollout = (userId % 100) + 1
	return userRollout <= throttle
end

function FlagSettings.IsLuaChatPlayTogetherEnabled(formFactor)
	-- Read throttle value based on platform and form factor:
	-- Note: defaults to iOS Tablet in Studio:
	local throttle
	if platform == Enum.Platform.Android then
		if formFactor == FormFactor.PHONE then
			throttle = luaChatPlayTogetherThrottleAndroidPhone
		else
			throttle = luaChatPlayTogetherThrottleAndroidTablet
		end
	else
		if formFactor == FormFactor.PHONE then
			throttle = luaChatPlayTogetherThrottleiOSPhone
		else
			throttle = luaChatPlayTogetherThrottleiOSTablet
		end
	end

	local throttleNumber = tonumber(throttle)
	if throttleNumber == nil then
		return false
	end

	local userId = Players.LocalPlayer.UserId
	return FlagSettings.ThrottleUserId(throttleNumber, userId)
end

function FlagSettings.UseCppTextTruncation()
	return luaChatUseCppTextTruncation and textTruncationEnabled
end

return FlagSettings