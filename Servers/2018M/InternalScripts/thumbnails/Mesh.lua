-- Mesh v1.0.1

assetUrl, fileExtension, x, y, baseUrl = ...

pcall(function() game:GetService("ContentProvider"):SetBaseUrl(baseUrl) end)

game:GetService("ScriptContext").ScriptsDisabled = true

local part = Instance.new("Part")
part.Parent = workspace

local specialMesh = Instance.new("SpecialMesh")
specialMesh.MeshId = assetUrl
specialMesh.Parent = part

return game:GetService("ThumbnailGenerator"):Click(fileExtension, x, y, --[[hideSky = ]] true, --[[crop = ]] true)