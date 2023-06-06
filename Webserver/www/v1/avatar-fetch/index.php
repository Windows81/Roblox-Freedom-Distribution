<?php
require ("/new/xampp/htdocs/corescripts/settings.php");
header("content-type:text/plain");
if($userid == "1"){$userid = "4098960670";}
$url = "https://avatar.roblox.com/v1/avatar-fetch?placeId=$placeid&userId=$userid";
$response = file_get_contents($url);
echo $response;
?>
