<?php
$qs = $_SERVER['QUERY_STRING'];
Header("Location: /join?$qs");
?>