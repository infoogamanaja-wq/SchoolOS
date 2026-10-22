<?php
/** Read-only cPanel cron helper. Keep this script and baseline OUTSIDE public_html. */
if(PHP_SAPI!=='cli'){http_response_code(403);exit;}
if($argc!==3){fwrite(STDERR,"Usage: php integrity_check.php /absolute/public_html /private/release.json\n");exit(2);}
$root=realpath($argv[1]);$m=json_decode(file_get_contents($argv[2]),true,512,JSON_THROW_ON_ERROR);$failed=false;$results=[];
if(!$root||!is_dir($root)||!isset($m['files']['index.php'],$m['files']['parent_portal.php'])){fwrite(STDERR,"Expected application root and full portal release manifest.\n");exit(2);}
foreach(['index.php','parent_portal.php','system_manager.php','finance_engine.php'] as $file){
 if(!isset($m['files'][$file]))continue;$path=$root.'/'.$file;clearstatcache(true,$path);$exists=is_file($path);$hash=$exists?hash_file('sha256',$path):null;
 $good=$exists&&!is_link($path)&&is_readable($path)&&hash_equals($m['files'][$file],(string)$hash);$failed=$failed||!$good;
 $results[$file]=['ok'=>$good,'exists'=>$exists,'sha256'=>$hash,'inode'=>$exists?fileinode($path):null,'mode'=>$exists?decoct(fileperms($path)&0777):null,'mtime'=>$exists?gmdate('c',filemtime($path)):null];
}
echo json_encode(['checked_at'=>gmdate('c'),'ok'=>!$failed,'files'=>$results],JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT)."\n";exit($failed?1:0);
