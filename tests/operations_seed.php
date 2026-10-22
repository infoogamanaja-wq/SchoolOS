<?php
require __DIR__.'/bootstrap.php';
if(getenv('SCHOOLOS_ALLOW_TEST_FIXTURES')!=='1'||!str_ends_with((string)g('SELECT DATABASE()'),'_test')||op_has('op_roles'))throw new RuntimeException('Fresh disposable test database required.');
$pwd=password_hash('Local-test-password-2026!',PASSWORD_DEFAULT);
foreach([[13,1,'hr@test.local','staff','HR Reviewer'],[14,1,'driver@test.local','staff','Assigned Driver'],[15,1,'warden@test.local','staff','Assigned Warden'],[16,1,'otherdriver@test.local','staff','Other Driver'],[17,1,'otherwarden@test.local','staff','Other Warden'],[18,2,'foreignhr@test.local','school_admin','FOREIGN HR']] as $r)q('INSERT INTO users(id,tenant_id,email,role,name,password_hash) VALUES(?,?,?,?,?,?)',array_merge($r,[$pwd]));
echo "Operations accounts seeded; activation intentionally pending.\n";
