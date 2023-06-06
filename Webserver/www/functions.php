<?php
function sign($script)
{
	$key = file_get_contents("./PrivateKey.pem");
	openssl_sign($script, $signature, $key, OPENSSL_ALGO_SHA1);
	return sprintf("--rbxsig%%%s%%%s", base64_encode($signature), $script);
}

function roblox_works()
{
	$connected = @fsockopen("assetdelivery.roblox.com", 80);
	//website, port  (try 80 or 443)
	if ($connected) {
		fclose($connected);
		return true;
	}
	return false;
}
?>