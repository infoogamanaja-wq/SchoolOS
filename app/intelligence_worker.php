<?php
/** cPanel cron: php intelligence_worker.php TENANT_ID [LIMIT]. No HTTP entry point. */
if(PHP_SAPI!=='cli'){http_response_code(404);exit;}
$tenant=filter_var($argv[1]??null,FILTER_VALIDATE_INT,['options'=>['min_range'=>1]]);$limit=filter_var($argv[2]??20,FILTER_VALIDATE_INT,['options'=>['min_range'=>1,'max_range'=>100]]);if(!$tenant||!$limit){fwrite(STDERR,"Usage: php intelligence_worker.php TENANT_ID [1..100]\n");exit(1);}define('SCHOOLOS_INTELLIGENCE_WORKER',true);require __DIR__.'/index.php';
