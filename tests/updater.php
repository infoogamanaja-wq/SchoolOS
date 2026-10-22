<?php
// Run with PHP 8.4 + zip. All deployments occur in a disposable temporary root.
define('SCHOOLOS_UPDATER_LIBRARY',true);require __DIR__.'/../app/system_manager.php';
$n=0;function ok($v,$label){global $n;if(!$v)throw new RuntimeException($label);echo 'PASS '.$label."\n";$n++;}
function rejects(callable $f,string $label){try{$f();}catch(Throwable $e){ok(true,$label);return;}throw new RuntimeException('Expected rejection: '.$label);}
$base=sys_get_temp_dir().'/schoolos-update-'.bin2hex(random_bytes(5));mkdir($base);mkdir($base.'/public');mkdir($base.'/storage/system',0700,true);file_put_contents($base.'/config.php','<?php return [];');
$old='<?php /* stable */ '.str_repeat(' ',110).'echo "stable";';file_put_contents($base.'/index.php',$old);chmod($base.'/index.php',0644);
file_put_contents($base.'/storage/system/version.json','{"version":"4.6.3"}');
function package(array $files,string $version='4.6.4',array $requires=[]):ZipArchive {
 $z=new ZipArchive();$path=tempnam(sys_get_temp_dir(),'soszip');$z->open($path,ZipArchive::OVERWRITE);$h=[];foreach($files as $f=>$b){$z->addFromString($f,$b);$h[$f]=hash('sha256',$b);}$z->addFromString('release.json',json_encode(['version'=>$version,'files'=>$h,'requires'=>$requires]));$z->close();$z=new ZipArchive();$z->open($path);unlink($path);return $z;
}
rejects(fn()=>sm_deploy($base,package(['index.php'=>'<?php syntax broken }']),'test'),'syntax rejected before activation');ok(file_get_contents($base.'/index.php')===$old,'stable index preserved after syntax failure');
rejects(fn()=>sm_deploy($base,package(['index.php'=>'<?php require __DIR__ . "/parent_portal.php";'.str_repeat(' ',100)]),'test'),'missing literal dependency rejected');
rejects(fn()=>sm_deploy($base,package(['index.php'=>$old],'4.6.4',['parent_portal.php']),'test'),'explicit missing dependency rejected');
rejects(fn()=>sm_deploy($base,package(['../index.php'=>'bad']),'test'),'traversal rejected');
rejects(fn()=>sm_deploy($base,package(['config.php'=>'bad']),'test'),'configuration overwrite rejected');
$z=package(['parent_portal.php'=>'<?php echo "portal";']);$z->addFromString('unexpected.php','<?php');rejects(fn()=>sm_deploy($base,$z,'test'),'undeclared payload rejected');
$z=package(['parent_portal.php'=>'<?php echo "portal";']);$z->addFromString('parent_portal.php','tampered');rejects(fn()=>sm_deploy($base,$z,'test'),'tampering rejected');
$z=package(['parent_portal.php'=>'<?php']);$z->setExternalAttributesName('parent_portal.php',ZipArchive::OPSYS_UNIX,0120777<<16);rejects(fn()=>sm_deploy($base,$z,'test'),'ZIP symlink rejected');
$link=tempnam(sys_get_temp_dir(),'external');symlink($link,$base.'/parent_portal.php');rejects(fn()=>sm_deploy($base,package(['parent_portal.php'=>'<?php']),'test'),'destination symlink rejected');unlink($base.'/parent_portal.php');unlink($link);
$new='<?php echo "release";'.str_repeat(' ',110);$files=['parent_portal.php'=>'<?php echo "family";','index.php'=>$new];
rejects(fn()=>sm_deploy($base,package($files),'test',function($f){if($f==='index.php')throw new RuntimeException('injected disk/activation failure');}),'activation failure rolls back');
ok(file_get_contents($base.'/index.php')===$old,'rollback restores stable index');ok(is_file($base.'/parent_portal.php'),'rollback retains new dependency');ok(json_decode(file_get_contents($base.'/storage/system/version.json'),true)['version']==='4.6.3','rollback restores version metadata');
$id=sm_deploy($base,package($files),'test');ok(file_get_contents($base.'/index.php')===$new,'valid update installed');ok((fileperms($base.'/index.php')&0777)===0644,'installed PHP mode 0644');
rejects(fn()=>sm_deploy($base,package($files),'test'),'same version rejected inside lock');
$lock=fopen($base.'/storage/system/update.lock','c');flock($lock,LOCK_EX);rejects(fn()=>sm_deploy($base,package($files,'4.6.5'),'test'),'concurrent update rejected');flock($lock,LOCK_UN);fclose($lock);
sm_rollback($base,$id);ok(file_get_contents($base.'/index.php')===$old,'manual rollback restores stable entry');ok(is_file($base.'/parent_portal.php'),'manual rollback does not delete portal');
// Simulated interrupted process: persisted applying journal and mixed live tree.
$id=sm_deploy($base,package($files),'test');$journal=$base.'/storage/system/backups/'.$id.'/transaction.json';$r=json_decode(file_get_contents($journal),true);$r['state']='applying';sm_json($journal,$r);sm_recover($base,$base.'/storage/system');ok(file_get_contents($base.'/index.php')===$old,'interrupted deployment recovered from journal');
ok(is_file($base.'/storage/.htaccess'),'backup storage protected');
// Restore only from verified bytes, never corrupt a healthy live entry from bad backup.
$id=sm_deploy($base,package($files),'test');file_put_contents($base.'/storage/system/backups/'.$id.'/index.php','corrupt');rejects(fn()=>sm_rollback($base,$id),'corrupted backup rejected');ok(file_get_contents($base.'/index.php')===$new,'corrupt backup cannot overwrite live index');
echo "TOTAL $n passed\n";
