#!/usr/bin/env python3
"""Actual 4.9.0 two-stage upgrade/activation/rollback on a disposable local Apache document root."""
from pathlib import Path
import urllib.request as U,urllib.parse as P,urllib.error,http.cookiejar,re,hashlib,json,zipfile,sys,os
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8092').rstrip('/');assert P.urlsplit(BASE).hostname in ('127.0.0.1','localhost')
ROOT=Path(os.environ.get('SCHOOLOS_UPGRADE_ROOT','/workspace/schoolos-audit/runtime/upgrade'));assert ROOT.name=='upgrade' and 'runtime' in ROOT.parts
REPO=Path(__file__).resolve().parents[1];n=0
def ok(v,label):
 global n
 assert v,label;n+=1;print('PASS',label)
def client():return U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def req(c,path,data=None,headers={}):
 try:
  r=c.open(U.Request(BASE+'/'+path,data=P.urlencode(data).encode() if isinstance(data,dict) else data,headers=headers));return r.status,r.read().decode()
 except urllib.error.HTTPError as e:return e.code,e.read().decode()
def token(b):return re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',b)[1]
def login(email):
 c=client();_,b=req(c,'index.php?login=1');s,b=req(c,'index.php?login=1',{'csrf':token(b),'login':1,'email':email,'password':'Local-test-password-2026!'});assert s==200;return c
admin=login('platform@test.local');baseline=hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest();oldlearning=(ROOT/'learning_portal.php').read_bytes();modified={f:(ROOT/f).read_bytes() for f in ['school_wallet.php','governance_hub.php','finance_engine.php','learning_portal.php','engagement_manager.php','login.html','register.html','onboarding.html','dashboard.html']};protected={f:(ROOT/f).read_bytes() for f in ['parent_portal.php','finance_view.php','operations_core.php','hr_payroll.php','boarding_portal.php','config.php']}
def upload(name):
 _,b=req(admin,'index.php?s=system');csrf=token(b);boundary='SchoolServicesReleaseBoundary';parts=[]
 for k,v in {'csrf':csrf,'sm_action':'install_update','confirm_release':'yes'}.items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
 parts.extend([f'--{boundary}\r\nContent-Disposition: form-data; name="package"; filename="{name}"\r\nContent-Type: application/zip\r\n\r\n'.encode()+(REPO/'dist'/name).read_bytes()+b'\r\n',f'--{boundary}--\r\n'.encode()]);s,b=req(admin,'index.php?s=system',b''.join(parts),{'Content-Type':'multipart/form-data; boundary='+boundary});assert s==200 and 'Update verified and installed' in b,re.search(r'Error:.*?</div>',b)
upload('SchoolOS-5.0.1-Experience-Updater.zip');ok(hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest()==baseline,'support package leaves working 5.0.0 index unchanged')
upload('SchoolOS-5.1.0-Platform-Experience.zip');version=json.loads((ROOT/'storage/system/version.json').read_text());ok(version['version']=='5.1.0','main release installed through frontend')
with zipfile.ZipFile(REPO/'dist/SchoolOS-5.1.0-Platform-Experience.zip') as z:
 manifest=json.loads(z.read('release.json'));ok(all(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h for f,h in manifest['files'].items()),'deployed source matches package manifest')
ok(all((ROOT/f).read_bytes()==b for f,b in protected.items()),'Finance Family Operations and private config bytes preserved')
school=login('admin@test.local');s,b=req(school,'index.php?s=welcome');ok(s==200 and 'Activate the new experience' in b,'explicit additive activation remains required');s,b=req(school,'index.php?s=welcome',{'csrf':token(b),'xp_action':'activate'});ok(s==200 and 'Experience and installed workspace tables activated' in b,'packaged Experience activation')
for path in ['index.php?s=workspace','index.php?s=welcome','index.php?s=welcome&view=access','index.php?s=welcome&view=modules','index.php?s=learning','index.php?s=operations','index.php?s=services','index.php?s=intelligence']:
 s,b=req(school,path);ok(s==200 and all(x not in b for x in ['Fatal error','Warning:','SQLSTATE']),'packaged school route '+path)
