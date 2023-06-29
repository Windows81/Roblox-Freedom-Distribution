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
$url = "http://assetdelivery.roblox.com/v1/asset/?id=".$_GET['id'];
Header("Location: ".$url);
}
}
?>