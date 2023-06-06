<?php
error_reporting(~E_ALL);
$root = $_SERVER['DOCUMENT_ROOT'];
include "$root/functions.php";
header("content-type:text/plain");
$f1 = file_get_contents("./thing.txt");
echo (sign($f1));
?>