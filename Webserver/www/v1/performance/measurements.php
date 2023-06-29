<?php
require ("/new/xampp/htdocs/corescripts/settings.php");
header("content-type:text/plain");
$v1 = file_get_contents("php://input");
file_put_contents("outsh.txt",$v1);
?>
{"wtfdoesthisreturnimgettingsomedamngibberishfrom2022m":"gaming"}