<?php
/** cPanel maintenance: php experience_demo_refresh.php --confirm-isolated-demo */
if(PHP_SAPI!=='cli'){http_response_code(404);exit;}
if(($argv[1]??'')!=='--confirm-isolated-demo'){fwrite(STDERR,"Use --confirm-isolated-demo to replace only the marked, separately configured fictional demo. Never use production database credentials for this sandbox.\n");exit(1);}
define('SCHOOLOS_DEMO_REFRESH',true);require __DIR__.'/index.php';
