<?php
function is_connected()
{
    $connected = @fsockopen("assetdelivery.roblox.com", 80); 
                                        //website, port  (try 80 or 443)
    if ($connected){
        $is_conn = true; //action when connected
        fclose($connected);
    }else{
        $is_conn = false; //action in connection failure
    }
    return $is_conn;

}
if(is_connected() && !file_exists("./".$_GET["id"]) ||  ( 0 == filesize("./".$_GET["id"])) && is_connected())
{
$url = "https://assetdelivery.roblox.com/v1/asset/?id=".$_GET['id'];
$file_name = $_GET['id'];
$myfile = fopen($file_name, "w");
file_put_contents($file_name,file_get_contents($url));
//Header("Location: ".$url);
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
if(file_exists("./".$_GET["id"])) {
    header("Content-type: text/plain");
    die(file_get_contents("./".$_GET['id']));

}
}
}
?>