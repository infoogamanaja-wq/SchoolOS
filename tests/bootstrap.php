<?php
// Test database only. Configure SCHOOLOS_TEST_DSN / USER / PASSWORD for your local MariaDB.
$pdo=new PDO(getenv('SCHOOLOS_TEST_DSN')?:'mysql:host=localhost;dbname=schoolos_test;charset=utf8mb4',getenv('SCHOOLOS_TEST_USER')?:'root',getenv('SCHOOLOS_TEST_PASSWORD')?:'',[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]);
$pdo->exec("SET time_zone = '+01:00'");
function load_index_functions():void {
 $tokens=token_get_all(file_get_contents(__DIR__.'/../app/index.php'));$n=count($tokens);
 for($i=0;$i<$n;$i++)if(is_array($tokens[$i])&&$tokens[$i][0]===T_FUNCTION){
  $j=$i+1;while($j<$n&&is_array($tokens[$j])&&$tokens[$j][0]===T_WHITESPACE)$j++;
  if(!is_array($tokens[$j])||$tokens[$j][0]!==T_STRING)continue;
  $code='';$depth=0;$opened=false;
  for(;$i<$n;$i++){$tok=$tokens[$i];$text=is_array($tok)?($tok[0]===T_DIR?var_export(realpath(__DIR__.'/../app'),true):$tok[1]):$tok;$code.=$text;if($tok==='{'){$depth++;$opened=true;}elseif($tok==='}'){$depth--;if($opened&&$depth===0)break;}}
  eval($code);
 }
}
load_index_functions();
define('SCHOOLOS_PARENT_LIBRARY',true);require __DIR__.'/../app/parent_portal.php';
define('SCHOOLOS_FINANCE_ENGINE',true);require __DIR__.'/../app/finance_engine.php';
define('SCHOOLOS_LEARNING_LIBRARY',true);require __DIR__.'/../app/learning_portal.php';

define('SCHOOLOS_OPERATIONS_LIBRARY',true);
foreach(['operations_core.php','hr_payroll.php','transport_portal.php','boarding_portal.php'] as $module)require __DIR__.'/../app/'.$module;

define('SCHOOLOS_SERVICES_LIBRARY',true);
foreach(['services_core.php','library_manager.php','inventory_manager.php','engagement_manager.php','website_cms.php'] as $module)require __DIR__.'/../app/'.$module;

define('SCHOOLOS_INSIGHTS_LIBRARY',true);
foreach(['insights_core.php', 'intelligence_reports.php', 'school_innovations.php', 'academic_tools.php', 'school_wallet.php', 'governance_hub.php'] as $module)require __DIR__.'/../app/'.$module;

define('SCHOOLOS_EXPERIENCE',true);foreach(['experience.php','experience_ui.php','experience_admin.php','experience_demo.php'] as $module)require __DIR__.'/../app/'.$module;

foreach(['affiliate.php','public_site.php','public_guides.php'] as $module)require __DIR__.'/../app/'.$module;
