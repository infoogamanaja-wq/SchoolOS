<?php
// Embedded in system_manager.php at package build time: no bootstrap dependency.
function sm_allow(): array {return ['affiliate.php','affiliate_worker.php','public_site.php','public_site.css','public_site.js','public_guides.php','public_guides.json','website-owner.png','website-onboarding.png','website-parent.png','index.php','experience.php','experience_ui.php','experience_admin.php','experience_demo.php','experience_demo_refresh.php','experience.css','experience.js','system_manager.php','school_logo_handler.php','finance_engine.php','finance_view.php','parent_portal.php','learning_portal.php','operations_core.php','hr_payroll.php','transport_portal.php','boarding_portal.php','services_core.php','library_manager.php','inventory_manager.php','engagement_manager.php','website_cms.php','insights_core.php','intelligence_reports.php','school_innovations.php','academic_tools.php','school_wallet.php','governance_hub.php','intelligence_worker.php','public/offline/offline_teacher.html','public/offline/offline_teacher.js','public/offline/advanced_sw.js','services_worker.php','services_push_worker.js','public/manifest.webmanifest','public/sw.js','dashboard.html','login.html','register.html','onboarding.html','VERSION.txt'];}
function sm_json(string $path, array $data): void {
 $tmp=$path.'.'.bin2hex(random_bytes(8)).'.tmp';
 try { $bytes=json_encode($data,JSON_PRETTY_PRINT|JSON_THROW_ON_ERROR);if(file_put_contents($tmp,$bytes,LOCK_EX)!==strlen($bytes)||!chmod($tmp,0600)||!rename($tmp,$path))throw new RuntimeException('Metadata write failed.'); }
 finally {if(is_file($tmp))unlink($tmp);}
}
function sm_target(string $root,string $file): string {
 if(!in_array($file,sm_allow(),true))throw new RuntimeException('Unapproved destination.');
 $path=$root.'/'.$file;
 if(is_link($path))throw new RuntimeException('Unsafe destination: '.$file);
 $parent=dirname($file);$current=$root;
 if($parent!=='.')foreach(explode('/',$parent) as $part){$current.='/'.$part;if(is_link($current)||(file_exists($current)&&(!is_dir($current)||realpath($current)!==$current)))throw new RuntimeException('Unsafe destination: '.$file);if(!file_exists($current)&&$current!==$root.'/public/offline')throw new RuntimeException('Unsafe destination: '.$file);}
 if(!is_dir(dirname($path))&&$parent!=='public/offline')throw new RuntimeException('Unsafe destination: '.$file);
 return $path;
}
function sm_atomic(string $target,string $bytes,int $mode=0644): void {
 $tmp=$target.'.'.bin2hex(random_bytes(8)).'.smnew';
 try {
  $f=fopen($tmp,'xb');if(!$f)throw new RuntimeException('Cannot stage '.$target);
  try {if(fwrite($f,$bytes)!==strlen($bytes)||!fflush($f)||(function_exists('fsync')&&!fsync($f)))throw new RuntimeException('Incomplete staged write.');}finally{fclose($f);}
  if(!chmod($tmp,$mode)||hash_file('sha256',$tmp)!==hash('sha256',$bytes))throw new RuntimeException('Staging integrity failed.');
  if(!rename($tmp,$target))throw new RuntimeException('Atomic activation failed.');
  clearstatcache(true,$target);
  if(!is_file($target)||!is_readable($target)||hash_file('sha256',$target)!==hash('sha256',$bytes))throw new RuntimeException('Activation integrity failed.');
  if(function_exists('opcache_invalidate'))opcache_invalidate($target,true);
 } finally {if(is_file($tmp))unlink($tmp);}
}
function sm_archive(ZipArchive $zip): array {
 if($zip->numFiles>200)throw new RuntimeException('Too many archive entries.');
 $names=[];$total=0;
 for($i=0;$i<$zip->numFiles;$i++){
  $s=$zip->statIndex($i);$n=$s['name'];$ops=0;$attr=0;$zip->getExternalAttributesIndex($i,$ops,$attr);
  if(!preg_match('~^[A-Za-z0-9_./-]+$~D',$n)||str_contains($n,'..')||str_starts_with($n,'/')||str_contains($n,'//')||isset($names[$n])||(($attr>>16)&0170000)===0120000)throw new RuntimeException('Unsafe or duplicate ZIP entry.');
  if(($s['size']??0)>8*1024*1024||($total+=$s['size'])>30*1024*1024)throw new RuntimeException('Archive too large.');
  $names[$n]=true;
 }
 return $names;
}
function sm_restore(string $root,string $backup,array $record): array {
 $errors=[];$files=$record['before'];uksort($files,fn($a,$b)=>($a==='index.php'?1:0)<=>($b==='index.php'?1:0));
 foreach($files as $file=>$info){try{
  $target=sm_target($root,$file);
  if($info===null)continue; // Never delete a newly installed dependency during recovery.
  $old=$backup.'/'.$file;
  if(!is_file($old)||is_link($old)||hash_file('sha256',$old)!==$info['sha256'])throw new RuntimeException('Backup checksum mismatch.');
  sm_atomic($target,file_get_contents($old),$info['mode']);
 }catch(Throwable $e){$errors[]=$file.': '.$e->getMessage();}}
 if(!$errors){try{sm_atomic($root.'/storage/system/version.json',$record['version_before']??'{"version":"1.1.0"}',0600);}catch(Throwable $e){$errors[]='version metadata';}}
 return $errors;
}
function sm_recover(string $root,string $system): void {
 foreach(glob($system.'/backups/*/transaction.json')?:[] as $path){
  $r=json_decode(file_get_contents($path),true,512,JSON_THROW_ON_ERROR);
  if(!in_array($r['state']??'', ['prepared','applying','recovery_required'],true))continue;
  $errors=sm_restore($root,dirname($path),$r);
  $r['state']=$errors?'recovery_required':'rolled_back';$r['recovery_errors']=$errors;sm_json($path,$r);
  if($errors)throw new RuntimeException('Manual recovery required. See transaction journal.');
 }
}
function sm_deploy(string $root, ZipArchive $zip, string $checksum, ?callable $testHook=null): string {
 $root=realpath($root);if(!$root)throw new RuntimeException('Missing application root.');
 $system=$root.'/storage/system';if(!is_dir($system)&&!mkdir($system,0700,true))throw new RuntimeException('Cannot create private system storage.');
 if(is_link($system)||realpath($system)!==$system)throw new RuntimeException('Unsafe system storage.');
 // Protect backups/configuration even when the uploaded installation omitted .htaccess.
 sm_atomic($root.'/storage/.htaccess',"Require all denied\n",0644);
 $lock=fopen($system.'/update.lock','c');if(!$lock||!flock($lock,LOCK_EX|LOCK_NB))throw new RuntimeException('Another deployment is running.');
 try{
  sm_recover($root,$system);
  $names=sm_archive($zip);$manifest=json_decode($zip->getFromName('release.json')?:'',true);
  if(!is_array($manifest)||!preg_match('/^\d+\.\d+\.\d+$/D',(string)($manifest['version']??''))||!is_array($manifest['files']??null)||!$manifest['files'])throw new RuntimeException('Invalid release manifest.');
  $current=is_file($system.'/version.json')?json_decode(file_get_contents($system.'/version.json'),true,512,JSON_THROW_ON_ERROR):['version'=>'1.1.0'];
  if(version_compare($manifest['version'],$current['version'],'<='))throw new RuntimeException('Release must be newer than installed version.');
  $bytes=[];
  foreach($manifest['files'] as $file=>$hash){
   sm_target($root,$file);
   if(!isset($names[$file])||!is_string($hash)||!preg_match('/^[a-f0-9]{64}$/D',$hash))throw new RuntimeException('Missing file or invalid hash.');
   $data=$zip->getFromName($file);if($data===false||!hash_equals($hash,hash('sha256',$data)))throw new RuntimeException('File hash mismatch: '.$file);
   if(str_ends_with($file,'.php')){if(!str_starts_with($data,'<?php'))throw new RuntimeException('Invalid PHP header.');token_get_all($data,TOKEN_PARSE);}
   $bytes[$file]=$data;
  }
  foreach($names as $name=>$_)if($name!=='release.json'&&!isset($bytes[$name]))throw new RuntimeException('Undeclared archive payload.');
  // Explicit dependencies supplement literal PHP include discovery.
  $dependencies=$manifest['requires']??[];if(!is_array($dependencies))throw new RuntimeException('Invalid dependencies.');
  $prospective=$bytes['index.php']??@file_get_contents($root.'/index.php');
  if(!is_string($prospective)||strlen($prospective)<100)throw new RuntimeException('Invalid prospective entry point.');
  $scan=$bytes+['index.php'=>$prospective];
  foreach($scan as $file=>$data)if(str_ends_with($file,'.php')){
   preg_match_all('~(?:require|include)(?:_once)?\s*\(?\s*__DIR__\s*\.\s*[\x27\x22]/([a-zA-Z0-9_./-]+\.php)[\x27\x22]~',$data,$matches);
   $dependencies=array_merge($dependencies,$matches[1]);
  }
  foreach(array_unique($dependencies) as $dep){
   if($dep==='config.php'){if(!is_file($root.'/config.php'))throw new RuntimeException('Missing configuration.');continue;}
   sm_target($root,$dep);if(!isset($bytes[$dep])&&(!is_file($root.'/'.$dep)||!is_readable($root.'/'.$dep)))throw new RuntimeException('Missing required dependency: '.$dep);
  }
  if(!is_file($root.'/index.php')||filesize($root.'/index.php')<100)throw new RuntimeException('Restore the existing index.php before updating.');
  // Only the fixed static offline directory may be introduced, after payload verification.
  foreach(array_keys($bytes) as $file){$target=sm_target($root,$file);if(!is_dir(dirname($target))&&(!mkdir(dirname($target),0755)||realpath(dirname($target))!==$root.'/public/offline'))throw new RuntimeException('Cannot prepare offline static directory.');}
  $id=gmdate('Ymd_His').'_'.bin2hex(random_bytes(6));$backup=$system.'/backups/'.$id;
  if(!mkdir($backup,0700,true))throw new RuntimeException('Backup directory failed.');
  $record=['state'=>'prepared','version'=>$manifest['version'],'checksum'=>$checksum,'after'=>$manifest['files'],'before'=>[], 'version_before'=>is_file($system.'/version.json')?file_get_contents($system.'/version.json'):null,'created_at'=>gmdate('c')];
  foreach(array_unique(array_merge(array_keys($bytes),['index.php'])) as $file){
   $target=sm_target($root,$file);$record['before'][$file]=null;
   if(is_file($target)){
    $dest=$backup.'/'.$file;if(!is_dir(dirname($dest))&&!mkdir(dirname($dest),0700,true))throw new RuntimeException('Backup directory failed.');
    if(!copy($target,$dest)||!chmod($dest,0600)||hash_file('sha256',$dest)!==hash_file('sha256',$target))throw new RuntimeException('Backup verification failed.');
    $record['before'][$file]=['sha256'=>hash_file('sha256',$dest),'mode'=>fileperms($target)&0777];
   }
  }
  sm_json($backup.'/transaction.json',$record);
  try{
   $record['state']='applying';sm_json($backup.'/transaction.json',$record);
   // Dependencies first; entry point last. Never move/unlink the live entry point.
   uksort($bytes,fn($a,$b)=>($a==='index.php'?1:0)<=>($b==='index.php'?1:0));
   foreach($bytes as $file=>$data){sm_atomic(sm_target($root,$file),$data);if($testHook)$testHook($file);}
   foreach($manifest['files'] as $file=>$hash)if(hash_file('sha256',$root.'/'.$file)!==$hash)throw new RuntimeException('Post-activation integrity failure.');
   sm_json($system.'/version.json',['version'=>$manifest['version'],'backup'=>$id,'checksum'=>$checksum,'updated_at'=>gmdate('c')]);
   $record['state']='committed';sm_json($backup.'/transaction.json',$record);
   return $id;
  }catch(Throwable $e){
   $errors=sm_restore($root,$backup,$record);$record['state']=$errors?'recovery_required':'rolled_back';$record['failure']=$e->getMessage();$record['recovery_errors']=$errors;sm_json($backup.'/transaction.json',$record);
   throw new RuntimeException('Update rolled back: '.$e->getMessage().($errors?' MANUAL RECOVERY REQUIRED.':''),0,$e);
  }
 }finally{flock($lock,LOCK_UN);fclose($lock);}
}
function sm_rollback(string $root,string $id): void {
 if(!preg_match('/^\d{8}_\d{6}_[a-f0-9]{12}$/D',$id))throw new RuntimeException('Invalid backup ID.');
 $system=$root.'/storage/system';$lock=fopen($system.'/update.lock','c');if(!$lock||!flock($lock,LOCK_EX|LOCK_NB))throw new RuntimeException('Another deployment is running.');
 try{
  $current=json_decode(file_get_contents($system.'/version.json'),true,512,JSON_THROW_ON_ERROR);
  if(($current['backup']??'')!==$id)throw new RuntimeException('Only the current release can be rolled back.');
  $path=$system.'/backups/'.$id.'/transaction.json';$r=json_decode(file_get_contents($path),true,512,JSON_THROW_ON_ERROR);
  if(($r['state']??'')!=='committed')throw new RuntimeException('Backup is not a committed deployment.');
  $r['state']='recovery_required';sm_json($path,$r);$errors=sm_restore($root,dirname($path),$r);
  if($errors)throw new RuntimeException('Manual recovery required: '.implode(', ',$errors));
  $r['state']='rolled_back';sm_json($path,$r);
 }finally{flock($lock,LOCK_UN);fclose($lock);}
}

