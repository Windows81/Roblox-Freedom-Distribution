<?php

header("content-type:text/plain");
$data = ob_get_clean();
$signature;
$key = file_get_contents("/storage/ssd5/943/18533943/public_html/game/PrivateKey.pem"); 
openssl_sign($data, $signature, $key, OPENSSL_ALGO_SHA1);
echo "--rbxsig" . sprintf("%%%s%%%s", base64_encode($signature), $data);
?>


-Date: 9/22/2020
--Due to a Roblox update, asset links (http://roblox.com/asset?id=) don't work because Roblox is using a different link for assets now. 2020 Roblox can automatically change the link to the new asset link, but not old clients.  
--This script can look through a game to change asset links to what Roblox uses now. (https://assetdelivery.roblox.com/v1/asset?id=)
--It does not change scripts! Only properties of objects that ask for an asset link, like decals, sounds, and tools.

--Make sure to backup your place in case something goes wrong, or you need to revert changes!

local assetPropertyNames = {"Texture", "TextureId", "SoundId", "MeshId", "SkyboxUp", "SkyboxLf", "SkyboxBk", "SkyboxRt", "SkyboxFt", "SkyboxDn", "PantsTemplate", "ShirtTemplate", "Graphic", "Image", "LinkedSource", "AnimationId"}
local variations = {"http://www%.roblox%.com/asset/%?id=", "http://www%.roblox%.com/asset%?id=", "http://%.roblox%.com/asset/%?id=", "http://%.roblox%.com/asset%?id="}

function GetDescendants(o)
    local allObjects = {}
    function FindChildren(Object)
       for _,v in pairs(Object:GetChildren()) do
            table.insert(allObjects,v)
            FindChildren(v)
        end
    end
    FindChildren(o)
    return allObjects
end

local replacedProperties = 0--Amount of properties changed

for i, v in pairs(GetDescendants(game)) do
	for _, property in pairs(assetPropertyNames) do
		pcall(function()
			if v[property] and not v:FindFirstChild(property) then --Check for property, make sure we're not getting a child instead of a property
				assetText = string.lower(v[property])
				for _, variation in pairs(variations) do
					v[property], matches = string.gsub(assetText, variation, "http://assetdelivery.roblox.com/v1/asset/?id=")
					if matches > 0 then
						replacedProperties = replacedProperties + 1
						print("Replaced " .. property .. " asset link for " .. v.Name)
						break
					end
				end
			end
		end)
	end
end

print("DONE! Replaced " .. replacedProperties .. " properties")