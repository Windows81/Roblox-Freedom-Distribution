<?php
header("content-type: application/xml");
error_reporting(0);
$method = $_GET['method'];
switch($method) {
	case "IsFriendsWith":
		die('<Value Type="boolean">false</Value>');
		break;
	case "IsBestFriendsWith":
		die('<Value Type="boolean">false</Value>');
		break;
	case "IsInGroup":
		die('<Value Type="boolean">true</Value>');
		break;
	case "GetGroupRank":
		die('<Value Type="integer">100</Value>');
		break;
	case "GetGroupRole":
		die('');
		break;
};
?>