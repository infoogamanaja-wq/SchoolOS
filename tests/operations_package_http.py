#!/usr/bin/env python3
"""Actual two-stage upgrade/activation/rollback on a disposable local Apache document root."""
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
admin=login('platform@test.local');baseline=hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest();protected={f:(ROOT/f).read_bytes() for f in ['parent_portal.php','learning_portal.php','finance_engine.php','finance_view.php','config.php']}
def upload(name):
 _,b=req(admin,'index.php?s=system');csrf=token(b);boundary='OperationsReleaseBoundary';parts=[]
 for k,v in {'csrf':csrf,'sm_action':'install_update','confirm_release':'yes'}.items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
 parts.extend([f'--{boundary}\r\nContent-Disposition: form-data; name="package"; filename="{name}"\r\nContent-Type: application/zip\r\n\r\n'.encode()+(REPO/'dist'/name).read_bytes()+b'\r\n',f'--{boundary}--\r\n'.encode()]);s,b=req(admin,'index.php?s=system',b''.join(parts),{'Content-Type':'multipart/form-data; boundary='+boundary})
 assert s==200 and 'Update verified and installed' in b,re.search(r'Error:.*?</div>',b)
 return b
upload('SchoolOS-4.7.1-Operations-Updater.zip');ok(hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest()==baseline,'updater support package leaves working 4.7.0 index unchanged')
# New module path must be accepted only after the support package.
upload('SchoolOS-4.8.0-HR-Transport-Boarding.zip');version=json.loads((ROOT/'storage/system/version.json').read_text());ok(version['version']=='4.8.0','full HR Transport Boarding package installed through frontend')
with zipfile.ZipFile(REPO/'dist/SchoolOS-4.8.0-HR-Transport-Boarding.zip') as z:
 manifest=json.loads(z.read('release.json'));ok(all(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h for f,h in manifest['files'].items()),'deployed portal files match final package manifest')
ok(all((ROOT/f).read_bytes()==b for f,b in protected.items()),'existing Family Space Finance and configuration bytes preserved')
school=login('admin@test.local');s,b=req(school,'index.php?s=operations');ok(s==200 and 'Activate School Operations' in b,'explicit activation required before schema changes');s,b=req(school,'index.php?s=operations',{'csrf':token(b),'op_action':'activate'});ok(s==200 and 'HR, Transport and Boarding activated' in b,'school administrator activates additive schemas via frontend')
for area,views in [('hr',['records','recruitment','onboarding','contracts','departments','attendance','leave','duties','salaries','allowances','policy','payslips','advances','evaluations','development','grievances','exit']),('transport',['vehicles','drivers','routes','assignments','fees','trips','events','suggestions']),('boarding',['dashboard','rooms','allocations','fees','movements','leave','visitors','roll','incidents','maintenance','supplies','meals'])]:
 for view in views:
  s,b=req(school,'index.php?s=operations&area='+area+'&view='+view);ok(s==200 and 'op-card' in b and 'Fatal error' not in b and 'Warning:' not in b and 'SQLSTATE' not in b,'packaged Apache '+area+' '+view)
parent=login('parent@test.local');s,b=req(parent,'index.php?s=family&child=1&view=homework');ok(s==200 and 'Complete page 12' in b,'working parent homework integration retained')
_,b=req(admin,'index.php?s=system');_,b=req(admin,'index.php?s=system',{'csrf':token(b),'sm_action':'rollback_update','backup_id':version['backup']});ok('Previous files restored' in b,'full portal update rolls back through frontend')
ok(hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest()==baseline,'rollback restores exact known working 4.7.0 index');ok(all((ROOT/f).is_file() for f in ['parent_portal.php','learning_portal.php','operations_core.php','hr_payroll.php','transport_portal.php','boarding_portal.php']),'rollback never deletes either portal dependency');s,b=req(client(),'index.php');ok(s==200 and 'Run your school' in b,'homepage remains available after rollback');s,b=req(parent,'index.php?s=family&child=1&view=homework');ok(s==200 and 'Complete page 12' in b,'Family Space still works after rollback')
upload('SchoolOS-4.8.0-HR-Transport-Boarding.zip');s,b=req(school,'index.php?s=operations&area=boarding');ok(s==200 and 'Warden dashboard' in b,'same package reinstalls with existing additive tables intact')
print('TOTAL',n,'passed')
