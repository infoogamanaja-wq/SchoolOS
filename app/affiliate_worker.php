<?php
// cPanel cron: php /absolute/path/public_html/affiliate_worker.php
if(PHP_SAPI!=='cli'){http_response_code(404);exit;}
define('SCHOOLOS_AFFILIATE_WORKER',true);require __DIR__.'/index.php';
