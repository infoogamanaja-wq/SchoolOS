<?php
declare(strict_types=1);
ini_set('session.cookie_httponly','1');ini_set('session.cookie_samesite','Lax');
if (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ini_set('session.cookie_secure','1');
session_start();
if (is_file(__DIR__.'/config.php') || is_file(__DIR__.'/.installed.lock')) { http_response_code(403); exit('Already installed.'); }
if (empty($_SESSION['install_csrf'])) $_SESSION['install_csrf']=bin2hex(random_bytes(32));
$errors=[];$success=false;
if ($_SERVER['REQUEST_METHOD']==='POST') {
 $installLock=null;
 try {
  $installLock=fopen(__DIR__.'/.installing.lock','c');
  if(!$installLock||!flock($installLock,LOCK_EX|LOCK_NB))throw new RuntimeException('Another installation is running.');
  if(is_file(__DIR__.'/config.php')||is_file(__DIR__.'/.installed.lock'))throw new RuntimeException('Already installed.');
  foreach(['pdo_mysql','zip','mbstring','curl','fileinfo','openssl','tokenizer'] as $ext)if(!extension_loaded($ext))throw new RuntimeException('Missing required PHP extension: '.$ext);
  if (!hash_equals($_SESSION['install_csrf'],(string)($_POST['csrf']??''))) throw new RuntimeException('Invalid form token.');
  if (!extension_loaded('pdo_mysql')) throw new RuntimeException('pdo_mysql is required.');
  if (!class_exists('ZipArchive')) throw new RuntimeException('PHP ZIP extension is required for Updates & Plugins.');
  $host=trim((string)($_POST['host']??''));$name=trim((string)($_POST['name']??''));$user=trim((string)($_POST['user']??''));$pass=(string)($_POST['pass']??'');
  $email=trim((string)($_POST['email']??''));$admin=(string)($_POST['admin_pass']??'');
  if (!preg_match('/^[a-zA-Z0-9_.-]{1,64}$/',$name)) throw new RuntimeException('Invalid database name.');
  if (!preg_match('/^[a-zA-Z0-9.-]{1,253}$/',$host)) throw new RuntimeException('Invalid database host.');
  if (!filter_var($email,FILTER_VALIDATE_EMAIL)) throw new RuntimeException('Invalid email.');
  if (strlen($admin)<14) throw new RuntimeException('Use an admin password of at least 14 characters.');
  $pdo=new PDO('mysql:host='.$host.';dbname='.$name.';charset=utf8mb4',$user,$pass,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_EMULATE_PREPARES=>false]);
  $tables=(int)$pdo->query('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE()')->fetchColumn();
  if ($tables>0) throw new RuntimeException('Use an empty database created in cPanel.');
  $sql=file_get_contents(__DIR__.'/database/schema.sql');if($sql===false)throw new RuntimeException('Missing schema.');
  foreach(array_filter(array_map('trim',preg_split('/;\s*(?:\r?\n|$)/',$sql))) as $statement)$pdo->exec($statement);
  $stmt=$pdo->prepare('INSERT INTO users(tenant_id,email,password_hash,role,name) VALUES(NULL,?,?,?,?)');
  $stmt->execute([$email,password_hash($admin,PASSWORD_DEFAULT),'platform_super_admin','Platform Super Admin']);
  $config=['db'=>['host'=>$host,'name'=>$name,'user'=>$user,'pass'=>$pass],'app'=>['name'=>'SchoolOS Nigeria','timezone'=>'Africa/Lagos'],'providers'=>['paystack_secret_key'=>'','whatsapp_token'=>'','sms_token'=>'','ai_api_key'=>'']];
  $content='<?php return '.var_export($config,true).';';
  $tmp=__DIR__.'/.config-'.bin2hex(random_bytes(8)).'.tmp';
  if(file_put_contents($tmp,$content,LOCK_EX)!==strlen($content)||!chmod($tmp,0600)||!rename($tmp,__DIR__.'/config.php')){if(is_file($tmp))unlink($tmp);throw new RuntimeException('Cannot securely save configuration.');}
  if(!is_dir(__DIR__.'/storage/system')&&!mkdir(__DIR__.'/storage/system',0700,true))throw new RuntimeException('Cannot create system storage.');
  if(file_put_contents(__DIR__.'/storage/.htaccess',"Require all denied\n",LOCK_EX)===false)throw new RuntimeException('Cannot protect storage.');

  if(file_put_contents(__DIR__.'/.installed.lock',date(DATE_ATOM),LOCK_EX)===false)throw new RuntimeException('Cannot create installation lock.');
  $success=true;
 } catch(Throwable $e) { error_log('SchoolOS install error: '.$e->getMessage());$errors[]='Installation failed. Check the database, server requirements, and PHP error log. Do not retry against a partially populated database.'; } finally {if(is_resource($installLock)){flock($installLock,LOCK_UN);fclose($installLock);}}
}
function h($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
?><!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>SchoolOS Setup</title><style>body{font:16px system-ui;background:#f1f5f9;color:#0f172a;padding:2rem}.box{max-width:550px;margin:auto;background:white;padding:2rem;border-radius:16px;box-shadow:0 10px 30px #0f172a12}label{display:block;margin-top:14px;font-weight:600}input{width:100%;box-sizing:border-box;padding:12px;margin-top:5px;border:1px solid #cbd5e1;border-radius:8px}button{margin-top:20px;background:#0f172a;color:white;border:0;border-radius:8px;padding:13px 22px}.err{color:#991b1b}</style><div class="box"><h1>SchoolOS installation</h1><?php if($success):?><p>Installation complete. <a href="index.php?login=1">Sign in</a>. Remove install.php from your live server.</p><?php else:?><p>Create an <b>empty MySQL database and user in cPanel</b>, then provide their details below. Use HTTPS.</p><?php foreach($errors as $error):?><p class="err"><?=h($error)?></p><?php endforeach;?><form method="post"><input type="hidden" name="csrf" value="<?=h($_SESSION['install_csrf'])?>"><label>MySQL host<input name="host" value="localhost" required></label><label>Existing database name<input name="name" required></label><label>Database username<input name="user" required></label><label>Database password<input type="password" name="pass"></label><label>Super Admin email<input type="email" name="email" required></label><label>Super Admin password (14+ characters)<input type="password" name="admin_pass" minlength="14" required></label><button type="submit">Install SchoolOS</button></form><?php endif;?></div></html>