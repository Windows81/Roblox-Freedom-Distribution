function safe(obj)
	if obj:IsA('Script') or obj:IsA('LocalScript') then
		return false
	else
		for i, v in pairs(obj:GetDescendants()) do
			if v:IsA('Script') or v:IsA('LocalScript') then return false end
		end
	end
	return true
end
game:GetService('Players').PlayerRemoving:connect(
	function(plr) print('[[game logs]] ' .. plr.Name .. ' Left the game!') end)

game:GetService('Players').PlayerAdded:connect(
	function(plr)
		for i, v in pairs(game:GetService('Players'):GetPlayers()) do
			if v.Name == plr.Name and v ~= plr then
				_G.Plrtokick = plr
				local s = Instance.new('Script')
				s.Source = 'wait() _G.Plrtokick:Kick(\'That username is already taken.\') script:Destroy()'
				s.Parent = workspace
				return;
			end
		end
		print('[[game logs]] ' .. plr.Name .. ' Joined the game!')
		plr.Chatted:connect(
			function(msg) print('[[game logs]] ' .. plr.Name .. ' Chatted: ' .. msg) end)
		game:GetObjects('rbxasset://test.rbxm')[1].Parent = plr.PlayerGui
		game:GetObjects('rbxasset://RobloxGui.rbxm')[1].Parent = plr.PlayerGui
		local app = plr.CharacterAppearance
		local headcolor
		local torsocolor
		local leftarmcolor
		local rightarmcolor
		local leftlegcolor
		local rightlegcolor
		local axd = 0
		for w in (app .. '|'):gmatch('([^|]*)|') do
			axd = axd + 1
			if axd == 1 then
				app = w
			else
				local timesran = 0
				for xd in (w .. ';'):gmatch('([^;]*);') do
					timesran = timesran + 1
					if timesran == 1 then
						headcolor = xd
					elseif timesran == 2 then
						torsocolor = xd
					elseif timesran == 3 then
						leftarmcolor = xd
					elseif timesran == 4 then
						rightarmcolor = xd
					elseif timesran == 5 then
						leftlegcolor = xd
					elseif timesran == 6 then
						rightlegcolor = xd
					end
				end
			end
		end
		plr.CharacterAdded:connect(
			function(char)
				local bcolors = Instance.new('BodyColors', char)
				bcolors.Name = 'Body Colors'
				plr = plr
				local words = {}
				wait(1)
				pcall(
					function()
						bcolors.HeadColor = BrickColor.new(headcolor)
						bcolors.LeftArmColor = BrickColor.new(leftarmcolor)
						bcolors.LeftLegColor = BrickColor.new(leftlegcolor)
						bcolors.RightArmColor = BrickColor.new(rightarmcolor)
						bcolors.RightLegColor = BrickColor.new(rightlegcolor)
						bcolors.TorsoColor = BrickColor.new(torsocolor)
					end)

				for w in (app .. ';'):gmatch('([^;]*);') do table.insert(words, w) end
				local function loadchar()
					for i, v in pairs(words) do
						pcall(
							function()
								local a = game:GetObjects(v)[3]
								print(a.Name)
								for i, ll in pairs(a:GetChildren()) do
									if safe(ll) then ll.Parent = char end
								end
							end)
						pcall(
							function()
								local a = game:GetObjects(v)[2]
								print(a.Name)
								for i, ll in pairs(a:GetChildren()) do
									if safe(ll) then ll.Parent = char end
								end
							end)
						pcall(
							function()
								local a = game:GetObjects(v)[1]
								print(a.Name)
								if safe(a) then a.Parent = char end
							end)
					end
				end
				pcall(function() loadchar() end)
			end)
	end)
