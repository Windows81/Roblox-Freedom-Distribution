<?php
$userids = addslashes($_GET["userIds"]);
$format = addslashes($_GET["format"]);
$imgsize = addslashes($_GET["size"]);
$url = "https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds=$userids&format=$format&size=$imgsize"
?>
<?php
header("Location: $url"); 
?>
