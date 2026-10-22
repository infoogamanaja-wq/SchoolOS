<?php
/** cPanel cron: php /absolute/public_html/services_worker.php --tenant=1 --limit=30 */
if(PHP_SAPI!=='cli'){http_response_code(403);exit('CLI only.');}
$options=getopt('',['tenant:','limit:']);$tenant=(string)($options['tenant']??'');$limit=(string)($options['limit']??'30');if(!preg_match('/^[1-9]\d{0,9}$/D',$tenant)||!preg_match('/^\d{1,3}$/D',$limit)||(int)$limit<1||(int)$limit>100){fwrite(STDERR,"Use --tenant=ID --limit=1..100\n");exit(2);}
define('SCHOOLOS_SERVICES_WORKER',true);$_SERVER['REQUEST_METHOD']='GET';$_GET=[];$_POST=[];require __DIR__.'/index.php';
