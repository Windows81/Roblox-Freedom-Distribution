<?php
require ("/new/xampp/htdocs/corescripts/settings.php");
header("content-type:text/plain");
echo file_get_contents("http://develop.sitetest4.robloxlabs.com/v1/user/universes?limit=50&sortOrder=Desc");
$jsonformat = '';
?>