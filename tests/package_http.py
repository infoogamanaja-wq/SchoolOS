#!/usr/bin/env python3
"""End-to-end ZIP upload against /upgrade, a disposable copy of the uploaded application."""
from pathlib import Path
import urllib.request as U,urllib.parse as P,urllib.error,http.cookiejar,re,hashlib,json,sys,os
base=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8090').rstrip('/')
assert P.urlsplit(base).hostname in ('localhost','127.0.0.1')
prefix=sys.argv[2] if len(sys.argv)>2 else '/upgrade/'
root=Path(os.environ.get('SCHOOLOS_UPGRADE_ROOT','/workspace/schoolos-audit/runtime/upgrade'));assert 'runtime' in root.parts and root.name=='upgrade', 'Disposable upgrade root required'
source=Path(__file__).resolve().parents[1];count=0
def ok(v,label):
 global count
 assert v,label
 count+=1;print('PASS',label)
def client():return U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def request(c,path,data=None,headers={}):
 r=c.open(U.Request(base+prefix+path,data=data,headers=headers));return r.status,r.read().decode()
def csrf(b):return re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',b)[1]
def login(email):
 c=client();_,b=request(c,'index.php?login=1');_,b=request(c,'index.php?login=1',P.urlencode({'login':1,'csrf':csrf(b),'email':email,'password':'Local-test-password-2026!'}).encode());return c
admin=login('platform@test.local');old=hashlib.sha256((root/'index.php').read_bytes()).hexdigest()
config=(root/'config.php').read_bytes()
def upload(name):
 _,b=request(admin,'index.php?s=system');token=csrf(b);boundary='SchoolOSBoundary2026';parts=[]
 for k,v in {'csrf':token,'sm_action':'install_update','confirm_release':'yes'}.items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
 parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="package"; filename="{name}"\r\nContent-Type: application/zip\r\n\r\n'.encode()+(source/'dist'/name).read_bytes()+b'\r\n')
 parts.append(f'--{boundary}--\r\n'.encode());s,b=request(admin,'index.php?s=system',b''.join(parts),{'Content-Type':'multipart/form-data; boundary='+boundary})
 if 'Error:' in b:
  m=re.search('Error:.*?</div>',b);print(m[0] if m else b[-2000:])
 return s,b
s,b=upload('SchoolOS-4.6.4-Updater-Repair.zip');ok(s==200 and 'Update installed' in b,'bootstrap ZIP installed through original frontend updater')
ok(hashlib.sha256((root/'index.php').read_bytes()).hexdigest()==old,'bootstrap leaves stable index byte-for-byte unchanged')
s,b=upload('SchoolOS-4.6.5-Family-Portal.zip');ok(s==200 and 'Update verified and installed' in b,'portal ZIP installed through hardened frontend updater')
version=json.loads((root/'storage/system/version.json').read_text());ok(version['version']=='4.6.5','installed version committed after verification')
import zipfile
with zipfile.ZipFile(source/'dist/SchoolOS-4.6.5-Family-Portal.zip') as z:
 m=json.loads(z.read('release.json'));ok(all(hashlib.sha256((root/f).read_bytes()).hexdigest()==v for f,v in m['files'].items()),'every installed file matches release manifest')
ok((root/'config.php').read_bytes()==config,'configuration preserved through both installs')
parent=login('parent@test.local');_,b=request(parent,'index.php?s=family&child=1&view=homework');ok('Complete page 12' in b and 'Parent & Guardian Portal' in b,'packaged portal serves integrated homework')
_,b=request(admin,'index.php?s=system');token=csrf(b);_,b=request(admin,'index.php?s=system',P.urlencode({'csrf':token,'sm_action':'rollback_update','backup_id':version['backup']}).encode());ok('Previous files restored' in b,'frontend manual rollback completes')
ok(hashlib.sha256((root/'index.php').read_bytes()).hexdigest()==old,'frontend rollback restores exact stable index')
ok((root/'parent_portal.php').is_file(),'frontend rollback retains new portal dependency')
_,b=request(client(),'index.php');ok('Run your school' in b,'public homepage survives rollback')
_,b=upload('SchoolOS-4.6.5-Family-Portal.zip');ok('Update verified and installed' in b,'same tested package reinstalls after rollback')
_,b=request(parent,'index.php?s=family&child=2&view=calendar');ok('Sports day' in b,'sibling portal works after reinstall')
print('TOTAL',count,'passed')
