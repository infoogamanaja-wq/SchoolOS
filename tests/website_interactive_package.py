from pathlib import Path
import urllib.request as U,urllib.parse as P,urllib.error,http.cookiejar,re,hashlib,json,zipfile
repo=Path(__file__).resolve().parents[1];root=Path('/workspace/schoolos-audit/runtime/upgrade');base='http://127.0.0.1:8092/';n=0
c=U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def req(path,data=None,headers={}):
 try:
  r=c.open(U.Request(base+path,data=P.urlencode(data).encode() if isinstance(data,dict) else data,headers=headers));return r.status,r.read().decode()
 except urllib.error.HTTPError as e:return e.code,e.read().decode()
def ok(v,m):
 global n
 assert v,m;n+=1;print('PASS',m)
def token(b):return re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',b)[1]
_,b=req('index.php?login=1');s,b=req('index.php?login=1',{'csrf':token(b),'login':1,'email':'platform@test.local','password':'Local-test-password-2026!'});ok(s==200 and 'Sign out' in b,'platform sign-in')
assert json.loads((root/'storage/system/version.json').read_text())['version']=='5.2.0','Disposable baseline must be 5.2.0'
package=repo/'dist/SchoolOS-5.2.1-Interactive-Website.zip';manifest=json.loads(zipfile.ZipFile(package).read('release.json'));before={name:(root/name).read_bytes() for name in manifest['files']};protected={name:(root/name).read_bytes() for name in ['affiliate.php','experience.php','finance_engine.php','parent_portal.php','config.php','system_manager.php']}
def upload():
 _,b=req('index.php?s=system');boundary='InteractiveSchoolOSPatchBoundary';parts=[]
 for k,v in {'csrf':token(b),'sm_action':'install_update','confirm_release':'yes'}.items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
 parts.extend([f'--{boundary}\r\nContent-Disposition: form-data; name="package"; filename="{package.name}"\r\nContent-Type: application/zip\r\n\r\n'.encode()+package.read_bytes()+b'\r\n',f'--{boundary}--\r\n'.encode()]);s,b=req('index.php?s=system',b''.join(parts),{'Content-Type':'multipart/form-data; boundary='+boundary});ok(s==200 and 'Update verified and installed' in b,'single patch installs through existing 5.2 updater')
upload();version=json.loads((root/'storage/system/version.json').read_text());ok(version['version']=='5.2.1','installed version 5.2.1')
for name,digest in manifest['files'].items():ok(hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,'deployed manifest '+name)
s,b=req('index.php?home=1');ok(s==200 and 'web-theme' in b and 'quiz-topic' in b and 'quiz-question' in b,'new interactive homepage routes')
s,b=req('index.php?s=workspace');ok(s==200 and 'data-schoolos-logo' in b,'shared mark in packaged dashboard');s,b=req('index.php?page=affiliate-account');ok(s==200 and 'Package Partner' in b,'existing affiliate account preserved')
_,b=req('index.php?s=system');s,b=req('index.php?s=system',{'csrf':token(b),'sm_action':'rollback_update','backup_id':version['backup']});ok(s==200 and 'Previous files restored' in b,'frontend patch rollback succeeds')
ok(all((root/name).read_bytes()==data for name,data in before.items()),'exact six baseline files restored');ok(all((root/name).read_bytes()==data for name,data in protected.items()),'affiliate Finance Family private config and updater unchanged');upload();s,b=req('index.php?home=1');ok(s==200 and 'web-theme' in b,'reinstall restores interactive public page');print('Interactive package:',n,'assertions passed.')
