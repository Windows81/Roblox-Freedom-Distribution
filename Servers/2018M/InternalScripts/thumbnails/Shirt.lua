-- Shirt v1.0.1

assetUrl, fileExtension, x, y, baseUrl, mannequinId = ...

pcall(function() game:GetService("ContentProvider"):SetBaseUrl(baseUrl) end)
game:GetService("ScriptContext").ScriptsDisabled = true

local mannequin = game:GetObjects(baseUrl.. "asset/?id=" .. tostring(mannequinId))[1]
mannequin.Humanoid.DisplayDistanceType = Enum.HumanoidDisplayDistanceType.None
mannequin.Parent = workspace

local shirt = game:GetObjects(assetUrl)[1]
shirt.Parent = mannequin

return game:GetService("ThumbnailGenerator"):Click(fileExtension, x, y, --[[hideSky = ]] true)