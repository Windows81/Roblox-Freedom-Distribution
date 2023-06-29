<?php
header("content-type:text/plain");
error_reporting(0);
// just another simple httpget
$userid = addslashes($_GET["userIds"]);
$size = addslashes($_GET["size"]);
$format = addslashes($_GET["format"]);
$circlethingy = addslashes($_GET["isCircular"]);
$url = "https://thumbnails.roblox.com/v1/users/avatar?userIds=$userid&size=$size&format=$format&isCircular=$circlethingy ";
echo file_get_contents($url)
?>