<?php

header("content-type:text/plain");

$year = addslashes($_GET["year"]);
$username = addslashes($_GET["username"]);
$ip = addslashes($_GET["ip"]);
$port = addslashes($_GET["port"]);
$id = addslashes($_GET["id"]);
$membership = addslashes($_GET["membership"]);
$response = file_get_contents("http://sitetest4.robloxlabs.com/game/join.lua?&id=$id&port=&$port&username=$username&ip=$ip&year=$year&clientticket=Test&membership=$membership");
echo $response
?>