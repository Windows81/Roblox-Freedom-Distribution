<?php
require("/new/xampp/htdocs/corescripts/settings.php");
header("content-type:text/plain");
$Method = "userlogin"
?>
{
  "user": {
    "id": <?php echo $userid ?>,
    "name": "<?php echo $username ?>.",
    "displayName": "<?php echo $displayname ?>"
  },
  "twoStepVerificationData": {
    "mediaType": "<?php echo $email ?>",
    "ticket": "1"
  },
  "identityVerificationLoginTicket": "1",
  "isBanned": true
}