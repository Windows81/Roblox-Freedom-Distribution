<?php
if(file_exists("./".$_GET["id"]))
{
    header("Content-type: text/plain");
    die(file_get_contents("./".$_GET['id']));
}
else
{
if (strstr($_GET['id'],'http'))
{
$url2 = $_GET['id'];
Header("Location: ".$url2);
}
else
{
$stringxd = $_GET['id'];
if (strstr($stringxd,'1111111'))
{
$s2=explode("1111111", $stringxd)[1];
$urlxd = "https://assetdelivery.roblox.com/v1/asset/?id=".$s2."&version=1";
Header("Location: ".$urlxd);
}
else
{
$url = "https://assetdelivery.roblox.com/v1/asset/?id=".$stringxd;
Header("Location: ".$url);
}
}
}
?>