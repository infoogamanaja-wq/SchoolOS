#!/usr/bin/env python3
"""Local end-to-end onboarding, role dashboards and isolated demo access."""
import urllib.request as U,urllib.parse as P,urllib.error,http.cookiejar,re,json,sys
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8090/experience').rstrip('/');assert P.urlsplit(BASE).hostname in ('127.0.0.1','localhost');n=0
def ok(v,m):
 global n
 assert v,m;n+=1;print('PASS',m)
def client():return U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def req(c,path,data=None):
 try:r=c.open(BASE+'/'+path,P.urlencode(data).encode() if data is not None else None);return r.status,r.read().decode(),r.headers
 except urllib.error.HTTPError as e:return e.code,e.read().decode(),e.headers
def token(b):return re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',b)[1]
def clean(s,b):return s==200 and not any(x in b for x in ['Fatal error','SQLSTATE','Warning:'])
def login(email,demo=False):
 c=client();_,b,_=req(c,'index.php?login=1');s,b,_=req(c,'index.php?login=1',{'csrf':token(b),'login':1,'email':email,'password':'SchoolOS-Demo-Explore-2026!' if demo else 'Local-test-password-2026!',**({'demo_mode':'yes'} if demo else {})});ok(clean(s,b) and ('Sign out' in b or 'sign out' in b.lower()),'login '+email);return c
public=client()
for path,label in [('index.php?login=1','Good to see you again'),('index.php?register=1','Let your school thrive'),('index.php?join=1','Find your place'),('index.php?xp_privacy=1','Who handles information?')]:
 s,b,h=req(public,path);ok(clean(s,b) and label in b,'public '+path)
s,b,h=req(public,'index.php?login=1');ok('data-fact-pause' in b and 'data-demo-role="driver"' in b and 'experience.css' in b,'interactive login facts and demo selector');ok('type="password"' in b and 'data-show-password' in b,'password visibility control')
admin=login('admin@test.local');platform=login('platform@test.local');teacher=login('teacher@test.local');parent=login('parent@test.local');student=login('student@test.local')
for c,label in [(admin,'school administrator'),(platform,'platform'),(teacher,'teacher'),(parent,'parent'),(student,'student')]:
 s,b,_=req(c,'index.php?s=workspace');ok(clean(s,b) and 'id="xpWelcome"' in b and 'data-xp-clock' in b and 'data-xp-tour' in b,'role overview '+label)
 s,b,_=req(c,'index.php?s=welcome');ok(clean(s,b),'role onboarding '+label)
s,b,_=req(admin,'index.php?s=workspace');ok('YOUR SETUP COMPASS' in b and 'readiness checks complete' in b,'school admin setup readiness alerts');ok('Current unpaid invoice balance' in b and 'recorded' in b,'dashboard metrics have defined meaning');
# Every link in the simplified owner navigation resolves through its installed workspace.
_,b,_=req(admin,'index.php?s=workspace');menu=re.search(r'<nav class="navscroll".*?</nav>',b,re.S)[0]
for href in dict.fromkeys(re.findall(r'href="([^"]+)"',menu)):
 if not href.startswith('?s='):continue
 s,body,_=req(admin,'index.php'+__import__('html').unescape(href));ok(clean(s,body),'owner navigation '+href)
for c,path in [(admin,'index.php?s=welcome&view=access'),(admin,'index.php?s=welcome&view=modules'),(platform,'index.php?s=welcome&view=platform')]:
 s,b,_=req(c,path);ok(clean(s,b) and 'xp-panel' in b,'working configuration '+path)
