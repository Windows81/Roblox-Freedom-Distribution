<?php
//require("/new/xampp/htdocs/corescripts/JS.php");
header("content-type:text/plain");
$year = addslashes($_GET["year"]);
$status = file_get_contents("http://www.sitetest4.robloxlabs.com/game/placelauncherstatus.ashx"); 
$username = addslashes($_GET["username"]);
$membership = addslashes($_GET["membership"]);
$ip = addslashes($_GET["ip"]);
$port = addslashes($_GET["port"]);
$username = addslashes($_GET["username"]);
$id = addslashes($_GET["id"]);
$v0 = 0;
//echo '{"jobId":"","status":,"joinScriptUrl":"","authenticationUrl":"","authenticationTicket":"","message":null}';
?>

<?php
while ($v0 < 6) { 
$v0 = $v0 + 1; 
}
sleep(1.75)
//exit;}
?>
{"jobId":"Test","status":<?php echo $status ?>,"joinScriptUrl":"https://assetgame.sitetest4.robloxlabs.com/game/Join.ashx?placeid=1818&ip=<?php echo $ip ?>&port=<?php echo $port ?>&username=<?php echo $username ?>&id=<?php echo $id ?>&membership=<?php echo $membership ?>&shirt=0&pants=0&hat=0&year=<?php echo $year ?>","authenticationUrl":"http://auth.sitetest4.robloxlabs.com/Login/Negotiate.ashx","authenticationTicket":"1","message":null}
