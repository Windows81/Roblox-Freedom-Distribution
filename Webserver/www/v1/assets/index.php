<?php
ob_start();
$id = (int)$_GET["id"];
$file = $id;
if (!file_exists($file)) {
    $file = "https://assetdelivery.roblox.com/v1/asset/?id=" . $id;
$file_name = $_GET['id'];
$myfile = fopen($file_name, "w");
file_put_contents($file_name,file_get_contents($file));
    header("location:" . $file);
}
readfile($file);
header("content-type:text/plain");
//btw everything below is so i dont have to change every single file's rbxsig
//i did have to change asset urls tho
$data = ob_get_clean();
$signature;
$key = file_get_contents("http://roblox.robloxlabs.com/game/PrivateKey.pem"); 
openssl_sign($data, $signature, $key, OPENSSL_ALGO_SHA1);
echo "--rbxsig" . sprintf("%%%s%%%s", base64_encode($signature), $data);
?>