<?Php
$okmommento = file_get_contents("php://input");
file_put_contents("post.txt",$okmommento);
?>
{
    "browserTrackerId": 1,
    "appDeviceIdentifier": null
}