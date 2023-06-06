-- Hat v1.0.1

assetUrl, fileExtension, x, y, baseUrl = ...

pcall(function() game:GetService("ContentProvider"):SetBaseUrl(baseUrl) end)
game:GetService("ScriptContext").ScriptsDisabled = true

game:GetObjects(assetUrl)[1].Parent = workspace

local ThumbnailGenerator = game:GetService("ThumbnailGenerator")
if string.lower(fileExtension) == "obj" then
	return ThumbnailGenerator:Click(fileExtension, x, y, --[[hideSky = ]] true, --[[crop = ]] true)
end

return ThumbnailGenerator:Click(fileExtension, x, y, --[[hideSky = ]] true, --[[crop = ]] true)
