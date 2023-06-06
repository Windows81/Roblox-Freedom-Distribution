<?php

header("content-type:text/plain");


ob_start();
?>
print 'tf'
<?php
$data = ob_get_clean();
$signature;
$key = file_get_contents("http://www.sitetest4.robloxlabs.com/game/privatekey.pem");
openssl_sign($data, $signature, $key, OPENSSL_ALGO_SHA1);
echo "--rbxsig" . sprintf("%%%s%%%s", base64_encode($signature), $data);

?>