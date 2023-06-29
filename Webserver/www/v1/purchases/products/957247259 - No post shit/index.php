<?php
$clientdata = file_get_contents('php://input');
$url = "https://economy.roblox.com/v1/purchases/products/957247259";

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, $url);
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

$headers = array(
   "Accept: application/json",
   "Content-Type: application/json",
);
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

curl_setopt($curl, CURLOPT_POSTFIELDS, $clientdata);

$resp = curl_exec($curl);
curl_close($curl);

echo $resp;
?>