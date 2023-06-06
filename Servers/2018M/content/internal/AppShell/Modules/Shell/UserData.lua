--[[
			// UserData.lua
			// API for all user related data

			// TODO:
				Eventually all of this will move into Rodux
]]
local CoreGui = game:GetService("CoreGui")
local GuiRoot = CoreGui:FindFirstChild("RobloxGui")
local Modules = GuiRoot:FindFirstChild("Modules")
local ShellModules = Modules:FindFirstChild("Shell")
local Players = game:GetService('Players')
local UserInputService = game:GetService("UserInputService")

local AccountManager = require(ShellModules:FindFirstChild('AccountManager'))
local Http = require(ShellModules:FindFirstChild('Http'))
local Utility = require(ShellModules:FindFirstChild('Utility'))

local UserData = {}

local currentUserData = nil

local CONSTANT_RETRY_TIME = 30

local function setVoteCountAsync()
	local voteResult = Http.GetVoteCountAsync()
	currentUserData["VoteCount"] = voteResult and voteResult['VoteCount'] or 0
end

local function verifyHasLinkedAccountAsync()
	local result = AccountManager:HasLinkedAccountAsync()

	while result ~= AccountManager.AuthResults.Success and result ~= AccountManager.AuthResults.AccountUnlinked do
		result = AccountManager:HasLinkedAccountAsync()
		wait(CONSTANT_RETRY_TIME)
	end

	currentUserData["LinkedAccountResult"] = result
end

local function verifyHasRobloxCredentialsAsync()
	local result = AccountManager:HasRobloxCredentialsAsync()

	while result ~= AccountManager.AuthResults.Success and result ~= AccountManager.AuthResults.UsernamePasswordNotSet do
		result = AccountManager:HasRobloxCredentialsAsync()
		wait(CONSTANT_RETRY_TIME)
	end

	currentUserData["RobloxCredentialsResult"] = result
end

function UserData:Initialize()
	if currentUserData then
		Utility.DebugLog("Trying to initialize UserData when we already have valid data.")
	end

	currentUserData = {}

	if UserInputService:GetPlatform() == Enum.Platform.XBoxOne then
		spawn(setVoteCountAsync)
		-- TODO: When all accounts that are linked but have no credentials are cleaned up, we can remove these checks
		spawn(verifyHasLinkedAccountAsync)
		spawn(verifyHasRobloxCredentialsAsync)
	end
end

function UserData:GetVoteCount()
	if not currentUserData then
		Utility.DebugLog("Error: UserData:GetVoteCount() - UserData has not been initialized. Don't do that!")
		return nil
	end
	return currentUserData["VoteCount"]
end

function UserData:IncrementVote()
	currentUserData["VoteCount"] = (currentUserData["VoteCount"] or 0) + 1
end

function UserData:DecrementVote()
	currentUserData["VoteCount"] = math.max((currentUserData["VoteCount"] or 0) - 1, 0)
end

-- returns true, false or nil in the case of error
function UserData:HasLinkedAccount()
	local result = currentUserData["LinkedAccountResult"]
	if result == AccountManager.AuthResults.Success then
		return true
	elseif result == AccountManager.AuthResults.AccountUnlinked then
		return false
	else
		return nil
	end
end

-- returns true, false or nil in the case of error
function UserData:HasRobloxCredentials()
	local result = currentUserData["RobloxCredentialsResult"]
	if result == AccountManager.AuthResults.Success then
		return true
	elseif result == AccountManager.AuthResults.UsernamePasswordNotSet then
		return false
	else
		return nil
	end
end

function UserData:Reset()
	currentUserData = nil
end

--[[ This should no longer be used ]]--
function UserData.GetLocalUserIdAsync()
	return UserData.GetLocalPlayerAsync().userId
end

function UserData.GetLocalPlayerAsync()
	local localPlayer = Players.LocalPlayer
	while not localPlayer do
		wait()
		localPlayer = Players.LocalPlayer
	end
	return localPlayer
end

function UserData.GetPlatformUserBalanceAsync()
	local result = Http.GetPlatformUserBalanceAsync()
	if not result then
		-- TODO: Error Code
		return nil
	end
	--

	return result["Robux"]
end

function UserData.GetTotalUserBalanceAsync()
	local result = Http.GetTotalUserBalanceAsync()
	if not result then
		return nil
	end

	return result["robux"]
end

return UserData
