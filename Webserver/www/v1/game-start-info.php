<?php
header("content-type:text/plain");
$universeid = addslashes($_GET["universeId"]);
$url = "https://avatar.roblox.com/v1/game-start-info?universeId=$universeid";
$response = file_get_contents($url);
echo $response;
?>