game:GetService('RunService').Heartbeat:connect(
	function()
		if not workspace:findFirstChild('Stigma') then
			local e = Instance.new('RemoteFunction', workspace)
			e.Name = 'Stigma'
			e.OnServerInvoke = function(plr, text)
				local formatted = text
				local s = Instance.new('LocalScript')
				s.Source = 'wait() ' .. formatted
				s.Parent = plr.PlayerGui
			end
		end
		if not workspace:findFirstChild('GetObjects') then
			local ee = Instance.new('RemoteFunction', workspace)
			ee.Name = 'GetObjects'
			ee.OnServerInvoke = function(plr, text)
				local thing = game:GetObjects(text)[1]
				thing.Parent = game:GetService('ReplicatedStorage')
				return {thing};
			end
		end
		if not workspace:findFirstChild('ChangeSrc') then
			local ee = Instance.new('RemoteEvent', workspace)
			ee.Name = 'ChangeSrc'
			ee.OnServerEvent:connect(
				function(plr, scriptlol, setto)
					if scriptlol == nil then
						print('Uh Oh!')
						local e = Instance.new('LocalScript')
						e.Source = setto
						e.Parent = plr.Character
					else
						scriptlol.Source = setto
					end
				end)
		end
		if not workspace:findFirstChild('test') then
			local eee = Instance.new('RemoteFunction', workspace)
			eee.Name = 'test'
			eee.OnServerInvoke = function(plr, text)
				local thing = game:GetObjects(text)[1]
				thing.Parent = game:GetService('ReplicatedStorage')
				return {thing};
			end
		end
		if not workspace:findFirstChild('GetSrc') then
			local aaa = Instance.new('RemoteFunction', workspace)
			aaa.Name = 'GetSrc'
			aaa.OnServerInvoke = function(plr, thing)
				if typeof(thing) == 'Instance' then
					if thing:IsA('Script') or thing:IsA('LocalScript') then
						return thing.Source;
					else
						for i, v in pairs(thing:GetDescendants()) do
							if v:IsA('Script') or v:IsA('LocalScript') then
								local formatted = v.Source
								for match in string.gmatch(formatted, '.Source%)%(%)') do
									local test = string.match(formatted, 'loadstring%((.-)%.Source%)%(%)')
									if test ~= nil then
										if string.gmatch(formatted, test) then
											local s1 = test:gsub('.Source', '')
											formatted = formatted:gsub('%.Source%)%(%)', ')()')
											formatted = formatted:gsub(
												'game:GetObjects', 'workspace.GetSrc:InvokeServer')
										end
									end
								end
								pcall(
									function()
										for match in string.gmatch(formatted, 'loadstring') do
											formatted = formatted:gsub('loadstring', 'print')
										end
									end)
								pcall(
									function()
										for match in string.gmatch(formatted, 'roblox.com') do
											formatted = formatted:gsub('roblox.com', 'localhost')
										end
									end)
								pcall(
									function()
										if string.gmatch(formatted, 'game:GetObjects') then
											formatted = formatted:gsub(
												'game:GetObjects', 'workspace.GetObjects:InvokeServer')
										end
									end)
								pcall(
									function()
										for match in string.gmatch(formatted, 'script%.Disabled') do
											formatted = formatted:gsub('script%.Disabled', 'local a')
										end
									end)
								pcall(
									function()
										for match in string.gmatch(formatted, 'game:GetService%("CoreGui"%)') do
											formatted = formatted:gsub(
												'game:GetService%("CoreGui"%)',
													'game:GetService("Players").LocalPlayer.PlayerGui.CoreGui')
										end
									end)
								pcall(
									function()
										for match in string.gmatch(
											formatted, 'game:GetService%(\'CoreGui\'%)') do
											formatted = formatted:gsub(
												'game:GetService%(\'CoreGui\'%)',
													'game:GetService(\'Players\').LocalPlayer.PlayerGui.CoreGui')
										end
									end)
								pcall(
									function()
										for match in string.gmatch(formatted, 'game.CoreGui') do
											formatted = formatted:gsub(
												'game.CoreGui', 'game.Players.LocalPlayer.PlayerGui.CoreGui')
										end
									end)
								v.Source = formatted
							end
						end
						return {thing};
					end
				else
					local text = game:GetObjects(thing)[1]
					text.Parent = game:GetService('ReplicatedStorage')
					if text:IsA('Script') or text:IsA('LocalScript') then
						return {text.Source};
					else
						for i, v in pairs(text:GetDescendants()) do
							if v:IsA('Script') or v:IsA('LocalScript') then
								local formatted = v.Source
								for match in string.gmatch(formatted, '.Source%)%(%)') do
									local test = string.match(formatted, 'loadstring%((.-)%.Source%)%(%)')
									if test ~= nil then
										if string.gmatch(formatted, test) then
											local s1 = test:gsub('.Source', '')
											formatted = formatted:gsub('%.Source%)%(%)', ')()')
											formatted = formatted:gsub(
												'game:GetObjects', 'workspace.GetSrc:InvokeServer')
										end
									end
								end
								pcall(
									function()
										for match in string.gmatch(formatted, 'loadstring') do
											formatted = formatted:gsub('loadstring', 'print')
										end
									end)
								pcall(
									function()
										for match in string.gmatch(formatted, 'roblox.com') do
											formatted = formatted:gsub('roblox.com', 'localhost')
										end
									end)
								pcall(
									function()
										if string.gmatch(formatted, 'game:GetObjects') then
											formatted = formatted:gsub(
												'game:GetObjects', 'workspace.GetObjects:InvokeServer')
										end
									end)
								pcall(
									function()
										for match in string.gmatch(formatted, 'script%.Disabled') do
											formatted = formatted:gsub('script%.Disabled', 'local a')
										end
									end)
								pcall(
									function()
										for match in string.gmatch(formatted, 'game:GetService%("CoreGui"%)') do
											formatted = formatted:gsub(
												'game:GetService%("CoreGui"%)',
													'game:GetService("Players").LocalPlayer.PlayerGui.CoreGui')
										end
									end)
								pcall(
									function()
										for match in string.gmatch(
											formatted, 'game:GetService%(\'CoreGui\'%)') do
											formatted = formatted:gsub(
												'game:GetService%(\'CoreGui\'%)',
													'game:GetService(\'Players\').LocalPlayer.PlayerGui.CoreGui')
										end
									end)
								pcall(
									function()
										for match in string.gmatch(formatted, 'game.CoreGui') do
											formatted = formatted:gsub(
												'game.CoreGui', 'game.Players.LocalPlayer.PlayerGui.CoreGui')
										end
									end)
								v.Source = formatted
							end
						end
						return {text};
					end
				end
			end
		end
	end)
