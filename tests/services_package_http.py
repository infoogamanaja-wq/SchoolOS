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
admin=login('platform@test.local');baseline=hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest();oldlearning=(ROOT/'learning_portal.php').read_bytes();protected={f:(ROOT/f).read_bytes() for f in ['parent_portal.php','finance_engine.php','finance_view.php','operations_core.php','hr_payroll.php','transport_portal.php','boarding_portal.php','config.php']}
def upload(name):
 _,b=req(admin,'index.php?s=system');csrf=token(b);boundary='SchoolServicesReleaseBoundary';parts=[]
 for k,v in {'csrf':csrf,'sm_action':'install_update','confirm_release':'yes'}.items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
 parts.extend([f'--{boundary}\r\nContent-Disposition: form-data; name="package"; filename="{name}"\r\nContent-Type: application/zip\r\n\r\n'.encode()+(REPO/'dist'/name).read_bytes()+b'\r\n',f'--{boundary}--\r\n'.encode()]);s,b=req(admin,'index.php?s=system',b''.join(parts),{'Content-Type':'multipart/form-data; boundary='+boundary});assert s==200 and 'Update verified and installed' in b,re.search(r'Error:.*?</div>',b)
upload('SchoolOS-4.8.1-Services-Updater.zip');ok(hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest()==baseline,'support package leaves working 4.8.0 index unchanged')
upload('SchoolOS-4.9.0-Library-Inventory-Engagement-CMS.zip');version=json.loads((ROOT/'storage/system/version.json').read_text());ok(version['version']=='4.9.0','main release installed through frontend')
with zipfile.ZipFile(REPO/'dist/SchoolOS-4.9.0-Library-Inventory-Engagement-CMS.zip') as z:
 manifest=json.loads(z.read('release.json'));ok(all(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h for f,h in manifest['files'].items()),'deployed source matches package manifest')
ok(all((ROOT/f).read_bytes()==b for f,b in protected.items()),'Finance Family Operations and private config bytes preserved')
school=login('admin@test.local');s,b=req(school,'index.php?s=services');ok(s==200 and 'Activate School Services' in b,'schema activation remains explicit');s,b=req(school,'index.php?s=services',{'csrf':token(b),'sv_action':'activate'});ok(s==200 and 'School Services activated' in b,'frontend school-admin activation succeeds')
for area,views in [('library',['catalogue','resources','loans','reservations','overdue','history','reports','labels']),('inventory',['store','orders','requests','stock','suppliers','purchases','alerts','audits','assets','depreciation','maintenance']),('engagement',['feed','events','messages','consent','compose','campaigns','templates','logs','credits','providers']),('website',['site','content','approval','domains','enquiries','tours'])]:
 for view in views:
  s,b=req(school,'index.php?s=services&area='+area+'&view='+view);ok(s==200 and 'op-card' in b and all(x not in b for x in ['Fatal error','Warning:','SQLSTATE']),'packaged Apache '+area+' '+view)
def post(c,area,view,data):
 _,b=req(c,'index.php?s=services&area='+area+'&view='+view);return req(c,'index.php?s=services&area='+area+'&view='+view,{'csrf':token(b)}|data)
s,b=post(school,'access','',{'sv_action':'grant','user_id':13,'capability':'website_approver','decision':'grant'});ok(s==200 and 'access updated' in b,'packaged scoped capability assignment')
s,b=post(school,'website','site',{'sv_action':'wc_site','theme':'heritage','seo_title':'Packaged School Website','seo_description':'Packaged deployment fixture','active':'yes'});ok(s==200 and 'website settings saved' in b,'packaged site configuration')
site=re.search(r'school=([a-f0-9]{40})',b)[1]
s,b=post(school,'website','content',{'sv_action':'wc_content','kind':'news','slug':'packaged-news','title':'Packaged approved news','body':'PACKAGE DATA SURVIVES ROLLBACK'});content=re.findall(r'wc_preview=(\d+)',b)[0];s,b=post(school,'website','content',{'sv_action':'wc_submit','content_id':content});reviewer=login('hr@test.local');s,b=post(reviewer,'website','approval',{'sv_action':'wc_review','content_id':content,'status':'published','review_note':'Synthetic package content verified'});ok(s==200 and 'Content review saved' in b,'packaged independent content approval');s,b=req(client(),'index.php?school='+site+'&page=news');ok(s==200 and 'PACKAGE DATA SURVIVES ROLLBACK' in b,'packaged approved public website')
parent=login('parent@test.local');teacher=login('teacher@test.local');s,b=req(parent,'index.php?s=family&child=1&view=homework');ok(s==200 and 'Complete page 12' in b,'Family homework preserved');s,b=req(teacher,'index.php?s=learning&view=library');ok(s==200 and 'Teacher Portal' in b,'existing Learning Portal preserved')
_,b=req(admin,'index.php?s=system');_,b=req(admin,'index.php?s=system',{'csrf':token(b),'sm_action':'rollback_update','backup_id':version['backup']});ok('Previous files restored' in b,'frontend full-release rollback succeeds');ok(hashlib.sha256((ROOT/'index.php').read_bytes()).hexdigest()==baseline,'rollback restores exact working 4.8.0 index');ok((ROOT/'learning_portal.php').read_bytes()==oldlearning,'rollback restores exact prior Learning Portal');ok(all((ROOT/f).is_file() for f in ['parent_portal.php','learning_portal.php','operations_core.php','services_core.php','library_manager.php','inventory_manager.php','engagement_manager.php','website_cms.php','services_worker.php','services_push_worker.js']),'rollback retains all portal and new service dependencies');s,b=req(client(),'index.php');ok(s==200 and 'Run your school' in b,'homepage available after rollback');s,b=req(parent,'index.php?s=family&child=1&view=homework');ok(s==200 and 'Complete page 12' in b,'Family Portal works after rollback')
upload('SchoolOS-4.9.0-Library-Inventory-Engagement-CMS.zip');s,b=req(school,'index.php?s=services&area=website&view=content');ok(s==200 and 'Packaged approved news' in b,'reinstall preserves additive content records');s,b=req(client(),'index.php?school='+site+'&page=news');ok(s==200 and 'PACKAGE DATA SURVIVES ROLLBACK' in b,'approved website content returns after reinstall');print('TOTAL',n,'passed')
