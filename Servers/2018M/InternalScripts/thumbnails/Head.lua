-- Head v1.0.1

assetUrl, fileExtension, x, y, baseUrl, mannequinId = ...

pcall(function() game:GetService("ContentProvider"):SetBaseUrl(baseUrl) end)

game:GetService("ScriptContext").ScriptsDisabled = true

local mannequin = game:GetObjects(baseUrl.. "asset/?id=" .. tostring(mannequinId))[1]
mannequin.Humanoid.DisplayDistanceType = Enum.HumanoidDisplayDistanceType.None
mannequin.Parent = workspace

mannequin.Head.BrickColor = BrickColor.Gray()
if mannequin.Head:FindFirstChild("Mesh") then
	mannequin.Head.Mesh:Destroy()
end

for _, child in pairs(mannequin:GetChildren()) do
	if child:IsA("BasePart") and child.Name ~= "Head" then
		child:Destroy()
	end
end

local mesh = game:GetObjects(assetUrl)[1]
mesh.Parent = mannequin.Head

return game:GetService("ThumbnailGenerator"):Click(fileExtension, x, y, --[[hideSky = ]] true)