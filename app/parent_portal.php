<?php
/** SchoolOS Family Space. Loaded before output; uses the existing login and PDO connection. */
if(!defined('SCHOOLOS_PARENT_LIBRARY')){header('Location: index.php?s=family',true,302);exit;}
function pp_tables(): array {return [
"CREATE TABLE IF NOT EXISTS pp_posts(id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,tenant_id BIGINT UNSIGNED NOT NULL,kind VARCHAR(20) NOT NULL,title VARCHAR(200) NOT NULL,body TEXT NOT NULL,class_id BIGINT UNSIGNED NULL,student_id BIGINT UNSIGNED NULL,starts_at DATETIME NULL,ends_at DATETIME NULL,options_json TEXT NULL,active TINYINT NOT NULL DEFAULT 1,created_by BIGINT UNSIGNED NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,INDEX(tenant_id,kind,active)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS pp_documents(id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,tenant_id BIGINT UNSIGNED NOT NULL,post_id BIGINT UNSIGNED NOT NULL,filename VARCHAR(180) NOT NULL,mime VARCHAR(100) NOT NULL,content MEDIUMBLOB NOT NULL,UNIQUE KEY post_doc(tenant_id,post_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS pp_responses(id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,tenant_id BIGINT UNSIGNED NOT NULL,post_id BIGINT UNSIGNED NOT NULL,user_id BIGINT UNSIGNED NOT NULL,student_id BIGINT UNSIGNED NOT NULL,answer TEXT NOT NULL,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,UNIQUE KEY one_response(tenant_id,post_id,user_id,student_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS pp_requests(id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,tenant_id BIGINT UNSIGNED NOT NULL,user_id BIGINT UNSIGNED NOT NULL,student_id BIGINT UNSIGNED NOT NULL,kind VARCHAR(20) NOT NULL,subject VARCHAR(200) NOT NULL,body TEXT NOT NULL,starts_on DATE NULL,ends_on DATE NULL,recipient_id BIGINT UNSIGNED NULL,status VARCHAR(20) NOT NULL DEFAULT 'pending',reply TEXT NULL,reviewed_by BIGINT UNSIGNED NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,INDEX(tenant_id,user_id,student_id),INDEX(tenant_id,recipient_id,status)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS pp_slots(id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,tenant_id BIGINT UNSIGNED NOT NULL,teacher_user_id BIGINT UNSIGNED NOT NULL,starts_at DATETIME NOT NULL,ends_at DATETIME NOT NULL,active TINYINT NOT NULL DEFAULT 1,UNIQUE KEY teacher_start(tenant_id,teacher_user_id,starts_at)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS pp_bookings(id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,tenant_id BIGINT UNSIGNED NOT NULL,slot_id BIGINT UNSIGNED NOT NULL,user_id BIGINT UNSIGNED NOT NULL,student_id BIGINT UNSIGNED NOT NULL,status VARCHAR(20) NOT NULL DEFAULT 'booked',created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,INDEX(tenant_id,slot_id,status),INDEX(tenant_id,user_id)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
];}
function pp_install(): void {global $pdo;foreach(pp_tables() as $s)$pdo->exec($s);}
function pp_ready(): bool {try{foreach(['pp_posts','pp_documents','pp_responses','pp_requests','pp_slots','pp_bookings','ecosystem_links','ecosystem_support'] as $t)if(!g('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE() AND table_name=?',[$t]))return false;return true;}catch(Throwable $e){return false;}}
function pp_has(string $table): bool {return (bool)g('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE() AND table_name=?',[$table]);}
function pp_actor(): array {
 $u=me();if(!$u||(int)($u['tenant_id']??0)<1||!in_array($u['role'],['parent','school_admin','teacher'],true))throw new RuntimeException('School parent, teacher or administrator access required.');
 // Recheck current account state instead of trusting a stale login snapshot.
 $active=q('SELECT id FROM users WHERE id=? AND tenant_id=? AND role=? AND active=1',[$u['id'],$u['tenant_id'],$u['role']])->fetch();
 if(!$active)throw new RuntimeException('Account is no longer active.');return $u;
}
function pp_children(array $u): array {
 return q("SELECT DISTINCT s.*,c.name class_name FROM ecosystem_links l JOIN students s ON s.id=l.student_id AND s.tenant_id=l.tenant_id LEFT JOIN classes c ON c.id=s.class_id AND c.tenant_id=s.tenant_id WHERE l.tenant_id=? AND l.user_id=? AND l.relation_type='parent' ORDER BY s.name,s.id",[$u['tenant_id'],$u['id']])->fetchAll();
}
function pp_child(array $u,int $sid): array {
 foreach(pp_children($u) as $s)if((int)$s['id']===$sid)return $s;
 throw new RuntimeException('Child is not linked to your account.');
}
function pp_text(string $key,int $max=2000): string {
 $v=$_POST[$key]??'';if(!is_string($v))throw new RuntimeException('Invalid input.');$v=trim($v);
 if(mb_strlen($v)>$max)throw new RuntimeException('Input too long: '.$key);return $v;
}
function pp_date(string $v): string {$d=DateTimeImmutable::createFromFormat('!Y-m-d',$v);if(!$d||$d->format('Y-m-d')!==$v)throw new RuntimeException('Invalid date.');return $v;}
function pp_datetime(string $v): string {$d=DateTimeImmutable::createFromFormat('!Y-m-d\TH:i',$v);if(!$d||$d->format('Y-m-d\TH:i')!==$v)throw new RuntimeException('Invalid appointment time.');return $d->format('Y-m-d H:i:s');}
function pp_visible(array $p,array $s): bool {return (!(int)($p['student_id']??0)||(int)$p['student_id']===(int)$s['id'])&&(!(int)($p['class_id']??0)||(int)$p['class_id']===(int)$s['class_id']);}
function pp_post(array $u,array $s,int $id,bool $lock=false): array {
 $p=q('SELECT * FROM pp_posts WHERE tenant_id=? AND id=? AND active=1'.($lock?' FOR UPDATE':''),[$u['tenant_id'],$id])->fetch();
 if(!$p||!pp_visible($p,$s))throw new RuntimeException('Item is unavailable.');return $p;
}
function pp_invoice(array $u,int $id): array {
 $i=q('SELECT * FROM fn_invoices WHERE tenant_id=? AND id=?',[$u['tenant_id'],$id])->fetch();
 if(!$i)throw new RuntimeException('Invoice not found.');pp_child($u,(int)$i['student_id']);return $i;
}
function pp_payment(array $u,string $action,?callable $transport=null): string {
 $api=$transport??'fn45Api';
 global $pdo;$tid=(int)$u['tenant_id'];$uid=(int)$u['id'];
 if(!pp_has('fn45_gateway')||!function_exists('fnConfirmPayment'))throw new RuntimeException('Ask the school to activate Finance and Paystack integration.');
 if($action==='pay'){
  $i=pp_invoice($u,(int)($_POST['invoice_id']??0));$balance=(int)$i['amount_kobo']-(int)$i['discount_kobo']+(int)$i['penalty_kobo']-(int)$i['paid_kobo'];
  if($balance<=0)throw new RuntimeException('Invoice is already settled.');
  if(!filter_var($u['email'],FILTER_VALIDATE_EMAIL))throw new RuntimeException('Valid account email required.');
  $ref='SOS-'.$tid.'-'.$i['id'].'-'.bin2hex(random_bytes(10));
  $resp=$api('POST','/transaction/initialize',fn45Secret($tid),['email'=>$u['email'],'amount'=>$balance,'reference'=>$ref,'currency'=>'NGN','metadata'=>['tenant_id'=>$tid,'invoice_id'=>(int)$i['id']]]);
  $url=(string)($resp['data']['authorization_url']??'');if(!preg_match('~^https://checkout\.paystack\.com/~',$url))throw new RuntimeException('Unexpected checkout URL.');
  q('INSERT INTO fn45_gateway(tenant_id,invoice_id,reference,amount_kobo,authorization_url) VALUES(?,?,?,?,?)',[$tid,$i['id'],$ref,$balance,$url]);
  return 'Checkout created. Open the secure Paystack link below, then select Verify payment.';
 }
 $gw=q('SELECT * FROM fn45_gateway WHERE tenant_id=? AND id=?',[$tid,(int)($_POST['gateway_id']??0)])->fetch();
 if(!$gw)throw new RuntimeException('Transaction not found.');pp_invoice($u,(int)$gw['invoice_id']);
 if($gw['status']==='confirmed')return 'Payment already verified.';
 // Network verification outside SQL transaction; lock and recheck before posting once.
 $resp=$api('GET','/transaction/verify/'.rawurlencode($gw['reference']),fn45Secret($tid));$data=$resp['data']??[];
 if(($data['status']??'')!=='success'||($data['reference']??'')!==$gw['reference']||!isset($data['amount'])||(string)$data['amount']!==(string)$gw['amount_kobo']||($data['currency']??'')!=='NGN')throw new RuntimeException('Provider has not confirmed the expected payment.');
 $pdo->beginTransaction();try{
  $locked=q('SELECT * FROM fn45_gateway WHERE tenant_id=? AND id=? FOR UPDATE',[$tid,$gw['id']])->fetch();
  pp_invoice($u,(int)$locked['invoice_id']);
  if($locked['status']!=='confirmed'){
   q("INSERT INTO fn_payments(tenant_id,invoice_id,reference,amount_kobo,channel,status,notes) VALUES(?,?,?,?,?,'pending',?)",[$tid,$gw['invoice_id'],$gw['reference'],$gw['amount_kobo'],'paystack','Parent portal: verified server-to-server']);
   fnConfirmPayment($tid,(int)$pdo->lastInsertId(),$uid);
   q("UPDATE fn45_gateway SET status='confirmed',verified_at=NOW() WHERE tenant_id=? AND id=?",[$tid,$gw['id']]);
   audit('family.payment.verified','invoice',(string)$gw['invoice_id']);
  }$pdo->commit();return 'Payment verified and posted to Finance.';
 }catch(Throwable $e){if($pdo->inTransaction())$pdo->rollBack();throw $e;}
}
function pp_action(array $u): string {
 global $pdo;$tid=(int)$u['tenant_id'];$uid=(int)$u['id'];
 if(!hash_equals((string)($_SESSION['csrf']??''),(string)($_POST['csrf']??'')))throw new RuntimeException('Security token expired.');
 $a=pp_text('pp_action',30);$admin=$u['role']==='school_admin';
 if($a==='activate'){if(!$admin)throw new RuntimeException('School administrator required.');if(!pp_has('ecosystem_links')||!pp_has('ecosystem_support'))throw new RuntimeException('Activate the ecosystem first.');pp_install();return 'Family Space activated. Existing records preserved.';}
 if(!pp_ready())throw new RuntimeException('Family Space needs activation by the school administrator.');
 if($u['role']==='parent'){
  if(in_array($a,['pay','verify'],true))return pp_payment($u,$a);
  $s=pp_child($u,(int)($_POST['child']??0));$sid=(int)$s['id'];
  if(in_array($a,['absence','pickup','message','ticket'],true)){
   $subject=pp_text('subject',200);$body=pp_text('body',2000);if(!$subject||!$body)throw new RuntimeException('Subject and details required.');
   if($a==='ticket'){q("INSERT INTO ecosystem_support(tenant_id,created_by,subject,message,status) VALUES(?,?,?,?,'open')",[$tid,$uid,$subject,'Student #'.$sid.': '.$body]);return 'Support ticket opened in Support Desk.';}
   $start=null;$end=null;$recipient=null;
   if($a==='absence'||$a==='pickup'){$start=pp_date(pp_text('starts_on',10));$end=$a==='absence'?pp_date(pp_text('ends_on',10)):$start;if($end<$start)throw new RuntimeException('End date must follow start date.');}
   if($a==='message'){$recipient=(int)($_POST['recipient_id']??0);if(!g("SELECT id FROM users WHERE tenant_id=? AND id=? AND role IN ('teacher','school_admin') AND active=1",[$tid,$recipient]))throw new RuntimeException('Choose a school teacher or administrator.');}
   q('INSERT INTO pp_requests(tenant_id,user_id,student_id,kind,subject,body,starts_on,ends_on,recipient_id) VALUES(?,?,?,?,?,?,?,?,?)',[$tid,$uid,$sid,$a,$subject,$body,$start,$end,$recipient]);audit('family.request',$a,(string)$pdo->lastInsertId());return 'Request submitted for school review.';
  }
  if($a==='respond'){
   $pdo->beginTransaction();try{
    $p=pp_post($u,$s,(int)($_POST['post_id']??0),true);
    if(!in_array($p['kind'],['consent','survey','meals'],true))throw new RuntimeException('This item does not accept responses.');
    if(($p['ends_at']&&$p['ends_at']<date('Y-m-d H:i:s'))||($p['starts_at']&&$p['starts_at']>date('Y-m-d H:i:s')))throw new RuntimeException('Response window is closed.');
    $answer=pp_text('answer',2000);$opts=json_decode($p['options_json']?:'[]',true);
    if(!$answer||($p['kind']==='consent'&&!in_array($answer,['yes','no'],true))||($p['kind']!=='consent'&&$opts&&!in_array($answer,$opts,true)))throw new RuntimeException('Choose a valid response.');
    q('INSERT INTO pp_responses(tenant_id,post_id,user_id,student_id,answer) VALUES(?,?,?,?,?) ON DUPLICATE KEY UPDATE answer=VALUES(answer)',[$tid,$p['id'],$uid,$sid,$answer]);audit('family.response',$p['kind'],(string)$p['id']);$pdo->commit();return 'Response saved for '.$s['name'].'.';
   }catch(Throwable $e){$pdo->rollBack();throw $e;}
  }
  if($a==='book'||$a==='cancel_booking'){
   $pdo->beginTransaction();try{
    $slot=q('SELECT * FROM pp_slots WHERE tenant_id=? AND id=? FOR UPDATE',[$tid,(int)($_POST['slot_id']??0)])->fetch();
    if(!$slot||!$slot['active']||$slot['starts_at']<=date('Y-m-d H:i:s'))throw new RuntimeException('Appointment is unavailable.');
    if($a==='cancel_booking'){q("UPDATE pp_bookings SET status='cancelled' WHERE tenant_id=? AND slot_id=? AND user_id=? AND student_id=? AND status='booked'",[$tid,$slot['id'],$uid,$sid]);}
    else{
     if(g("SELECT id FROM pp_bookings WHERE tenant_id=? AND slot_id=? AND status='booked'",[$tid,$slot['id']]))throw new RuntimeException('This slot is already booked.');
     q('INSERT INTO pp_bookings(tenant_id,slot_id,user_id,student_id) VALUES(?,?,?,?)',[$tid,$slot['id'],$uid,$sid]);
    }$pdo->commit();return $a==='book'?'Appointment booked.':'Appointment cancelled.';
   }catch(Throwable $e){$pdo->rollBack();throw $e;}
  }
  if($a==='revoke_pickup'){
   q("UPDATE pp_requests SET status='revoked' WHERE tenant_id=? AND id=? AND user_id=? AND student_id=? AND kind='pickup' AND status IN ('pending','approved')",[$tid,(int)($_POST['request_id']??0),$uid,$sid]);audit('family.pickup.revoked','request',(string)($_POST['request_id']??0));return 'Pickup authorization revoked.';
  }
  throw new RuntimeException('Unsupported parent action.');
 }
 if($a==='slot'){
  $teacher=$admin?(int)($_POST['teacher_user_id']??0):$uid;
  if(!g("SELECT id FROM users WHERE tenant_id=? AND id=? AND role='teacher' AND active=1",[$tid,$teacher]))throw new RuntimeException('Choose a teacher.');
  $start=pp_datetime(pp_text('starts_at',16));$end=pp_datetime(pp_text('ends_at',16));if($end<=$start||$start<=date('Y-m-d H:i:s'))throw new RuntimeException('Choose a future appointment and valid end time.');
  // Serialize slot creation on the teacher account, preventing overlapping appointments.
  $pdo->beginTransaction();try{
   q('SELECT id FROM users WHERE id=? AND tenant_id=? FOR UPDATE',[$teacher,$tid]);
   if(g('SELECT id FROM pp_slots WHERE tenant_id=? AND teacher_user_id=? AND active=1 AND starts_at<? AND ends_at>?',[$tid,$teacher,$end,$start]))throw new RuntimeException('Teacher already has an overlapping slot.');
   q('INSERT INTO pp_slots(tenant_id,teacher_user_id,starts_at,ends_at) VALUES(?,?,?,?)',[$tid,$teacher,$start,$end]);$pdo->commit();return 'Appointment slot published.';
  }catch(Throwable $e){$pdo->rollBack();throw $e;}
 }
 if($a==='review'){
  $id=(int)($_POST['request_id']??0);$r=q('SELECT * FROM pp_requests WHERE tenant_id=? AND id=?',[$tid,$id])->fetch();
  if(!$r||(!$admin&&($r['kind']!=='message'||(int)$r['recipient_id']!==$uid)))throw new RuntimeException('Request is unavailable.');
  $status=pp_text('status',20);$allowed=$r['kind']==='message'?['replied','closed']:['approved','rejected'];
  if(!in_array($status,$allowed,true)||in_array($r['status'],['revoked','collected'],true))throw new RuntimeException('Invalid review status.');
  $reply=pp_text('reply',2000);if(!$reply)throw new RuntimeException('Provide a reply or review note.');
  $st=q('UPDATE pp_requests SET status=?,reply=?,reviewed_by=? WHERE tenant_id=? AND id=? AND status=?',[$status,$reply,$uid,$tid,$id,$r['status']]);if($st->rowCount()!==1)throw new RuntimeException('Request changed. Refresh and review again.');
  audit('family.review',$r['kind'],(string)$id);return 'Review saved. Absence approval does not rewrite attendance; pickup still requires identity checks.';
 }
 if(!$admin)throw new RuntimeException('School administrator required.');
 if($a==='publish'){
  $kind=pp_text('kind',20);if(!in_array($kind,['calendar','consent','transport','meals','document','survey'],true))throw new RuntimeException('Invalid item type.');
  $title=pp_text('title',200);$body=pp_text('body',4000);if(!$title||!$body)throw new RuntimeException('Title and details required.');
  $class=(int)($_POST['class_id']??0);$student=(int)($_POST['student_id']??0);
  if($class&&!g('SELECT id FROM classes WHERE tenant_id=? AND id=?',[$tid,$class]))throw new RuntimeException('Invalid class.');
  if($student&&!g('SELECT id FROM students WHERE tenant_id=? AND id=?',[$tid,$student]))throw new RuntimeException('Invalid student.');
  $start=pp_text('starts_at',16);$end=pp_text('ends_at',16);$start=$start?pp_datetime($start):null;$end=$end?pp_datetime($end):null;
  if($start&&$end&&$end<=$start)throw new RuntimeException('Invalid date range.');
  $options=array_values(array_filter(array_map('trim',explode("\n",pp_text('options',2000))),fn($s)=>$s!==''));if(count($options)>30)throw new RuntimeException('Too many options.');
  if($kind==='meals'&&!$options)throw new RuntimeException('Enter meal choices, one per line.');
  $doc=null;if($kind==='document'){
   $f=$_FILES['document']??null;if(!$f||$f['error']!==UPLOAD_ERR_OK||$f['size']<1||$f['size']>2097152)throw new RuntimeException('Document must be 1 byte to 2 MB.');
   $mime=(new finfo(FILEINFO_MIME_TYPE))->file($f['tmp_name']);if(!in_array($mime,['application/pdf','image/jpeg','image/png','image/webp'],true))throw new RuntimeException('Only PDF and images allowed.');
   $doc=['filename'=>mb_substr(basename($f['name']),0,180),'mime'=>$mime,'content'=>file_get_contents($f['tmp_name'])];
  }
  $pdo->beginTransaction();try{
   q('INSERT INTO pp_posts(tenant_id,kind,title,body,class_id,student_id,starts_at,ends_at,options_json,created_by) VALUES(?,?,?,?,?,?,?,?,?,?)',[$tid,$kind,$title,$body,$class?:null,$student?:null,$start,$end,json_encode($options,JSON_THROW_ON_ERROR),$uid]);$pid=(int)$pdo->lastInsertId();
   if($doc)q('INSERT INTO pp_documents(tenant_id,post_id,filename,mime,content) VALUES(?,?,?,?,?)',[$tid,$pid,$doc['filename'],$doc['mime'],$doc['content']]);
   audit('family.publish',$kind,(string)$pid);$pdo->commit();return 'Published to the selected families.';
  }catch(Throwable $e){$pdo->rollBack();throw $e;}
 }
 if($a==='close_post'){q('UPDATE pp_posts SET active=0 WHERE tenant_id=? AND id=?',[$tid,(int)($_POST['post_id']??0)]);return 'Item closed. Responses retained.';}
 throw new RuntimeException('Unsupported staff action.');
}
function pp_download(array $u): void {
 $tid=(int)$u['tenant_id'];$s=pp_child($u,(int)($_GET['child']??0));
 $d=q('SELECT d.*,p.kind,p.class_id,p.student_id,p.active FROM pp_documents d JOIN pp_posts p ON p.id=d.post_id AND p.tenant_id=d.tenant_id WHERE d.tenant_id=? AND d.id=?',[$tid,(int)$_GET['pp_document']])->fetch();
 if(!$d||!$d['active']||!pp_visible($d,$s)){http_response_code(404);exit('Document not found.');}
 header('Content-Type: '.$d['mime']);header('Content-Disposition: attachment; filename="'.preg_replace('/[^A-Za-z0-9._-]/','_',$d['filename']).'"');header('Cache-Control: private, no-store');header('X-Content-Type-Options: nosniff');echo $d['content'];exit;
}
function pp_form(string $action,int $sid=0): void {echo '<form method="post" enctype="multipart/form-data"><input type="hidden" name="csrf" value="'.e($_SESSION['csrf']).'"><input type="hidden" name="pp_action" value="'.e($action).'"><input type="hidden" name="child" value="'.$sid.'">';}
function pp_field(string $name,string $label,string $type='text',bool $required=true): void {echo '<label>'.e($label).($type==='textarea'?'<textarea rows="3" name="'.e($name).'" maxlength="2000"'.($required?' required':'').'></textarea>':'<input name="'.e($name).'" type="'.e($type).'"'.($required?' required':'').'>').'</label>';}
function pp_end(string $label): void {echo '<button class="btn">'.e($label).'</button></form>';}
function pp_table(array $rows,array $labels): void {
 echo '<div class="pp-scroll"><table class="table"><tr>';foreach($labels as $l)echo '<th>'.e($l).'</th>';echo '</tr>';
 foreach($rows as $r){echo '<tr>';foreach($r as $v)echo '<td>'.e($v).'</td>';echo '</tr>';}
 echo '</table></div>';if(!$rows)echo '<p class="muted">No records available.</p>';
}
function pp_render(array $u): void {
 $tid=(int)$u['tenant_id'];$uid=(int)$u['id'];$admin=$u['role']==='school_admin';
 echo '<style>.pp-nav{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}.pp-nav a{padding:9px 12px;border:1px solid #cbd5e1;border-radius:9px;color:inherit;text-decoration:none}.pp-nav a[aria-current=page]{background:#075e56;color:white}.pp-card{background:var(--card,#fff);border:1px solid #d7e3e6;border-radius:16px;padding:22px;margin:14px 0}.pp-card label{display:block;margin:12px 0}.pp-card input,.pp-card textarea,.pp-card select{display:block;max-width:100%;box-sizing:border-box;width:100%;padding:10px;border:1px solid #aabdc8;border-radius:7px;font:inherit}.pp-scroll{overflow:auto}.pp-card p{white-space:pre-wrap}.pp-hero{background:linear-gradient(110deg,#13394c,#08796e);color:white;border-radius:18px;padding:24px}.pp-card form{margin:16px 0}.pp-card button{margin:8px 0}</style><div class="pp-hero"><h2>Parent & Guardian Portal</h2><p>Your family’s school day, in one place.</p></div>';
 if(!pp_ready()){
  echo '<div class="pp-card"><h3>Activate Family Space</h3><p>Back up the database first. Activation adds six tables without altering existing records. Activate Ecosystem Hub first.</p>';
  if($admin){pp_form('activate');pp_end('Activate Family Space');}else echo '<p>Ask your school administrator to activate Family Space.</p>';echo '</div>';return;
 }
 if($u['role']!=='parent'){pp_staff($u);return;}
 $children=pp_children($u);if(!$children){echo '<div class="pp-card">No children are linked yet. Ask your school to link your parent account under Account Links. Matching names or emails never grants access.</div>';return;}
 $sid=(int)($_GET['child']??0);if($sid===0)$sid=(int)$children[0]['id'];$s=pp_child($u,$sid);
 $tabs=['children'=>'Multiple children','results'=>'Results','attendance'=>'Attendance','fees'=>'Fee payment','receipts'=>'Receipts','homework'=>'Homework','messages'=>'Messages','calendar'=>'Calendar','bookings'=>'Parent–teacher bookings','absence'=>'Absence requests','consent'=>'Consent forms','pickup'=>'Pickup authorization','transport'=>'Transport updates','meals'=>'School meals','documents'=>'Documents','support'=>'Support tickets','surveys'=>'Surveys'];
 $tab=(string)($_GET['view']??'children');if(!isset($tabs[$tab]))$tab='children';
 echo '<nav class="pp-nav" aria-label="Children">';foreach($children as $child)echo '<a href="?s=family&amp;child='.(int)$child['id'].'&amp;view='.e($tab).'" '.((int)$child['id']===$sid?'aria-current="page"':'').'>'.e($child['name']).'</a>';echo '</nav><nav class="pp-nav" aria-label="Family features">';
 foreach($tabs as $key=>$label)echo '<a href="?s=family&amp;child='.$sid.'&amp;view='.$key.'" '.($key===$tab?'aria-current="page"':'').'>'.e($label).'</a>';echo '</nav><div class="pp-card"><h2>'.e($tabs[$tab]).' · '.e($s['name']).'</h2>';
 if($tab==='children'){pp_table(array_map(fn($c)=>[$c['student_no'],$c['name'],$c['class_name']],$children),['Admission number','Child','Class']);echo '<p><a href="?s=announcements">Open Community Hub & WhatsApp contacts →</a></p>';}
 elseif($tab==='results'){
  pp_table(q("SELECT sub.name,r.score,r.max_score,r.grade,r.remark FROM results r JOIN subjects sub ON sub.id=r.subject_id AND sub.tenant_id=r.tenant_id WHERE r.tenant_id=? AND r.student_id=? AND r.status='published' ORDER BY r.id DESC LIMIT 100",[$tid,$sid])->fetchAll(),['Subject','Score','Maximum','Grade','Remark']);
  if(pp_has('ac_term_approvals'))pp_table(q("SELECT a.session_name,a.term_name,sub.name,a.title,sc.score,a.max_score FROM ac_scores sc JOIN ac_assessments a ON a.id=sc.assessment_id AND a.tenant_id=sc.tenant_id JOIN subjects sub ON sub.id=a.subject_id AND sub.tenant_id=a.tenant_id JOIN ac_term_approvals p ON p.tenant_id=a.tenant_id AND p.class_id=a.class_id AND p.session_name=a.session_name AND p.term_name=a.term_name WHERE sc.tenant_id=? AND sc.student_id=? AND sc.status='approved' AND p.status='published' ORDER BY a.id DESC LIMIT 100",[$tid,$sid])->fetchAll(),['Session','Term','Subject','Assessment','Score','Maximum']);
 }
 elseif($tab==='attendance'){
  pp_table(q('SELECT attendance_date,status,reason FROM attendance WHERE tenant_id=? AND student_id=? ORDER BY attendance_date DESC LIMIT 100',[$tid,$sid])->fetchAll(),['Date','Status','Reason']);
  if(pp_has('aw_period_attendance'))pp_table(q('SELECT attendance_date,period_name,status,reason FROM aw_period_attendance WHERE tenant_id=? AND student_id=? ORDER BY attendance_date DESC LIMIT 100',[$tid,$sid])->fetchAll(),['Date','Period','Status','Reason']);
 }
 elseif($tab==='homework'){
  if(pp_has('ac_lessons'))pp_table(q("SELECT l.lesson_date,sub.name,c.topic,l.homework FROM ac_lessons l JOIN ac_curriculum c ON c.id=l.curriculum_id AND c.tenant_id=l.tenant_id JOIN subjects sub ON sub.id=c.subject_id AND sub.tenant_id=c.tenant_id WHERE l.tenant_id=? AND c.class_id=? AND l.status='delivered' AND l.homework IS NOT NULL AND l.homework<>'' ORDER BY l.lesson_date DESC LIMIT 100",[$tid,$s['class_id']])->fetchAll(),['Lesson date','Subject','Topic','Homework']);else echo '<p>No published academic homework yet.</p>';
 }
 elseif($tab==='fees'||$tab==='receipts'){pp_finance_view($u,$s,$tab);}
 elseif($tab==='bookings'){
  $slots=q("SELECT sl.*,u.name teacher FROM pp_slots sl JOIN users u ON u.id=sl.teacher_user_id AND u.tenant_id=sl.tenant_id AND u.active=1 WHERE sl.tenant_id=? AND sl.active=1 AND sl.starts_at>? ORDER BY sl.starts_at LIMIT 100",[$tid,date('Y-m-d H:i:s')])->fetchAll();
  foreach($slots as $slot){$book=q("SELECT * FROM pp_bookings WHERE tenant_id=? AND slot_id=? AND status='booked'",[$tid,$slot['id']])->fetch();echo '<h3>'.e($slot['teacher']).'</h3><p>'.e($slot['starts_at']).' – '.e($slot['ends_at']).' (Africa/Lagos)</p>';
   if(!$book||((int)$book['user_id']===$uid&&(int)$book['student_id']===$sid)){pp_form($book?'cancel_booking':'book',$sid);echo '<input type="hidden" name="slot_id" value="'.(int)$slot['id'].'">';pp_end($book?'Cancel my booking':'Book appointment');}else echo '<p>Unavailable</p>';
  }if(!$slots)echo '<p>No appointment slots have been published.</p>';
 }
 elseif(in_array($tab,['absence','pickup','messages','support'],true)){
  $a=['absence'=>'absence','pickup'=>'pickup','messages'=>'message','support'=>'ticket'][$tab];pp_form($a,$sid);pp_field('subject',$a==='pickup'?'Authorized adult’s full name':'Subject');
  pp_field('body',$a==='pickup'?'Relationship, phone, pickup window and identity-check instructions':'Details','textarea');
  if($a==='absence'){pp_field('starts_on','First absence date','date');pp_field('ends_on','Last absence date','date');}
  if($a==='pickup')pp_field('starts_on','Pickup date','date');
  if($a==='message'){echo '<label>Recipient<select name="recipient_id" required>';foreach(q("SELECT id,name,role FROM users WHERE tenant_id=? AND active=1 AND role IN ('teacher','school_admin') ORDER BY name",[$tid])->fetchAll() as $r)echo '<option value="'.(int)$r['id'].'">'.e($r['name'].' · '.$r['role']).'</option>';echo '</select></label>';}
  pp_end($a==='pickup'?'Request pickup authorization':'Submit');
  if($a==='ticket')pp_table(q('SELECT id,subject,message,status,created_at FROM ecosystem_support WHERE tenant_id=? AND created_by=? ORDER BY id DESC LIMIT 100',[$tid,$uid])->fetchAll(),['Ticket','Subject','Message','Status','Created']);
  else{
   $rows=q('SELECT id,subject,body,starts_on,ends_on,status,reply FROM pp_requests WHERE tenant_id=? AND user_id=? AND student_id=? AND kind=? ORDER BY id DESC LIMIT 100',[$tid,$uid,$sid,$a])->fetchAll();pp_table($rows,['ID','Subject','Details','From','To','Status','School reply']);
   if($a==='pickup'){echo '<p>School approval and physical identity checks are required. This portal does not prove the collector’s identity.</p>';foreach($rows as $r)if(in_array($r['status'],['pending','approved'],true)){pp_form('revoke_pickup',$sid);echo '<input type="hidden" name="request_id" value="'.(int)$r['id'].'">';pp_end('Revoke authorization #'.$r['id']);}}
  }
 }
 else{
  $kind=['surveys'=>'survey','documents'=>'document'][$tab]??$tab;
  $posts=q('SELECT * FROM pp_posts WHERE tenant_id=? AND kind=? AND active=1 ORDER BY COALESCE(starts_at,created_at) DESC LIMIT 200',[$tid,$kind])->fetchAll();$shown=0;
  foreach($posts as $p){if(!pp_visible($p,$s))continue;$shown++;echo '<article class="pp-card"><h3>'.e($p['title']).'</h3><p>'.e($p['body']).'</p><small>'.e($p['starts_at']).' '.e($p['ends_at']).'</small>';
   if($kind==='document'){$doc=g('SELECT id FROM pp_documents WHERE tenant_id=? AND post_id=?',[$tid,$p['id']]);echo '<p><a href="?s=family&amp;child='.$sid.'&amp;pp_document='.(int)$doc.'">Download document</a></p>';}
   if(in_array($kind,['consent','survey','meals'],true)){
    $answer=g('SELECT answer FROM pp_responses WHERE tenant_id=? AND post_id=? AND user_id=? AND student_id=?',[$tid,$p['id'],$uid,$sid]);if($answer)echo '<p>Your saved response: '.e($answer).'</p>';
    pp_form('respond',$sid);echo '<input type="hidden" name="post_id" value="'.(int)$p['id'].'">';$opts=$kind==='consent'?['yes','no']:json_decode($p['options_json']?:'[]',true);
    if($opts){echo '<label>Your choice<select name="answer" required>';foreach($opts as $o)echo '<option '.($answer===$o?'selected ':'').'value="'.e($o).'">'.e($o).'</option>';echo '</select></label>';}else pp_field('answer','Your response','textarea');pp_end('Save response');
   }echo '</article>';
  }if(!$shown)echo '<p>No items have been published for this child.</p>';
 }
 echo '</div>';
}
function pp_finance_view(array $u,array $s,string $tab): void {
 $tid=(int)$u['tenant_id'];$sid=(int)$s['id'];
 if(!pp_has('fn_invoices')){echo '<p>Finance workspace has not been activated.</p>';return;}
 if($tab==='fees'){
  $rows=q('SELECT * FROM fn_invoices WHERE tenant_id=? AND student_id=? ORDER BY id DESC LIMIT 100',[$tid,$sid])->fetchAll();
  foreach($rows as $i){$balance=(int)$i['amount_kobo']-(int)$i['discount_kobo']+(int)$i['penalty_kobo']-(int)$i['paid_kobo'];echo '<h3>'.e($i['reference']).' · '.e($i['description']).'</h3><p>Balance: '.e(fnFmt($balance)).' · Due: '.e($i['due_date']).' · '.e($i['status']).'</p>';if($balance>0&&pp_has('fn45_gateway')){pp_form('pay',$sid);echo '<input type="hidden" name="invoice_id" value="'.(int)$i['id'].'">';pp_end('Pay securely with Paystack');}}
  if(!$rows)echo '<p>No Finance invoices for this child.</p>';
  if(pp_has('fn45_gateway'))foreach(q('SELECT gw.* FROM fn45_gateway gw JOIN fn_invoices i ON i.id=gw.invoice_id AND i.tenant_id=gw.tenant_id WHERE gw.tenant_id=? AND i.student_id=? ORDER BY gw.id DESC LIMIT 30',[$tid,$sid])->fetchAll() as $gw){echo '<p>'.e($gw['reference']).' · '.e($gw['status']).'</p>';if($gw['status']!=='confirmed'){
   if(preg_match('~^https://checkout\.paystack\.com/~',(string)$gw['authorization_url']))echo '<a href="'.e($gw['authorization_url']).'" target="_blank" rel="noopener noreferrer">Open secure Paystack checkout ↗</a>';
   pp_form('verify',$sid);echo '<input type="hidden" name="gateway_id" value="'.(int)$gw['id'].'">';pp_end('Verify payment');}}
  $legacy=q('SELECT reference,amount,paid,status,due_date FROM invoices WHERE tenant_id=? AND student_id=? ORDER BY id DESC LIMIT 100',[$tid,$sid])->fetchAll();if($legacy){echo '<h3>Legacy invoices (contact school to pay)</h3>';pp_table($legacy,['Reference','Amount NGN','Paid NGN','Status','Due']);}
 }else{
  $rows=q("SELECT p.id,p.reference,p.amount_kobo,p.confirmed_at FROM fn_payments p JOIN fn_invoices i ON i.id=p.invoice_id AND i.tenant_id=p.tenant_id WHERE p.tenant_id=? AND i.student_id=? AND p.status='confirmed' ORDER BY p.id DESC LIMIT 100",[$tid,$sid])->fetchAll();
  foreach($rows as $r)echo '<p><a href="?fn_receipt='.(int)$r['id'].'">'.e($r['reference']).' · '.e(fnFmt($r['amount_kobo'])).' · Print receipt</a></p>';if(!$rows)echo '<p>No confirmed payments. Receipts appear after payment verification.</p>';
 }
}
function pp_staff(array $u): void {
 $tid=(int)$u['tenant_id'];$uid=(int)$u['id'];$admin=$u['role']==='school_admin';
 echo '<div class="pp-card"><h2>Family Space · school workspace</h2><p>Use Portal Accounts and Account Links to connect parents to their children. Published documents are explicitly shared with families; private SIS documents remain private.</p>';
 if($admin){
  pp_form('publish');echo '<label>Type<select name="kind">';foreach(['calendar','consent','transport','meals','document','survey'] as $k)echo '<option>'.e($k).'</option>';echo '</select></label>';pp_field('title','Title');pp_field('body','Details','textarea');
  echo '<label>Class audience<select name="class_id"><option value="0">All classes</option>';foreach(q('SELECT id,name FROM classes WHERE tenant_id=? ORDER BY name',[$tid])->fetchAll() as $c)echo '<option value="'.(int)$c['id'].'">'.e($c['name']).'</option>';echo '</select></label>';
  pp_field('student_id','Student ID (optional, narrows audience)','number',false);pp_field('starts_at','Start / response window opens (Africa/Lagos)','datetime-local',false);pp_field('ends_at','End / response deadline (Africa/Lagos)','datetime-local',false);pp_field('options','Meal or survey choices, one per line','textarea',false);
  echo '<label>Document (PDF/image, up to 2 MB)<input type="file" name="document" accept="application/pdf,image/jpeg,image/png,image/webp"></label>';pp_end('Publish to families');
  foreach(q('SELECT id,title,kind,active FROM pp_posts WHERE tenant_id=? ORDER BY id DESC LIMIT 60',[$tid])->fetchAll() as $p){echo '<h3>'.e($p['title']).' · '.e($p['kind']).'</h3>';pp_table(q('SELECT s.name child,u.name parent,r.answer,r.updated_at FROM pp_responses r JOIN users u ON u.id=r.user_id AND u.tenant_id=r.tenant_id JOIN students s ON s.id=r.student_id AND s.tenant_id=r.tenant_id WHERE r.tenant_id=? AND r.post_id=? ORDER BY r.id DESC LIMIT 200',[$tid,$p['id']])->fetchAll(),['Child','Parent','Response','Updated']);if($p['active']){pp_form('close_post');echo '<input type="hidden" name="post_id" value="'.(int)$p['id'].'">';pp_end('Close item #'.$p['id']);}}
 }
 echo '</div><div class="pp-card"><h3>Publish a parent–teacher appointment</h3>';pp_form('slot');
 if($admin){echo '<label>Teacher<select name="teacher_user_id">';foreach(q("SELECT id,name FROM users WHERE tenant_id=? AND role='teacher' AND active=1 ORDER BY name",[$tid])->fetchAll() as $r)echo '<option value="'.(int)$r['id'].'">'.e($r['name']).'</option>';echo '</select></label>';}
 pp_field('starts_at','Start (Africa/Lagos)','datetime-local');pp_field('ends_at','End','datetime-local');pp_end('Publish appointment');
 pp_table(q("SELECT sl.starts_at,sl.ends_at,tu.name teacher,pa.name parent,s.name child,b.status FROM pp_bookings b JOIN pp_slots sl ON sl.id=b.slot_id AND sl.tenant_id=b.tenant_id JOIN users tu ON tu.id=sl.teacher_user_id AND tu.tenant_id=sl.tenant_id JOIN users pa ON pa.id=b.user_id AND pa.tenant_id=b.tenant_id JOIN students s ON s.id=b.student_id AND s.tenant_id=b.tenant_id WHERE b.tenant_id=?".($admin?'':' AND sl.teacher_user_id=?').' ORDER BY sl.starts_at DESC LIMIT 100',$admin?[$tid]:[$tid,$uid])->fetchAll(),['Start','End','Teacher','Parent','Child','Status']);echo '</div><div class="pp-card"><h3>Requests and messages</h3>';
 $rows=q('SELECT r.*,u.name parent,s.name child FROM pp_requests r JOIN users u ON u.id=r.user_id AND u.tenant_id=r.tenant_id JOIN students s ON s.id=r.student_id AND s.tenant_id=r.tenant_id WHERE r.tenant_id=?'.($admin?'':" AND r.kind='message' AND r.recipient_id=?").' ORDER BY r.id DESC LIMIT 100',$admin?[$tid]:[$tid,$uid])->fetchAll();
 foreach($rows as $r){echo '<article class="pp-card"><h3>'.e($r['kind'].' #'.$r['id'].' · '.$r['subject']).'</h3><p>'.e($r['parent'].' / '.$r['child']).' · '.e($r['starts_on']).' – '.e($r['ends_on']).'</p><p>'.e($r['body']).'</p><p>Status: '.e($r['status']).' · '.e($r['reply']).'</p>';if(!in_array($r['status'],['revoked','collected'],true)){
  pp_form('review');echo '<input type="hidden" name="request_id" value="'.(int)$r['id'].'"><label>Decision<select name="status">';foreach($r['kind']==='message'?['replied','closed']:['approved','rejected'] as $st)echo '<option>'.e($st).'</option>';echo '</select></label>';pp_field('reply','School reply / identity verification note','textarea');pp_end('Save review');}echo '</article>';
 }echo '</div>';
}
