<?php
header('content-type:application/json');
echo json_encode(
	[
		'CreatorId' => 1,
		'CreatorType' => 'User',
		'PlaceVersion' => 1,
		'GameId' => 123456,
		'IsRobloxPlace' => true
	]
);
?>