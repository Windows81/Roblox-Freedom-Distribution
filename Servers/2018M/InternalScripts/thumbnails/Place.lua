-- Place v1.0.2

assetUrl, fileExtension, x, y, baseUrl, universeId = ... 

pcall(function() game:GetService("ContentProvider"):SetBaseUrl(baseUrl) end)
if universeId ~= nil then
	pcall(function() game:SetUniverseId(universeId) end)
end

game:GetService("ScriptContext").ScriptsDisabled = true
game:GetService("StarterGui").ShowDevelopmentGui = false

game:Load(assetUrl)

-- Do this after again loading the place file to ensure that these values aren't changed when the place file is loaded.
game:GetService("ScriptContext").ScriptsDisabled = true
game:GetService("StarterGui").ShowDevelopmentGui = false

return game:GetService("ThumbnailGenerator"):Click(fileExtension, x, y, --[[hideSky = ]] false)