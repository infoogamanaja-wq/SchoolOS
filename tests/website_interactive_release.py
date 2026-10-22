from pathlib import Path
import zipfile,json,hashlib,subprocess
r=Path(__file__).resolve().parents[1];n=0
def ok(v,m):
 global n
 assert v,m;n+=1;print('PASS',m)
historical=subprocess.check_output(['git','show','d6a386e:dist/SHA256SUMS'],cwd=r,text=True)
for line in historical.splitlines():
 digest,name=line.split();ok(hashlib.sha256((r/'dist'/name).read_bytes()).hexdigest()==digest,'immutable historical archive '+name)
p=r/'dist/SchoolOS-5.2.1-Interactive-Website.zip'
with zipfile.ZipFile(p) as z:
 m=json.loads(z.read('release.json'));ok(m['version']=='5.2.1' and len(m['files'])==6,'six-file patch manifest')
 ok(z.testzip() is None,'ZIP integrity');ok(set(z.namelist())==set(m['files'])|{'release.json'},'no unexpected payload files')
 for name,digest in m['files'].items():ok(z.read(name)==(r/'app'/name).read_bytes() and hashlib.sha256(z.read(name)).hexdigest()==digest,'manifest source matches '+name)
 ok(all((i.external_attr>>16)&0o777==0o644 for i in z.infolist()),'0644 file permissions')
 ok(not any(x.startswith(('storage/','uploads/')) or x=='config.php' for x in z.namelist()),'private paths excluded')
before=p.read_bytes();subprocess.run(['python','tools/build_release.py'],cwd=r,check=True,capture_output=True);ok(p.read_bytes()==before,'deterministic package rebuild')
print('Release:',n,'assertions passed.')