if(defined('SCHOOLOS_UPDATER_LIBRARY'))return;

// Direct access goes through the authenticated dashboard router.
if (!defined("SCHOOLOS_DASHBOARD_ROUTER")) { header("Location: index.php?s=system", true, 302); exit; }
// Included from index.php after authentication. Platform Super Admin only.
if (!isset($u) || ($u['role'] ?? '') !== 'platform_super_admin') { http_response_code(403); exit('Forbidden'); }
$root=__DIR__; $systemDir=$root.'/storage/system';
if (!is_dir($systemDir)) mkdir($systemDir,0700,true);
function sm_notice($s){return '<div class="card" style="margin:12px 0">'.htmlspecialchars($s,ENT_QUOTES,'UTF-8').'</div>';}
function sm_read($p,$default=[]){if(!is_file($p))return $default;$x=json_decode(file_get_contents($p),true);return is_array($x)?$x:$default;}
function sm_write($p,$v){$tmp=$p.'.tmp';if(file_put_contents($tmp,json_encode($v,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES),LOCK_EX)===false||!chmod($tmp,0600)||!rename($tmp,$p))throw new RuntimeException('Unable to save system metadata.');}
function sm_validzip($zip,$prefix,$limit=200){return array_keys(sm_archive($zip));}
function sm_zipupload(){if(!isset($_FILES['package'])||$_FILES['package']['error']!==UPLOAD_ERR_OK)throw new RuntimeException('ZIP upload failed.');if($_FILES['package']['size']>12*1024*1024)throw new RuntimeException('ZIP upload too large.');$z=new ZipArchive();if($z->open($_FILES['package']['tmp_name'])!==true)throw new RuntimeException('Invalid ZIP file.');return $z;}
$msg='';$registry=$systemDir.'/plugins.json';$plugins=sm_read($registry);
if($_SERVER['REQUEST_METHOD']==='POST'&&isset($_POST['sm_action'])){
 try{
 if(!hash_equals($_SESSION['csrf'],(string)($_POST['csrf']??'')))throw new RuntimeException('Invalid security token.');
 $action=$_POST['sm_action'];
 if($action==='install_plugin'){
  $z=sm_zipupload();$names=sm_validzip($z,'');if(!in_array('plugin.json',$names,true))throw new RuntimeException('Missing plugin.json.');$m=json_decode($z->getFromName('plugin.json'),true);
  if(!is_array($m)||!preg_match('/^[a-z][a-z0-9_-]{2,40}$/',$m['id']??'')||!is_string($m['name']??null)||strlen($m['name'])>100)throw new RuntimeException('Invalid plugin manifest.');
  $id=$m['id'];if(isset($plugins[$id]))throw new RuntimeException('Plugin already installed.');
  foreach($names as $n){if(!in_array($n,['plugin.json','README.md','settings.json'],true))throw new RuntimeException('Only declarative plugin files are supported. PHP execution is blocked.');}
  $dest=$systemDir.'/plugins/'.$id;if(!is_dir($dest))mkdir($dest,0700,true);
  foreach($names as $n){if(str_ends_with($n,'/'))continue;file_put_contents($dest.'/'.$n,$z->getFromName($n),LOCK_EX);}
  $plugins[$id]=['name'=>$m['name'],'version'=>(string)($m['version']??'1.0.0'),'enabled'=>false,'installed_at'=>gmdate('c')];sm_write($registry,$plugins);$z->close();$msg='Plugin package installed. Enable it below. Declarative plugins do not execute arbitrary code.';
 }elseif($action==='toggle_plugin'){
  $id=(string)($_POST['id']??'');if(!isset($plugins[$id]))throw new RuntimeException('Unknown plugin.');$plugins[$id]['enabled']=!$plugins[$id]['enabled'];sm_write($registry,$plugins);$msg='Plugin state updated.';
 }elseif($action==='install_update'){
  if(($_POST['confirm_release']??'')!=='yes')throw new RuntimeException('Confirm the release source.');
  $z=sm_zipupload();
  try{$id=sm_deploy($root,$z,hash_file('sha256',$_FILES['package']['tmp_name']));}finally{$z->close();}
  $msg='Update verified and installed. Backup: '.$id.'. No database records changed.';
 }elseif($action==='rollback_update'){
  sm_rollback($root,(string)($_POST['backup_id']??''));$msg='Previous files restored. New dependencies retained; database unchanged.';
 }else throw new RuntimeException('Unknown action.');
 }catch(Throwable $ex){$msg='Error: '.$ex->getMessage();}
}
$version=sm_read($systemDir.'/version.json',['version'=>'1.1.0']);
if(!empty($version['backup'])&&preg_match('/^\d{8}_\d{6}_[a-f0-9]{12}$/D',$version['backup']))echo '<div class="card"><h2>Rollback current update</h2><p>Restores verified previous files; preserves all database records and newly added dependencies.</p><form method="post"><input type="hidden" name="csrf" value="'.e($_SESSION['csrf']).'"><input type="hidden" name="sm_action" value="rollback_update"><input type="hidden" name="backup_id" value="'.e($version['backup']).'"><button class="btn">Restore previous release</button></form></div>';

