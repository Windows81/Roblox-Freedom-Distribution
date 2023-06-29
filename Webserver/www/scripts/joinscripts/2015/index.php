<?php

header("content-type:text/plain");

$year = addslashes($_GET["year"]);
$username = addslashes($_GET["username"]);
$ip = addslashes($_GET["ip"]);
$port = addslashes($_GET["port"]);
$id = addslashes($_GET["id"]);
$membership = addslashes($_GET["membership"]);
$response = "https://www.sitetest4.robloxlabs.com/scripts/joinscripts/2016?&year=$year&ip=$ip&port=$port&username=$username&membership=$membership&id=$id"
?>
<?php
echo $response
?>