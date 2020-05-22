<?php

require_once('CheckUser.php');

$array = file("emails.txt");

foreach($array as $value){
 //echo $value;
 //$email = 'ahamano@flywheel.jp';
$email = $value;

$sender = 'webmaster@example.com';
$fqdn = 'fqdn.example.com';
$chk = new Mail_CheckUser($fqdn, $sender);
$result = $chk->checkEmail( $email );
if( $result ){ // $emailが有効かも？
  print 'OK, '.$email;
}else{ // $emailが有効ではないかも？
  print 'NG, '.$email;
  //print $chk->response_code;
  //print ': ';
  //print $chk->response;
  //var_dump($chk);
}

}
?>
