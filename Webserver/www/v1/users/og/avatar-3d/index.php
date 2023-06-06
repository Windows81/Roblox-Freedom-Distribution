<?php
$id = addslashes($_GET["userId"]);
$url = file_get_contents("https://thumbnails.roblox.com/v1/users/avatar-3d?userId=$id");
echo $url
?>