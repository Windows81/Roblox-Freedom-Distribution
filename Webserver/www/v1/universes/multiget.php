<?php
header("content-type:text/plain");
$ids = addslashes($_GET["ids"]);
$url = "https://develop.roblox.com/v1/universes/multiget?ids=$ids&ids=$ids&ids=$ids";
echo file_get_contents($url);
?>