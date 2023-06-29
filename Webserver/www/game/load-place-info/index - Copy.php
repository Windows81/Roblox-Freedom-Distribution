<?php
header("content-type:text/plain");
ob_start();
?>

local baseUrl = https://www.sitetest4.robloxlabs.com

-- Loaded by StartGameSharedScript --
pcall(function() game:SetCreatorID(1, Enum.CreatorType.User) end)

pcall(function() game:GetService("SocialService"):SetFriendUrl(baseUrl .. "/Game/LuaWebService/HandleSocialRequest.ashx?method=IsFriendsWith&playerid=%d&userid=%d") end)
pcall(function() game:GetService("SocialService"):SetBestFriendUrl(baseUrl .. "/Game/LuaWebService/HandleSocialRequest.ashx?method=IsBestFriendsWith&playerid=%d&userid=%d") end)
pcall(function() game:GetService("SocialService"):SetGroupUrl(baseUrl .. "/Game/LuaWebService/HandleSocialRequest.ashx?method=IsInGroup&playerid=%d&groupid=%d") end)
pcall(function() game:GetService("SocialService"):SetGroupRankUrl(baseUrl .. "/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRank&playerid=%d&groupid=%d") end)
pcall(function() game:GetService("SocialService"):SetGroupRoleUrl(baseUrl .. "/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRole&playerid=%d&groupid=%d") end)
pcall(function() game:GetService("GamePassService"):SetPlayerHasPassUrl(baseUrl .. "/Game/GamePass/GamePassHandler.ashx?Action=HasPass&UserID=%d&PassID=%d") end)
pcall(function() game:GetService("MarketplaceService"):SetProductInfoUrl(baseUrl .. "/marketplace/productinfo?assetId=%d") end)
pcall(function() game:GetService("MarketplaceService"):SetDevProductInfoUrl(baseUrl .. "/marketplace/productDetails?productId=%d") end)
pcall(function() game:GetService("MarketplaceService"):SetPlayerOwnsAssetUrl(baseUrl .. "/ownership/hasasset?userId=%d&assetId=%d") end)
pcall(function() game:SetPlaceVersion(0) end)
pcall(function() game:SetVIPServerOwnerId(1) end)

<?php
$data = ob_get_clean();
$signature;
$key = file_get_contents("http://www.sitetest4.robloxlabs.com/game/privatekey.pem");
openssl_sign($data, $signature, $key, OPENSSL_ALGO_SHA1);
echo "--rbxsig" . sprintf("%%%s%%%s", base64_encode($signature), $data);

?>