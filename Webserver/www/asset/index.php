<?php
$root = $_SERVER['DOCUMENT_ROOT'];
include "$root/functions.php";

$id = $_GET['id'];
$path = "$root/_CACHE/$id";
$exists = file_exists($path) && 0 != filesize($path);

error_reporting(~E_ALL);
if ($exists) {
    header("Content-type: text/plain");
    die(file_get_contents($path));

} elseif (strstr($id, 'http')) {
    header("Location: $id");

} elseif (roblox_works()) {
    if (!$exists) {
        $url = "https://assetdelivery.roblox.com/v1/asset/?id=$id";
        file_put_contents($path, file_get_contents($url));
    }
    header("Content-type: text/plain");
    die(file_get_contents($path));
}
?>