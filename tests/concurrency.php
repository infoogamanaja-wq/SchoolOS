<?php
require __DIR__.'/bootstrap.php';
if(!str_ends_with((string)g('SELECT DATABASE()'),'_test'))throw new RuntimeException('Disposable database required.');
$start='2030-02-15 10:00:00';q('INSERT INTO pp_slots(tenant_id,teacher_user_id,starts_at,ends_at) VALUES(1,3,?,?)',[$start,'2030-02-15 10:30:00']);$slot=(int)$pdo->lastInsertId();
$worker=tempnam(sys_get_temp_dir(),'booking-worker').'.php';
file_put_contents($worker,'<?php require '.var_export(__DIR__.'/bootstrap.php',true).'; date_default_timezone_set("Africa/Lagos"); $_SESSION=["csrf"=>"race", "u"=>q("SELECT * FROM users WHERE id=?",[(int)$argv[1]])->fetch()]; $_POST=["csrf"=>"race","pp_action"=>"book","child"=>(int)$argv[2],"slot_id"=>(int)$argv[3]];try{pp_action(pp_actor());echo "BOOKED";}catch(Throwable $e){echo "DENIED";}');
$workers=[];
foreach([[1,1],[4,3]] as [$user,$child]){
 $pipes=[];$proc=proc_open([PHP_BINARY,'-c',php_ini_loaded_file(),$worker,(string)$user,(string)$child,(string)$slot],[0=>['pipe','r'],1=>['pipe','w'],2=>['pipe','w']],$pipes);fclose($pipes[0]);$workers[]=[$proc,$pipes];
}
$out=[];foreach($workers as [$proc,$pipes]){$out[]=stream_get_contents($pipes[1]);$err=stream_get_contents($pipes[2]);fclose($pipes[1]);fclose($pipes[2]);if(proc_close($proc)!==0||$err)throw new RuntimeException('Worker failed: '.$err);}
unlink($worker);sort($out);if($out!==['BOOKED','DENIED']||(int)g("SELECT COUNT(*) FROM pp_bookings WHERE slot_id=? AND status='booked'",[$slot])!==1)throw new RuntimeException('Concurrent double booking.');echo "PASS two simultaneous parent requests produce one booking\nTOTAL 1 passed\n";
