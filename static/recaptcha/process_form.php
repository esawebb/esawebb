<html>
  <body>
<?php

require_once('recaptchalib.php');
$privatekey = "6LdumwAAAAAAAKnhn3eKNHTb_pHDdo68NOerS2tF";

$resp = recaptcha_check_answer ($privatekey,
                                $_SERVER["REMOTE_ADDR"],
                                $_POST["recaptcha_challenge_field"],
                                $_POST["recaptcha_response_field"]);

if (!$resp->is_valid) {
  die ("The reCAPTCHA wasn't entered correctly. Go back and try it again." .
       "(reCAPTCHA said: " . $resp->error . ")");
} else {
	echo "You got it";
}
?>
  </body>
</html>
