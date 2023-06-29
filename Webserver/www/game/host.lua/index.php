<?php
$servertTicket = "test"
//DO NOT FUCK WITH THE SIGNATURE
?>
<?php
header("content-type:text/plain");
ob_start();
?>

-- Start Game Script Arguments
local serverticket, placeId, port  = ...


-- StartGame -- 
local serverticket = <?php echo $servertTicket ?> 
local bitstream = (game.PlaceId .. "10240210502135021305302150231050215021")

pcall(function() game:GetService("ScriptContext"):AddStarterScript(injectScriptAssetID) end)
game:GetService("RunService"):Run()


-----------------------------------START GAME SHARED SCRIPT------------------------------
local placeId = 1818
local port = 53640
local url = "http://www.sitetest4.robloxlabs.com"
local assetId = placeId -- might be able to remove this now


game:SetPlaceID(assetId, false)
ns = game:GetService("NetworkServer")

if placeId~=nil then
	-- yield so that file load happens in the heartbeat thread
	wait(5)
	
	-- load the game
	game:Load("rbxasset://place.rbxl")
end

-- Now start the connection
ns:Start(port, 0) 

sageage = Instance.new("Model")
sageage.Parent = game.Lighting
sageage.Name = "Data"
------------------------------END START GAME SHARED SCRIPT--------------------------
<?php
$data = ob_get_clean();
$signature;
$key = file_get_contents("http://sitetest4.robloxlabs.com/game/privatekey.pem"); 
openssl_sign($data, $signature, $key, OPENSSL_ALGO_SHA1);
echo "--rbxsig" . sprintf("%%%s%%%s", base64_encode($signature), $data);
$servericket = "test"
?>
