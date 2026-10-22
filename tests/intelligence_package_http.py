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
admin=login('platform@test.local');baseline=hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest();oldlearning=(ROOT/'learning_portal.php').read_bytes();modified={f:(ROOT/f).read_bytes() for f in ['transport_portal.php','engagement_manager.php']};protected={f:(ROOT/f).read_bytes() for f in ['parent_portal.php','finance_engine.php','finance_view.php','operations_core.php','hr_payroll.php','boarding_portal.php','config.php']}
def upload(name):
 _,b=req(admin,'index.php?s=system');csrf=token(b);boundary='SchoolServicesReleaseBoundary';parts=[]
 for k,v in {'csrf':csrf,'sm_action':'install_update','confirm_release':'yes'}.items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
 parts.extend([f'--{boundary}\r\nContent-Disposition: form-data; name="package"; filename="{name}"\r\nContent-Type: application/zip\r\n\r\n'.encode()+(REPO/'dist'/name).read_bytes()+b'\r\n',f'--{boundary}--\r\n'.encode()]);s,b=req(admin,'index.php?s=system',b''.join(parts),{'Content-Type':'multipart/form-data; boundary='+boundary});assert s==200 and 'Update verified and installed' in b,re.search(r'Error:.*?</div>',b)
upload('SchoolOS-4.9.1-Intelligence-Updater.zip');ok(hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest()==baseline,'support package leaves working 4.9.0 index unchanged')
upload('SchoolOS-5.0.0-Intelligence-Innovations.zip');version=json.loads((ROOT/'storage/system/version.json').read_text());ok(version['version']=='5.0.0','main release installed through frontend')
with zipfile.ZipFile(REPO/'dist/SchoolOS-5.0.0-Intelligence-Innovations.zip') as z:
 manifest=json.loads(z.read('release.json'));ok(all(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h for f,h in manifest['files'].items()),'deployed source matches package manifest')
ok(all((ROOT/f).read_bytes()==b for f,b in protected.items()),'Finance Family Operations and private config bytes preserved')
school=login('admin@test.local');s,b=req(school,'index.php?s=intelligence');ok(s==200 and 'Activate School Intelligence' in b,'schema activation explicit');s,b=req(school,'index.php?s=intelligence',{'csrf':token(b),'ix_action':'activate'});ok(s==200 and 'School Intelligence activated' in b,'packaged frontend activation')
for area,views in [('reports',['dashboard','reports','builder','exports','retention','forecast']),('innovations',['copilot','drafts','success','pickup','whatsapp']),('academics',['cards','observations','curricula','designer','calendar','timetable']),('governance',['alumni','scholarships','privacy','accreditation','hq','plugins']),('wallet',['']),('settings',[''])]:
 for view in views:
  s,b=req(school,'index.php?s=intelligence&area='+area+'&view='+view);ok(s==200 and 'op-card' in b and all(x not in b for x in ['Fatal error','Warning:','SQLSTATE']),'packaged Apache '+area+' '+view)
s,b=req(school,'index.php?s=intelligence&area=reports&view=builder',{'csrf':token(b),'ix_action':'rp_definition','name':'Package persisted report','dataset':'attendance','class_id':0,'columns':'class,recorded','from':'2026-01-01','to':'2026-12-31'});ok(s==200 and 'definition saved' in b,'packaged definition mutation')
for path in ['public/offline/offline_teacher.html','public/offline/offline_teacher.js','public/offline/advanced_sw.js']:
 s,b=req(client(),path);ok(s==200 and 'Fatal error' not in b,'packaged nested static path '+path)
def ixpost(c,area,fields):
 _,body=req(c,'index.php?s=intelligence&view=plugins&area='+area);return req(c,'index.php?s=intelligence&view=plugins&area='+area,{'csrf':token(body)}|fields)
for cap in ['integration_manager','reports_view']:
 s,b=ixpost(school,'settings',{'ix_action':'grant','user_id':13,'capability':cap,'decision':'grant'});assert 'capability updated' in b
s,b=ixpost(school,'governance',{'ix_action':'gv_plugin','name':'Packaged API integration','version':'1.0.0','scopes':'["attendance"]','endpoint':'https://example.com'});assert 'integration submitted' in b
reviewer=login('hr@test.local');s,b=ixpost(reviewer,'governance',{'ix_action':'gv_approve_plugin','plugin_id':1});ok(s==200 and 'integration approved' in b,'packaged independent plugin review')
s,b=ixpost(school,'governance',{'ix_action':'gv_token','plugin_id':1,'days':30})
# Token is displayed only on the plugins view after the POST redirect.
apiToken=re.search(r'Copy token once: <code>([a-f0-9]{64})</code>',b)[1]
s,b=req(client(),'index.php?ix_api=v1&dataset=attendance',headers={'X-SchoolOS-Token':apiToken});ok(s==200 and json.loads(b)['api_version']==1,'packaged Apache aggregate API credential forwarding')
s,b=req(client(),'index.php?ix_api=v1&dataset=finance',headers={'X-SchoolOS-Token':apiToken});ok(s==403,'packaged API scope enforcement')
parent=login('parent@test.local');s,b=req(parent,'index.php?s=family&child=1&view=homework');ok(s==200 and 'Complete page 12' in b,'Family homework preserved')
_,b=req(admin,'index.php?s=system');_,b=req(admin,'index.php?s=system',{'csrf':token(b),'sm_action':'rollback_update','backup_id':version['backup']});ok('Previous files restored' in b,'frontend rollback succeeds');ok(hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest()==baseline,'rollback restores exact stable 4.9.0 index');ok(all((ROOT/f).read_bytes()==data for f,data in modified.items()),'rollback restores exact prior transport and engagement modules');ok(all((ROOT/f).is_file() for f in ['parent_portal.php','learning_portal.php','insights_core.php','intelligence_reports.php','school_wallet.php','governance_hub.php']),'rollback retains dependency files');ok(all((ROOT/f).read_bytes()==v for f,v in protected.items()),'rollback preserves unchanged modules and private config');s,b=req(client(),'index.php');ok(s==200 and 'Run your school' in b,'homepage works after rollback');s,b=req(parent,'index.php?s=family&child=1&view=homework');ok(s==200 and 'Complete page 12' in b,'Family works after rollback');upload('SchoolOS-5.0.0-Intelligence-Innovations.zip');s,b=req(school,'index.php?s=intelligence&area=reports&view=exports');ok(s==200 and 'Package persisted report' in b,'reinstall retains additive intelligence records');print('TOTAL',n,'passed')