for file in ['experience.css','experience.js','login.html','register.html','onboarding.html','dashboard.html']:
 s,b=req(client(),file);ok(s==200 and 'Fatal error' not in b,'packaged asset '+file)
_,b=req(admin,'index.php?s=saas');s,b=req(admin,'index.php?s=saas',{'csrf':token(b),'saas_action':'plan','name':'Package Starter','monthly':'25000','termly':'90000','annual':'240000','trial_days':'14','student_limit':'200','staff_limit':'30'});ok(s==200 and 'Saved successfully' in b,'existing configured plan creation')
_,b=req(admin,'index.php?s=welcome');s,b=req(admin,'index.php?s=welcome',{'csrf':token(b),'xp_action':'platform_settings','origin':'https://schoolos.test','trial_policy':'plans','registrations':'yes','join':'yes'});ok(s==200 and 'subscription settings saved' in b,'packaged platform signup policy')
# Exercise demo provisioning through the actual frontend and retain its private session ID for rollback safety.
_,b=req(admin,'index.php?s=welcome');s,b=req(admin,'index.php?s=welcome',{'csrf':token(b),'xp_action':'demo_config','demo_host':'localhost','demo_name':'schoolos_package_test_demo','demo_user':'root','demo_pass':'','demo_confirm':'yes'});ok(s==200 and 'Connected demo provisioned' in b,'packaged frontend provisions isolated demo')
demo=client();_,b=req(demo,'index.php?login=1');s,b=req(demo,'index.php?login=1',{'csrf':token(b),'login':1,'demo_mode':'yes','email':'schooladmin@demo.schoolos.test','password':'SchoolOS-Demo-Explore-2026!'});ok(s==200 and 'Possibility Heights Demo School' in b and 'DEMO SANDBOX' in b,'packaged role login enters separate database');demoSession=None
for handler in demo.handlers:
 if isinstance(handler,U.HTTPCookieProcessor):
  demoSession=next(cookie.value for cookie in handler.cookiejar if cookie.name.startswith('SCHOOLOSDEMO'))
assert demoSession
new=client();_,b=req(new,'index.php?register=1');request=re.search(r'name="request_key" value="([a-f0-9]{64})"',b)[1];s,b=req(new,'index.php?register=1',{'csrf':token(b),'request_key':request,'xp_public':'school','name':'New Owner','school_name':'Package New School','state':'Lagos','school_type':'Primary','plan_id':1,'cycle':'monthly','email':'package-owner@test.local','password':'PackageOwner-password-2026!','terms':'yes'});ok(s==200 and 'One purposeful step at a time' in b,'public school registration enters guided onboarding')
s,b=req(new,'index.php?s=workspace');ok(s==200 and 'Package New School' in b and 'readiness checks complete' in b,'new school owner overview and setup alerts')
parent=login('parent@test.local');s,b=req(parent,'index.php?s=family&child=1&view=homework');ok(s==200 and 'Complete page 12' in b,'existing family homework preserved')
_,b=req(admin,'index.php?s=system');_,b=req(admin,'index.php?s=system',{'csrf':token(b),'sm_action':'rollback_update','backup_id':version['backup']});ok('Previous files restored' in b,'frontend rollback succeeds');ok(hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest()==baseline,'rollback restores exact stable 5.0.0 index');ok(all((ROOT/f).read_bytes()==value for f,value in modified.items()),'rollback restores exact modified libraries and entry templates');ok(all((ROOT/f).read_bytes()==value for f,value in protected.items()),'unmodified Finance view Family Operations and private config preserved');ok((ROOT/'experience.php').is_file(),'rollback retains new dependency files');s,b=req(client(),'index.php');ok(s==200 and 'Run your school' in b,'homepage works after rollback');s,b=req(client(),'index.php?s=fees',headers={'Cookie':'PHPSESSID='+demoSession});ok(s==200 and 'Run your school' in b and 'Sign out' not in b,'demo session ID cannot authenticate into stable production app after rollback');upload('SchoolOS-5.1.0-Platform-Experience.zip');s,b=req(new,'index.php?s=workspace');ok(s==200 and 'Package New School' in b,'reinstall preserves newly registered school and subscription');print('TOTAL',n,'passed')
