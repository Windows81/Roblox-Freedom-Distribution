<?php
require ("/new/xampp/htdocs/corescripts/settings.php");
header("content-type:text/plain");
$request_body = file_get_contents('php://input');
$ch = curl_init();
    
curl_setopt($ch, CURLOPT_URL, 'https://thumbnails.roblox.com/v1/batch');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_HEADER, false);
curl_setopt($ch, CURLOPT_POSTFIELDS, ''.$request_body.''
);

$headers = array();
$headers[] = 'Content-Type: application/json';
$headers[] = 'Accept: application/json';
 $headers[] =   'User-Agent: Roblox/WinInetRobloxApp/0.549.0.5490632 (GlobalDist; RobloxDirectDownload)';
$headers[] =    'Referer: https://thumbnails.roblox.com/docs/index.html';
   $headers[] = 'Origin: https://thumbnails.roblox.com';
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
$result = curl_exec($ch);
echo $result;
?>