from pathlib import Path
import urllib.request as U,urllib.parse as P,urllib.error,http.cookiejar,re,hashlib,json,zipfile,subprocess,os
ROOT=Path('/workspace/schoolos-audit/runtime/upgrade');REPO=Path(__file__).resolve().parents[1];BASE='http://127.0.0.1:8092/';n=0

def ok(v,m):
 global n
 assert v,m;n+=1;print('PASS',m,flush=True)
def client():return U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def req(c,path,data=None,headers={}):
 try:
  r=c.open(U.Request(BASE+path,data=P.urlencode(data).encode() if isinstance(data,dict) else data,headers=headers));return r.status,r.read().decode()
 except urllib.error.HTTPError as e:return e.code,e.read().decode()
def token(b):return re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',b)[1]
def login(email,password='Local-test-password-2026!',demo=False):
 c=client();_,b=req(c,'index.php?login=1');s,b=req(c,'index.php?login=1',{'csrf':token(b),'login':1,'email':email,'password':password,**({'demo_mode':'yes'} if demo else {})});assert s==200 and 'Sign out' in b;return c
admin=login('platform@test.local');_,b=req(admin,'index.php?s=welcome');s,b=req(admin,'index.php?s=welcome',{'csrf':token(b),'xp_action':'activate'});ok(s==200 and 'Experience and installed workspace tables activated' in b,'baseline 5.2.1 activation')
_,b=req(admin,'index.php?s=welcome');s,b=req(admin,'index.php?s=welcome',{'csrf':token(b),'xp_action':'demo_config','demo_host':'localhost','demo_name':'schoolos_package_test_demo','demo_user':'root','demo_pass':'','demo_confirm':'yes'});ok('Connected demo provisioned' in b,'baseline frontend creates old isolated demo')
demo=login('parent@demo.schoolos.test','SchoolOS-Demo-Explore-2026!',True);_,b=req(demo,'index.php?s=family&child=1&view=bookings');s,b=req(demo,'index.php?s=family&child=1&view=bookings',{'csrf':token(b),'pp_action':'book','child':1,'slot_id':1});ok(s==200,'existing demo booking before migration')
with zipfile.ZipFile(REPO/'dist/SchoolOS-5.3.0-Role-Portals-LMS.zip') as z:manifest=json.loads(z.read('release.json'))
before={f:(ROOT/f).read_bytes() for f in manifest['files'] if (ROOT/f).is_file()};stable=before['index.php'];protected={f:(ROOT/f).read_bytes() for f in ['affiliate.php','school_wallet.php','finance_view.php','config.php']}
def upload(name):
 _,b=req(admin,'index.php?s=system');boundary='SchoolOSRolePortalReleaseBoundary';parts=[]
 for k,v in {'csrf':token(b),'sm_action':'install_update','confirm_release':'yes'}.items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
 parts += [f'--{boundary}\r\nContent-Disposition: form-data; name="package"; filename="{name}"\r\nContent-Type: application/zip\r\n\r\n'.encode()+(REPO/'dist'/name).read_bytes()+b'\r\n',f'--{boundary}--\r\n'.encode()];s,b=req(admin,'index.php?s=system',b''.join(parts),{'Content-Type':'multipart/form-data; boundary='+boundary});assert s==200 and 'Update verified and installed' in b,re.search(r'Error:.*?</div>',b)
upload('SchoolOS-5.2.2-Portal-Updater.zip');ok((ROOT/'index.php').read_bytes()==stable,'support ZIP preserves exact stable index');before['system_manager.php']=(ROOT/'system_manager.php').read_bytes();upload('SchoolOS-5.3.0-Role-Portals-LMS.zip');version=json.loads((ROOT/'storage/system/version.json').read_text());ok(version['version']=='5.3.0','main update installed through actual frontend')
for f,h in manifest['files'].items():ok(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,'deployed manifest '+f)
s,b=req(demo,'index.php?s=family&child=1&view=meals');ok(s==200 and 'px-meal-grid' in b,'existing demo upgrades automatically to daily meal calendar');s,b=req(demo,'index.php?s=family&child=1&view=results');ok(s==200 and 'CA contribution' in b and 'Exam contribution' in b,'upgraded demo displays CA and exam breakdown');s,b=req(demo,'index.php?s=family&child=1&view=bookings');ok(s==200 and 'Cancel my booking' in b,'automatic demo migration preserves existing booking');s,b=req(demo,'index.php?s=chat');ok(s==200 and 'Our learning check-in' in b,'demo has connected new chat conversation');s,b=req(demo,'index.php?fn_receipt=1');ok(s==200 and 'office@demo.schoolos.test' in b,'packaged demo receipt has school contact branding')
school=login('admin@test.local');_,b=req(school,'index.php?s=welcome');s,b=req(school,'index.php?s=welcome',{'csrf':token(b),'xp_action':'activate'});ok(s==200 and 'Experience and installed workspace tables activated' in b,'school explicitly activates additive live-workspace tables');s,b=req(school,'index.php?s=chat');ok(s==200 and 'Start a conversation' in b,'packaged real-school chat workspace ready');s,b=req(school,'index.php?s=family');ok(s==200 and 'Requests and messages' in b,'existing family review records retained')
_,b=req(admin,'index.php?s=system');s,b=req(admin,'index.php?s=system',{'csrf':token(b),'sm_action':'rollback_update','backup_id':version['backup']});ok('Previous files restored' in b,'actual frontend rollback succeeds');ok(all((ROOT/f).read_bytes()==data for f,data in before.items()),'rollback restores exact baseline files');ok(all((ROOT/f).read_bytes()==data for f,data in protected.items()),'Finance view affiliate wallet and private config preserved');s,b=req(client(),'index.php?home=1');ok(s==200 and 'Give your school' in b,'stable homepage works after rollback');upload('SchoolOS-5.3.0-Role-Portals-LMS.zip');s,b=req(demo,'index.php?s=family&child=1&view=bookings');ok(s==200 and 'Cancel my booking' in b,'reinstall preserves demo booking and migrated data');print('Portal package:',n,'assertions passed.')
