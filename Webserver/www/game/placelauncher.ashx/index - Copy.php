<?php
header("content-type:text/plain");
$year = addslashes($_GET["year"]);
$status = file_get_contents("http://www.sitetest4.robloxlabs.com/game/placelauncherstatus.ashx"); 
$username = addslashes($_GET["username"]);
$membership = addslashes($_GET["membership"]);
$ip = addslashes($_GET["ip"]);
$port = addslashes($_GET["port"]);
$username = addslashes($_GET["username"]);
$id = addslashes($_GET["id"]);
?>
{"jobId":"Test","status":<?php echo $status ?>,"joinScriptUrl":"https://assetgame.sitetest4.robloxlabs.com/game/Join.ashx?placeid=1818&ip=<?php echo $ip ?>&port=<?php echo $port ?>&username=<?php echo $username ?>&id=<?php echo $id ?>&membership=<?php echo $membership ?>&shirt=0&pants=0&hat=0&year=<?php echo $year ?>","authenticationUrl":"http://auth.sitetest4.robloxlabs.com/Login/Negotiate.ashx","authenticationTicket":"1","message":null}

<?php
header("content-type:text/plain");
$year = addslashes($_GET["year"]);
$status = file_get_contents("http://www.sitetest4.robloxlabs.com/game/placelauncherstatus.ashx"); 
$username = addslashes($_GET["username"]);
$membership = addslashes($_GET["membership"]);
$ip = addslashes($_GET["ip"]);
$port = addslashes($_GET["port"]);
$username = addslashes($_GET["username"]);
$id = addslashes($_GET["id"]);
?>
{"jobId":"Test","status":<?php echo $status ?>,"joinScriptUrl":"http://www.lumias.gay/game/join.ashx?placeId=1&userName=mario&placeAddress=127.0.0.1&placePort=4001","authenticationUrl":"http://auth.sitetest4.robloxlabs.com/Login/Negotiate.ashx","authenticationTicket":"1","message":null}