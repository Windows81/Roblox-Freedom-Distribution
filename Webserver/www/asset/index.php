<?php
$root = $_SERVER['DOCUMENT_ROOT'];
include "$root/functions.php";

$id = $_GET['id'];
$exists = file_exists("./$id") && 0 != filesize("./$id");

if ($exists) {
    header("Content-type: text/plain");
    die(file_get_contents("./$id"));

} elseif (strstr($id, 'http')) {
    header("Location: $id");

} elseif (roblox_works()) {
    if ($exists) {
        $url = "https://assetdelivery.roblox.com/v1/asset/?id=$id";
        $file_name = $id;
        file_put_contents($file_name, file_get_contents($url));
        header("Content-type: text/plain");
        die(file_get_contents("./$id"));
    }
}
?>