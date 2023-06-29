<?Php
$v2 = $_POST;
$v1 =  file_get_contents("php://input");
file_put_contents("outsh.txt",$v1);
?>
