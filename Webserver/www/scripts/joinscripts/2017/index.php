<?php

header("content-type:text/plain");

$year = addslashes($_GET["year"]);
$username = addslashes($_GET["username"]);
$ip = addslashes($_GET["ip"]);
$port = addslashes($_GET["port"]);
$userid = addslashes($_GET["id"]);
$membership = addslashes($_GET["membership"]);
ob_start();
?>

{"ClientPort":0,"MachineAddress":"<?php echo $ip ?>","ServerPort":<?php echo $port ?>,"PingUrl":"","PingInterval":120,"UserName":"<?php echo $username ?>","SeleniumTestMode":false,"UserId":<?php echo $userid ?>,"SuperSafeChat":false,"CharacterAppearance":"https://api.sitetest4.robloxlabs.com/v1.1/avatar-fetch/?placeId=0&userId=<?php echo $userid ?>","ClientTicket":"7/6/2017 9:04:32 PM;LwnuNTnJ5vPWiUUFG/f+0U5A8uogqDQYQNQRf8G7tyapDv89tTRIrd7fqStXbGOrjI0rY0rUapynncc6OeWE/5pMhn/o03SmWkpNC/Xi+zo6SoeopAJX0q8yqSKGSIYzrMO/zh0YL8cwwdzpLSrFD0WdB8ouERSOqaEbKBB/XmE=;mAtDgbq2cODsN/Xz1lDbCxgqgj+i/09SR+JA8S96AQsZ26ZE45RmhsXGUsS3VY96/7iiMb0A0Quo0SRzppfduARmhlM+0u2v6ynxu4GHvbg/krrNV5uemeS9wE5KzbNKlctizoNYpvCR7iwa1js1Dnfcm4X0OB2uKMelWtQFyA8=","GameId":"00000000-0000-0000-0000-000000000000","PlaceId":1818,"MeasurementUrl":"","WaitingForCharacterGuid":"3fe16da3-decf-482b-8680-99a24914f8d7","BaseUrl":"http://www.sitetest4.robloxlabs.com/","ChatStyle":"ClassicAndBubble","VendorId":0,"ScreenShotInfo":"","VideoInfo":"<?xml version=\"1.0\"?><entry xmlns=\"http://www.w3.org/2005/Atom\" xmlns:media=\"http://search.yahoo.com/mrss/\" xmlns:yt=\"http://gdata.youtube.com/schemas/2007\"><media:group><media:title type=\"plain\"><![CDATA[ROBLOX Place]]></media:title><media:description type=\"plain\"><![CDATA[ For more games visit http://www.roblox.com]]></media:description><media:category scheme=\"http://gdata.youtube.com/schemas/2007/categories.cat\">Games</media:category><media:keywords>ROBLOX, video, free game, online virtual world</media:keywords></media:group></entry>","CreatorId":1,"CreatorTypeEnum":"User","MembershipType":"<?php echo $membership ?>","AccountAge":69420,"CookieStoreFirstTimePlayKey":"rbx_evt_ftp","CookieStoreFiveMinutePlayKey":"rbx_evt_fmp","CookieStoreEnabled":true,"IsRobloxPlace":true,"GenerateTeleportJoin":false,"IsUnknownOrUnder13":false,"GameChatType":"AllUsers","SessionId":"04f7f4a9-7325-4e18-9315-7b9a0fa434c1|00000000-0000-0000-0000-000000000000|0|34.207.98.73|8|2017-07-07T02:04:31.8714196Z|0|null|null|null|null|null","DataCenterId":0,"UniverseId":0,"BrowserTrackerId":0,"UsePortraitMode":false,"FollowUserId":0,"characterAppearanceId":<?php echo $userid ?>}

<?php
$data = ob_get_clean();
$signature;
$key = file_get_contents("http://www.sitetest4.robloxlabs.com/game/privatekey.pem");
openssl_sign($data, $signature, $key, OPENSSL_ALGO_SHA1);
echo "--rbxsig" . sprintf("%%%s%%%s", base64_encode($signature), $data);

?>
