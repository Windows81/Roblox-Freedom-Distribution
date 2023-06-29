<?php
function sign($script) {
    $signature;
$key = file_get_contents("./PrivateKey.pem");
openssl_sign($script,$signature,$key,OPENSSL_ALGO_SHA1);
return "--rbxsig".sprintf("%%%s%%%s",base64_encode($signature),$script);
}
?>
