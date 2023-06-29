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

{"ClientPort":0,"MachineAddress":"<?php echo $ip ?>","ServerPort":<?php echo $port ?>,"PingUrl":"","PingInterval":120,"UserName":"<?php echo $username ?>","SeleniumTestMode":false,"UserId":<?php echo $userid ?>,"SuperSafeChat":false,"CharacterAppearance":"http://assetgame.sitetest4.robloxlabs.com.com/Asset/CharacterFetch.ashx?userId=<?php echo $userid ?>&placeId=0","ClientTicket":"5/20/2016 1:42:15 PM;NrIIE25IsF2FrEN4ndNMVfz5zeYW5jp1uql+gmz5lShAWUKHE+n3CGaK6V9goXbzw2R/SOy/hQ9OT/y72b7Yoty8z4RVXlDEewn0rOado2wGs2kqzQqjtwMWiwBJi0HZ2HAS8xlX2Tpp1GhEdONem7SVFcqzHsUufPqKySxBBTI=;WUraepy1LfhrnjYgRbn9rQKckP+1AXpMEHAIuFvee6Al8HB+ss7w57REuUhqkIKRgNlKfobF6drSyeHPg/XZfH34/BqkPgQ9vykootvdJKHlPeran+qvGQ2icUqG3EE+/ZUZ3hAHZ5Kc3vsMpx6axbXSJV+mDElM8ej3X9mP/Fo=","GameId":"00000000-0000-0000-0000-000000000000","PlaceId":1818,"MeasurementUrl":"","WaitingForCharacterGuid":"16be1dd8-5462-4ca5-a997-0725d997708b","BaseUrl":"http://www.sitetest4.robloxlabs.com/","ChatStyle":"Classic","VendorId":0,"ScreenShotInfo":"","VideoInfo":"<?xml version=\"1.0\"?><entry xmlns=\"http://www.w3.org/2005/Atom\" xmlns:media=\"http://search.yahoo.com/mrss/\" xmlns:yt=\"http://gdata.youtube.com/schemas/2007\"><media:group><media:title type=\"plain\"><![CDATA[ROBLOX Place]]></media:title><media:description type=\"plain\"><![CDATA[ For more games visit http://www.roblox.com]]></media:description><media:category scheme=\"http://gdata.youtube.com/schemas/2007/categories.cat\">Games</media:category><media:keywords>ROBLOX, video, free game, online virtual world</media:keywords></media:group></entry>","CreatorId":1,"CreatorTypeEnum":"User","MembershipType":"<?Php echo $membership ?>","AccountAge":0,"CookieStoreFirstTimePlayKey":"rbx_evt_ftp","CookieStoreFiveMinutePlayKey":"rbx_evt_fmp","CookieStoreEnabled":true,"IsRobloxPlace":true,"GenerateTeleportJoin":false,"IsUnknownOrUnder13":false,"SessionId":"084fe2bc-2a6e-423c-bc2a-0ed876f7c274|00000000-0000-0000-0000-000000000000|0|204.236.226.210|8|2016-05-20T18:42:15.3704607Z|0|null|null","DataCenterId":1,"UniverseId":1,"BrowserTrackerId":1,"UsePortraitMode":false,"FollowUserId":1}

<?php
$data = ob_get_clean();
$signature;
$key = file_get_contents("http://www.sitetest4.robloxlabs.com/game/privatekey.pem");
openssl_sign($data, $signature, $key, OPENSSL_ALGO_SHA1);
echo "--rbxsig" . sprintf("%%%s%%%s", base64_encode($signature), $data);

?>