echo '<h1>System Management</h1><p class="muted">Platform Super Admin · Update packages and declarative plugins</p>'.($msg?sm_notice($msg):'');
echo '<div class="card"><h2>Core updates</h2><p>Installed version: <b>'.e($version['version']).'</b></p><p class="muted">Upload a trusted SchoolOS release ZIP containing release.json and approved application files. Only install update ZIPs obtained from your trusted SchoolOS publisher. File hashes are checked automatically; the ZIP itself is not digitally signed in this edition. Existing files are backed up. Updates requiring database migrations must be handled separately.</p><form method="post" enctype="multipart/form-data"><input type="hidden" name="csrf" value="'.e($_SESSION['csrf']).'"><input type="hidden" name="sm_action" value="install_update"><p><label>Release ZIP <input type="file" name="package" accept=".zip" required></label></p><p><label><input type="checkbox" name="confirm_release" value="yes" required> I trust the source of this update ZIP and have a backup.</label></p><button class="btn">Verify & Install Update</button></form></div><br>';
echo '<div class="card"><h2>Plugin manager</h2><p class="muted">Only safe declarative plugin packages are accepted. This edition does not execute uploaded PHP plugins or automatically add dashboard modules.</p><form method="post" enctype="multipart/form-data"><input type="hidden" name="csrf" value="'.e($_SESSION['csrf']).'"><input type="hidden" name="sm_action" value="install_plugin"><input type="file" name="package" accept=".zip" required> <button class="btn">Install Plugin Package</button></form><br><table class="table"><tr><th>Plugin</th><th>Version</th><th>Status</th><th>Action</th></tr>';
foreach($plugins as $id=>$p){echo '<tr><td>'.e($p['name']).' <small>'.e($id).'</small></td><td>'.e($p['version']).'</td><td>'.($p['enabled']?'Enabled':'Disabled').'</td><td><form method="post"><input type="hidden" name="csrf" value="'.e($_SESSION['csrf']).'"><input type="hidden" name="sm_action" value="toggle_plugin"><input type="hidden" name="id" value="'.e($id).'"><button class="btn">'.($p['enabled']?'Disable':'Enable').'</button></form></td></tr>';}
echo '</table></div>';
