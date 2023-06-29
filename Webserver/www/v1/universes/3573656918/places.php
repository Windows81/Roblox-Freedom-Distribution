<?php
header("content-type:text/plain");
echo file_get_contents("https://develop.roblox.com/v1/universes/3573656918/places?sortOrder=Asc&limit=10");
?>
