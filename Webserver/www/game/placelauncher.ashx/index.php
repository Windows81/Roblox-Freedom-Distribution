<?php
$qs = $_SERVER['QUERY_STRING'];
header('content-type:application/json');
echo json_encode(
	[
		'jobId' => 'Test',
		'status' => 2,
		'joinScriptUrl' => "https://localhost/game/Join.ashx?$qs",
		'authenticationUrl' => 'http://localhost/Login/Negotiate.ashx',
		'authenticationTicket' => '1',
		'message' => NULL,
	]
);
?>