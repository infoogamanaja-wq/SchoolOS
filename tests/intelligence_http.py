#!/usr/bin/env python3
"""Local-only HTTP routing, access, exports, report cards and offline API checks."""
import urllib.request as U,urllib.parse as P,urllib.error,http.cookiejar,re,sys,json,subprocess,os
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8090/intelligence').rstrip('/');assert P.urlsplit(BASE).hostname in ('127.0.0.1','localhost');n=0
def ok(v,m):
 global n
 assert v,m;n+=1;print('PASS',m)
def client():return U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def req(c,path,data=None,headers={}):
 try:
  r=c.open(U.Request(BASE+'/'+path,data=P.urlencode(data).encode() if isinstance(data,dict) else data,headers=headers));return r.status,r.read(),r.headers
 except urllib.error.HTTPError as e:return e.code,e.read(),e.headers
def text(c,path,data=None):
 s,b,h=req(c,path,data);return s,b.decode(errors='replace'),h
def token(b):return re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',b)[1]
def login(email):
 c=client();_,b,_=text(c,'index.php?login=1');s,b,_=text(c,'index.php?login=1',{'csrf':token(b),'login':1,'email':email,'password':'Local-test-password-2026!'});ok(s==200 and 'Sign out' in b,'login '+email);return c
def clean(s,b):return s==200 and all(x not in b for x in ['Fatal error','Warning:','SQLSTATE'])
a=login('admin@test.local');analyst=login('analyst@test.local');parent=login('parent@test.local');other=login('other@test.local');teacher=login('teacher@test.local');student=login('student@test.local');foreign=login('foreignhr@test.local');public=client()
areas={'reports':['dashboard','reports','builder','exports','retention','forecast'],'innovations':['copilot','drafts','success','pickup','whatsapp'],'academics':['cards','observations','curricula','designer','calendar','timetable'],'governance':['alumni','scholarships','privacy','accreditation','hq','plugins'],'wallet':[''],'settings':['']}
for area,views in areas.items():
 for view in views:
  s,b,_=text(a,f'index.php?s=intelligence&area={area}&view={view}');ok(clean(s,b) and 'op-card' in b,f'admin HTML {area} {view}')
for c,label in [(parent,'parent'),(student,'student'),(teacher,'teacher')]:
 for area,view in [('innovations','copilot'),('academics','cards'),('governance','privacy'),('governance','alumni'),('wallet','')]:
  s,b,_=text(c,f'index.php?s=intelligence&area={area}&view={view}');ok(clean(s,b) and 'School Intelligence' in b,f'{label} route {area}')
 s,b,_=text(c,'index.php?s=intelligence&area=reports');ok(clean(s,b) and 'Requires reports_view' in b,'reports access denied '+label)
for c in [parent,foreign,public]:
 s,b,h=req(c,'index.php?ix_export=1');ok(s==403 and b'false' in b,'private export denied')
s,b,h=req(analyst,'index.php?ix_export=1');ok(s==200 and b'class,recorded' in b and h.get('Cache-Control')=='private, no-store','owner CSV download private')
for c in [parent,teacher,foreign,public]:
 s,b,h=req(c,'index.php?ix_report_card=1&student_id=1&design_id=1&session_name=2026%2F2027&term_name=First');ok((s==200 and b'Communication' in b) if c in [parent,teacher] else s==403,'report card role routing')
s,b,h=req(other,'index.php?ix_report_card=1&student_id=1&design_id=1&session_name=2026%2F2027&term_name=First');ok(s==403,'unlinked report card denied')
s,b,h=req(teacher,'index.php?ix_snapshot=1&class_id=1&day='+__import__('datetime').date.today().isoformat());data=json.loads(b);ok(s==200 and data['ok'] and len(data['snapshot']['students'])==3 and h.get('Cache-Control')=='private, no-store','assigned snapshot JSON private')
s,b,h=req(parent,'index.php?ix_snapshot=1&class_id=1&day='+__import__('datetime').date.today().isoformat());ok(s==403,'family snapshot denied');s,b,h=req(teacher,'index.php?ix_session=1');session=json.loads(b);s,b,h=req(teacher,'index.php?ix_sync=1',json.dumps({'tenant_id':1,'user_id':3,'operations':[]}).encode(),{'Content-Type':'application/json','X-CSRF-Token':session['csrf']});ok(s==200 and json.loads(b)['results']==[],'fresh CSRF JSON synchronization');s,b,h=req(teacher,'index.php?ix_sync=1',b'{}',{'Content-Type':'application/json','X-CSRF-Token':'bad'});ok(s==403,'JSON synchronization CSRF enforced')
s,b,h=req(parent,'index.php?ix_rights=1');ok(s==200 and b'attendance' in b and h.get('Cache-Control')=='private, no-store','approved requester private access response');s,b,h=req(other,'index.php?ix_rights=1');ok(s==403,'other family access response denied')
for path in ['public/offline/offline_teacher.html','public/offline/offline_teacher.js','public/offline/advanced_sw.js']:
 s,b,h=req(public,path);ok(s==200 and b'Amara' not in b,'offline static shell '+path)
for file in ['insights_core.php','intelligence_reports.php','school_innovations.php','academic_tools.php','school_wallet.php','governance_hub.php']:
 s,b,h=req(public,file);ok(s==200 and b'SchoolOS Nigeria' in b and b'function ' not in b,'direct PHP source protected '+file)
s,b,h=req(public,'intelligence_worker.php');ok(s==404,'cron unavailable through HTTP');s,b,h=req(public,'index.php?ix_api=v1&dataset=attendance');ok(s==403,'API rejects anonymous access');s,b,_=text(parent,'index.php?s=intelligence&area=innovations',{'csrf':'bad','ix_action':'si_scan'});ok(clean(s,b) and 'Security token expired' in b,'form CSRF enforced');r=subprocess.run([os.environ.get('SCHOOLOS_PHP_COMMAND','/workspace/toolchain/php'),'/workspace/schoolos-audit/runtime/intelligence/intelligence_worker.php','1','10'],capture_output=True,text=True);ok(r.returncode==0 and r.stdout.startswith('Created ') and '<html' not in r.stdout,'actual Intelligence CLI worker produces no webpage');print('TOTAL',n,'passed')