_,b,_=req(admin,'index.php?s=workspace');s,b,_=req(admin,'index.php?xp_tour=1',{'csrf':token(b),'xp_action':'tour_done'});ok(s==200 and json.loads(b)['ok'],'walkthrough completion persists');s,b,_=req(admin,'index.php?xp_tour=1',{'csrf':'wrong','xp_action':'tour_done'});ok(s==403,'tour CSRF enforced')
# Approval issues a school-controlled temporary credential; no records open until it is replaced.
member=client();_,b,_=req(member,'index.php?login=1');s,b,_=req(member,'index.php?login=1',{'csrf':token(b),'login':1,'email':'new-parent@experience.test','password':'FirstLogin-temporary-2026!'});ok(clean(s,b) and 'Make this account yours' in b,'approved member forced through first-login password change');s,b,_=req(member,'index.php?s=family');ok(s==200 and 'Make this account yours' in b,'initial password gate protects direct school routes');s,b,_=req(member,'index.php?s=workspace',{'csrf':token(b),'xp_initial_password':1,'new_password':'PersonalParent-password-2026!'});ok(clean(s,b) and 'A verified student link is still needed' in b,'new password unlocks only scoped overview without guessed child links')
roles=['schooladmin','teacher','parent','student','driver','warden','hr','librarian','stock','comms','admissions','partner','platform','reviewer'];demos={}
for role in roles:
 c=login(role+'@demo.schoolos.test',True);demos[role]=c;s,b,_=req(c,'index.php?s=workspace');ok(clean(s,b) and 'DEMO SANDBOX' in b and 'Test Academy' not in b,'isolated demo overview '+role)
for role,path,needle in [('teacher','index.php?s=learning&view=classes','Primary 5'),('parent','index.php?s=family&child=1','Amara Demo'),('student','index.php?s=learning&view=homework','Fractions in everyday life'),('driver','index.php?s=operations&area=transport','Sunrise'),('warden','index.php?s=operations&area=boarding','Harmony'),('hr','index.php?s=operations&area=hr','Demo Teacher'),('librarian','index.php?s=services&area=library','The Joy of Numbers'),('stock','index.php?s=services&area=inventory','School notebook'),('admissions','index.php?s=applications','New Learner Demo')]:
 s,b,_=req(demos[role],path);ok(clean(s,b) and needle in b,'connected demo workflow '+role)
# Demo writes stay within the shared fictional database and connect across role accounts.
_,b,_=req(demos['teacher'],'index.php?s=learning&view=attendance');s,b,_=req(demos['teacher'],'index.php?s=learning&view=attendance',{'csrf':token(b),'lp_action':'attendance','student_id':1,'attendance_date':__import__('datetime').date.today().isoformat(),'status':'late','reason':'Fictional demo bus delay'});ok(clean(s,b) and 'Attendance recorded' in b,'demo teacher can record fictional attendance')
s,b,_=req(demos['parent'],'index.php?s=family&child=1&view=attendance');ok(clean(s,b) and 'late' in b,'demo parent sees teacher attendance change')
for c,path in [(demos['platform'],'index.php?s=system'),(demos['platform'],'index.php?s=integrations'),(demos['platform'],'index.php?v24_backup=1')]:
 s,b,_=req(c,path);ok(s==403,'demo host management endpoint blocked '+path)
_,b,_=req(demos['schooladmin'],'index.php?s=workspace');s,b,_=req(demos['schooladmin'],'index.php?s=welcome',{'csrf':token(b),'xp_action':'checkout'});ok(s==403,'demo live checkout blocked')
s,b,_=req(demos['schooladmin'],'index.php?s=welcome',{'csrf':token(b) if 'name="csrf"' in b else 'unused','v23_action':'test_smtp'});ok(s==403,'demo external integration action blocked')
_,b,_=req(public,'index.php?login=1');s,b,_=req(public,'index.php?login=1',{'csrf':token(b),'login':1,'email':'schooladmin@demo.schoolos.test','password':'SchoolOS-Demo-Explore-2026!'});ok(s==200 and 'Check your email and password' in b,'public demo password never authenticates into live database')
_,b,_=req(demos['schooladmin'],'index.php?s=workspace');s,b,_=req(demos['schooladmin'],'index.php?s=applications',{'csrf':token(b),'crm_action':'send_emails'});ok(s==403,'demo native mail dispatcher blocked')
for file in ['experience.php','experience_ui.php','experience_admin.php','experience_demo.php']:
 s,b,_=req(public,file);ok(s==200 and 'Good to see you again' in b and 'function xp_' not in b,'direct source protected '+file)
s,b,_=req(public,'experience_demo_refresh.php');ok(s==404,'demo maintenance CLI blocked over HTTP');_,b,_=req(demos['schooladmin'],'index.php?s=workspace');s,b,_=req(demos['schooladmin'],'index.php?s=operations',{'csrf':token(b),'op_action':'grant','user_id':5,'capability':'driver','decision':'revoke'});ok(s==403,'shared demo role capabilities cannot be revoked');print('TOTAL',n,'passed')
