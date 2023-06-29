<?php
error_reporting(~E_ALL);
header("content-type:text/plain");
$user = $_GET['user'];
$membership = $_GET["membership"];
$ip = $_GET['ip'];
$port = $_GET['port'];
$user = $_GET['user'];
$id = $_GET['id'];
$app = $_GET['app'];
?>
{"jobId":"Test","status":2,"joinScriptUrl":"https://localhost/game/Join.ashx?placeid=1818&ip=<?php echo $ip ?>&port=<?php echo $port ?>&user=<?php echo $user ?>&id=<?php echo $id ?>&membership=<?php echo $membership ?>&app=<?php echo $app ?>","authenticationUrl":"http://localhost/Login/Negotiate.ashx","authenticationTicket":"1","message":null}
