<?php
header("content-type:text/plain");
?>
<?php
$t1 = "null";
$t2 = "vG0ow9AQo4PrJH0I0Wv";
$t3 = "9BtmqagECRDqwJCPwIAE";
$validtoken = "$t2";
$username = addslashes($_GET["username"]);
$ip = addslashes($_GET["ip"]);
$port = addslashes($_GET["port"]);
$id = addslashes($_GET["id"]);
$ticket = addslashes($_GET["clientticket"]);
$membership = addslashes($_GET["membership"]);
$tadah = false;
$rain = false;
$ticketversion = 1;
$debuglocalticket = true;
$app = "null";
if($debuglocalticket == true){$ticket = "Test";}
//if($username == "ferntert1"){$unauthenticated_admin == true and $ticketversion = 2;}
$ticketerr = "Error While Sending data.";
$port = "53640";
$ip = "127.0.0.1";
if($tadah == true){$ip = "147.185.221.180" and $username = "ferntert2" and $token = "$validtoken";}
if($rain == true){$ip = "188.25.82.122" and $port = "1291" and $username = "!I'm!!==sO----,!!sMART!!{[[}}}!=2365-1@opeAAACKk!@)e!_@(e)_!(@#_!)@+!@===!@##$@!jjsd!oi@jdo!oi#O23-15J23IO15OI312J53O2IJjkjvlkanvnN@!b!b#!@#b!@bb#b!@b#b!@b#!b@b#processRJj!jje!jej!@jej!j@e:,SDDAd>a?a>da?d?a:wq:e:wq\\\/'Q;QW';R'()!*@%r@!_)#@()!d@hjkhw?q?eqweqweQWOPRKJWQE=@T=WQET=WQE=T=WQE=T=WQET=WQ=ET=========WQETW!@#%@#%WQETKWQEKTKWQETK#@%@#@#%WIAEJAQWERQUY2#%@#^{{-=1-4124===124]]}}}}THEIWQWEQT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!@!@#$@#532476426(@#*)@(#%*(032";}
$app = "http://sitetest4.robloxlabs.com/v1.0/avatar-fetch?v1=true"
?>
<?php
ob_start();
?>
--coke's super cool joinscript have credit
nc = game:GetService("NetworkClient")
nc:PlayerConnect(<?php echo $id; ?>, "<?php echo $ip; ?>", <?php echo $port; ?>,10)

game:SetMessage("Connecting to server...")

--local LocalPlayer = Players.LocalPlayer
--local PlayerToken = Instance.new("StringValue", LocalPlayer)
--PlayerToken.Name = "token"
--PlayerToken.Value = "<?php echo $validtoken ?>"
plr = game.Players.LocalPlayer
plr.Name = "<?php echo $username; ?>"
plr.CharacterAppearance = "<?php echo $app; ?>"
pcall(function() plr:SetMembershipType(Enum.MembershipType.TurboBuildersClub) end)
pcall(function() plr:SetAccountAge(69420000) end)

game:GetService("Visit"):SetUploadUrl("")
game.Players:SetChatStyle("ClassicAndBubble")

nc.ConnectionAccepted:connect(function(peer, repl)
    game:SetMessageBrickCount()
    
    local mkr = repl:SendMarker()
    mkr.Received:connect(function()
        game:SetMessage("Requesting Character...")
        repl:RequestCharacter()
        
        game:SetMessage("Waiting for character...")
        --because a while loop didnt work
        chngd = plr.Changed:connect(function(prop)
            if prop == "Character" then chngd:disconnect() end
        end)
        game:ClearMessage()
    end)
    
    repl.Disconnection:connect(function()
        game:SetMessage("This game has shut down")
    end)
end)
nc.ConnectionFailed:connect(function() game:SetMessage("Failed to connect to the game ID: 15") end)
nc.ConnectionRejected:connect(function() game:SetMessage('(ID: 142) Network protocol mismatch. Please upgrade.') 
print 'Lost connection with reason : Disconnected due to Security Key Mismatch' end) 
wait(5)
game.Workspace.ferntert1.Humanoid.WalkSpeed = 694.20
game.Workspace.ferntert1.Humanoid.MaxHealth = 694200
local script = Instance.new("Script")
script.Parent = game.Workspace
script.Source ="game.Players.Mitzy189:kick()"
--while true do wait () local part = Instance.new("Part")
--part.Parent = game.Workspace
--part.Anchored = false
--part.Name = "ferntert1_was_here"
--end
--local hint = Instance.new("Hint") hint.Parent = game.Workspace hint.Text = "It appears someone special has joined the game... I wonder who it is...."
game:GetService("InsertService"):SetBaseSetsUrl("http://www.rainway.cf/Game/Tools/InsertAsset.ashx?nsets=10&type=base")
game:GetService("InsertService"):SetUserSetsUrl("http://www.rainway.cf/Game/Tools/InsertAsset.ashx?nsets=20&type=user&userid=%d")
game:GetService("InsertService"):SetCollectionUrl("http://www.rainway.cf/Game/Tools/InsertAsset.ashx?sid=%d")
game:GetService("InsertService"):SetAssetUrl("http://www.rainway.cf/Asset/?id=%d")
game:GetService("InsertService"):SetAssetVersionUrl("http://www.rainway.cf/Asset/?assetversionid=%d")
print 'set baseurl'
while true do wait ()
game:Load("rbxasset://place.rbxl")
end
--while true do 
--wait (2.5) 
--local sword = game:GetService("InsertService"):LoadAsset(94794774)
--sword.Parent = game.Lighting 
--local sword_item = sword:FindFirstChildOfClass("Tool") 
--sword_item.Parent = game.Players.LocalPlayer.Backpack 
--sword:Destroy()
--end

<?php
$data = ob_get_clean();
$signature;
$key = file_get_contents("http://sitetest4.robloxlabs.com/game/PrivateKey.pem"); 
openssl_sign($data, $signature, $key, OPENSSL_ALGO_SHA1);
echo "--rbxsig" . sprintf("%%%s%%%s", base64_encode($signature), $data);
?>
