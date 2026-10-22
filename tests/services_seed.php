<?php
require __DIR__.'/bootstrap.php';if(getenv('SCHOOLOS_ALLOW_TEST_FIXTURES')!=='1'||!str_ends_with((string)g('SELECT DATABASE()'),'_test')||op_has('sv_roles'))throw new RuntimeException('Fresh disposable services database required.');
$pwd=password_hash('Local-test-password-2026!',PASSWORD_DEFAULT);foreach([[19,'librarian','Librarian'],[20,'stock','Stock Manager'],[21,'approver','Purchase Approver'],[22,'editor','Website Editor'],[23,'publisher','Website Approver'],[24,'comms','Communications Manager'],[25,'assets','Asset Manager']] as [$id,$name,$label])q("INSERT INTO users(id,tenant_id,email,role,name,password_hash) VALUES(?,1,?,'staff',?,?)",[$id,$name.'@test.local',$label,$pwd]);
echo "School Services accounts seeded; activation pending.\n";
