<?php
error_reporting(~E_ALL);
$root = $_SERVER['DOCUMENT_ROOT'];
include "$root/functions.php";
header('content-type:application/json');

$placeid = $_GET["placeid"];
$ip = $_GET['ip'];
$port = $_GET['port'];
$id = $_GET['id'];
$username = $_GET['user'];
$app = $_GET['app'];
$membership = $_GET["membership"];

$a = [
	'ClientPort' => 0,
	'MachineAddress' => $ip,
	'ServerPort' => $port,
	'PingUrl' => '',
	'PingInterval' => 0,
	'UserName' => $username,
	'SeleniumTestMode' => false,
	'UserId' => intval($id),
	'SuperSafeChat' => false,
	'CharacterAppearance' => $app,
	'PlaceId' => intval($placeid),
	'MeasurementUrl' => '',
	'WaitingForCharacterGuid' => 'e01c22e4-a428-45f8-ae40-5058b4a1dafc',
	'BaseUrl' => $_SERVER['SERVER_NAME'],
	'ChatStyle' => 'ClassicAndBubble',
	'VendorId' => 0,
	'ScreenShotInfo' => '',
	'VideoInfo' => '<?xml version="1.0"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/" xmlns:yt="http://gdata.youtube.com/schemas/2007"><media:group><media:title type="plain"><![CDATA[ROBLOX Place]]></media:title><media:description type="plain"><![CDATA[ For more games visit http://www.roblox.com]]></media:description><media:category scheme="http://gdata.youtube.com/schemas/2007/categories.cat">Games</media:category><media:keywords>ROBLOX, video, free game, online virtual world</media:keywords></media:group></entry>',
	'CreatorId' => 1,
	'CreatorTypeEnum' => 'User',
	'MembershipType' => 'OutrageousBuildersClub',
	'AccountAge' => date_diff(new DateTime('2008-12-01T02:45Z'), new DateTime('now'))->days,
	'CookieStoreFirstTimePlayKey' => 'rbx_evt_ftp',
	'CookieStoreFiveMinutePlayKey' => 'rbx_evt_fmp',
	'CookieStoreEnabled' => false,
	'IsRobloxPlace' => true,
	'GenerateTeleportJoin' => false,
	'IsUnknownOrUnder13' => false,
	'SessionId' => '',
	'DataCenterId' => 0,
	'FollowUserId' => 0,
	'CharacterAppearanceId' => intval($id),
	'UniverseId' => 0,
];

// Removing the CRLF makes joins stall forever.
error_reporting(E_ALL);
echo sign("\r\n" . json_encode($a));
?>