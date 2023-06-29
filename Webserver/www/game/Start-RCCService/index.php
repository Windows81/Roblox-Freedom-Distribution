<?php
$FFlag_OverRideYear = true;
//$year = addslashes($_GET["Year"]);
$year = "2019";
$str = "D:\new\clients\$year\rcc\RCCService2.exe -console -placeid:1818 -verbose -settingsfile";
$file = '"D:\new\clients\2019m\rcc\settings.json"';
$warning = 'Error:   Important !Your version of RCCService may be out of date. Please manually patch it.';
if($FFlag_OverRideYear == true){$str = "D:\new\clients\2018m[late]\RCCService.exe -console -verbose";}
exec("$str");
if($year > 2017)
{
echo "Started RCCService (JSON) at 26.76.93.232|53640,127.0.0.1|53640,25.63.106.176|53640.";
} 
else 
{
echo "Started RCCService (LUA) at 26.76.93.232|53640,127.0.0.1|53640,25.63.106.176|53640. ";
}
echo "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------";
echo $warning;
?>
