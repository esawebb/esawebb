<html>
  <body>
    <form action="process_form.php" method="post">
<?php
require_once('recaptchalib.php');
$publickey = "6LdumwAAAAAAAEZWIkpYzMNQllaL2haqkvbFPY4y";
echo recaptcha_get_html($publickey);
?>
    <br/>
    <input type="submit" value="submit" />
    </form>
  </body>
</html>
