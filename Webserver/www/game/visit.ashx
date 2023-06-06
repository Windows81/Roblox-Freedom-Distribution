<?php
error_reporting(~E_ALL);
require("functions.php");
header("content-type:text/plain");
$IsPlaySolo = $_GET["IsPlaySolo"];
$UserID = $_GET['UserID'];
$PlaceID = $_GET['PlaceID'];
$universeId = $_GET['universeId'];
$f1 = str_replace("%UserID%",$UserID,file_get_contents("./joinguest.txt"));
$f2 = str_replace("%PlaceID%",$PlaceID,$f1);
$f3 = str_replace("%universeId%",$universeId,$f2);
echo(sign($f3));
?>
