<?php
$qs = $_SERVER['QUERY_STRING'];
Header("Location: /marketplace/productinfo?$qs");
?>