<?php
error_reporting(0);
header("content-type:text/plain");
$limit = addslashes($_GET["limit"]);
if($limit == NULL){$limit = "53";};
$url = "https://develop.roblox.com/v1/gametemplates?limit=$limit";
$theR = file_get_contents($url);
echo $theR
?>