<?php
header("content-type:text/plain");
echo file_get_contents("https://develop.roblox.com/v1/universes/4211103412/places?sortOrder=Asc&limit=10");
?>
