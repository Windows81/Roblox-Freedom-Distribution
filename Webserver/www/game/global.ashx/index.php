<?php
header("content-type:text/plain");
ob_start();
//15 seconds is enough time for me to patch sigs once the connection is accepted... maybe?
?>

printidentity()
wait (15)
pcall(function() game:GetService("InsertService"):SetFreeModelUrl("http://www.roblox.com/Game/Tools/InsertAsset.ashx?type=fm&q=%s&pg=%d&rs=%d") end)
pcall(function() game:GetService("InsertService"):SetFreeDecalUrl("http://www.roblox.com/Game/Tools/InsertAsset.ashx?type=fd&q=%s&pg=%d&rs=%d") end)

game:GetService("ScriptInformationProvider"):SetAssetUrl("http://www.tadah.rocks/asset/")
game:GetService("InsertService"):SetBaseSetsUrl("http://www.tadah.rocks/Game/Tools/InsertAsset.ashx?nsets=10&type=base")
game:GetService("InsertService"):SetUserSetsUrl("http://www.tadah.rocks/Game/Tools/InsertAsset.ashx?nsets=20&type=user&userid=%d&t=2")
game:GetService("InsertService"):SetCollectionUrl("http://www.tadah.rocks/Game/Tools/InsertAsset.ashx?sid=%d")
game:GetService("InsertService"):SetAssetUrl("http://www.tadah.rocks/asset/?id=%d")
game:GetService("InsertService"):SetAssetVersionUrl("http://www.tadah.rocks/Asset/?assetversionid=%d")
game:GetService("InsertService"):SetTrustLevel(0)

pcall(function() game:GetService("SocialService"):SetFriendUrl("http://www.tadah.rocks/Game/LuaWebService/HandleSocialRequest.ashx?method=IsFriendsWith&playerid=%d&userid=%d") end)
pcall(function() game:GetService("SocialService"):SetBestFriendUrl("http://www.tadah.rocks/Game/LuaWebService/HandleSocialRequest.ashx?method=IsBestFriendsWith&playerid=%d&userid=%d") end)
pcall(function() game:GetService("SocialService"):SetGroupUrl("http://www.tadah.rocks/Game/LuaWebService/HandleSocialRequest.ashx?method=IsInGroup&playerid=%d&groupid=%d") end)
pcall(function() game:GetService("SocialService"):SetGroupRankUrl("http://www.tadah.rocks/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRank&playerid=%d&groupid=%d") end)
pcall(function() game:GetService("SocialService"):SetGroupRoleUrl("http://www.tadah.rocks/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRole&playerid=%d&groupid=%d") end)

local ScriptContext = game:GetService("ScriptContext")

-- 1086 for mid 2014 corescripts and 39 for late 2014, uncommented tadah
--ScriptContext:AddStarterScript(39)
<?php
$data = ob_get_clean();
$signature;
$key = file_get_contents("http://sitetest4.robloxlabs.com/game/PrivateKey.pem");
openssl_sign($data, $signature, $key, OPENSSL_ALGO_SHA1);
echo "--rbxsig" . sprintf("%%%s%%%s", base64_encode($signature), $data);
?>