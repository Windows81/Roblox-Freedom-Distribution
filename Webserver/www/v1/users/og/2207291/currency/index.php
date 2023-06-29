<?php
header("content-type:text/plain");
require ("/new/xampp/htdocs/corescripts/settings.php");
$httperrormsg404 = '{"errors":[{"code":0,"message":"Authorization has been denied for this request."}]}' 
?>
{"robux":<?php echo $robux ?>}