"""Artifact integrity, immutable previous releases and index-last dependencies."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
r=Path(__file__).resolve().parents[1];n=0

def ok(v,m):
 global n
 assert v,m;n+=1;print('PASS',m)
for line in subprocess.check_output(['git','show','7f71fef:dist/SHA256SUMS'],cwd=r,text=True).splitlines():
 digest,name=line.split();ok(hashlib.sha256((r/'dist'/name).read_bytes()).hexdigest()==digest,'immutable '+name)
before={}
for name,count in [('SchoolOS-5.2.2-Portal-Updater.zip',1),('SchoolOS-5.3.0-Role-Portals-LMS.zip',23)]:
 p=r/'dist'/name;before[name]=p.read_bytes()
 with zipfile.ZipFile(p) as z:
  m=json.loads(z.read('release.json'));ok(len(m['files'])==count,'payload file count '+name);ok(z.testzip() is None,'archive integrity '+name);ok(set(z.namelist())==set(m['files'])|{'release.json'},'exact manifest files '+name)
  for f,digest in m['files'].items():ok(z.read(f)==(r/'app'/f).read_bytes() and hashlib.sha256(z.read(f)).hexdigest()==digest,'source and hash '+f)
  ok(all((i.external_attr>>16)&0o777==0o644 for i in z.infolist()),'0644 permissions '+name);ok(not any(f.startswith(('storage/','uploads/')) or f=='config.php' for f in z.namelist()),'private files excluded '+name)
  if count>1:
   files=list(m['files']);ok(files.index('classroom.php')<files.index('experience.php'),'new helper definitions precede autoloading experience module');ok(all(f=='config.php' or (r/'app'/f).exists() for f in m['requires']),'required baseline dependencies available')
subprocess.run(['python3','tools/build_release.py'],cwd=r,check=True,capture_output=True)
for name,content in before.items():ok((r/'dist'/name).read_bytes()==content,'deterministic '+name)
print('Portal release:',n,'assertions passed.')
