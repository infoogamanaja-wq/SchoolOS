#!/usr/bin/env python3
"""Verify distributable bytes, dependency completeness, privacy and historical immutability."""
from pathlib import Path
import hashlib,json,zipfile,subprocess,re
root=Path(__file__).resolve().parents[1];n=0
def ok(v,label):
 global n
 assert v,label;n+=1;print('PASS',label)
sums={line.split()[1]:line.split()[0] for line in (root/'dist/SHA256SUMS').read_text().splitlines()};old=subprocess.check_output(['git','show','c6af17a:dist/SHA256SUMS'],cwd=root,text=True);old={line.split()[1]:line.split()[0] for line in old.splitlines()}
for name,digest in old.items():ok(sums[name]==digest and hashlib.sha256((root/'dist'/name).read_bytes()).hexdigest()==digest,'historical archive unchanged '+name)
for name,count in [('SchoolOS-5.1.1-Website-Affiliate-Updater.zip',1),('SchoolOS-5.2.0-Website-Affiliates.zip',15)]:
 path=root/'dist'/name;ok(hashlib.sha256(path.read_bytes()).hexdigest()==sums[name],'published digest '+name)
 with zipfile.ZipFile(path) as z:
  manifest=json.loads(z.read('release.json'));ok(z.testzip() is None and len(manifest['files'])==count and set(z.namelist())==set(manifest['files'])|{'release.json'},'complete ZIP manifest '+name)
  ok(all(hashlib.sha256(z.read(file)).hexdigest()==digest and z.read(file)==(root/'app'/file).read_bytes() for file,digest in manifest['files'].items()),'exact validated source bytes '+name)
  ok(all(not re.search(r'(^|/)(config\.php|storage|uploads|database|\.git)(/|$)',file) and '..' not in file and not file.startswith('/') for file in z.namelist()),'no private directories or configuration '+name)
  ok(all((root/'app'/dep).is_file() or dep=='config.php' for dep in manifest['requires']),'dependencies accounted for '+name)
  ok(all(((i.external_attr>>16)&0o777)==0o644 for i in z.infolist()),'normal 0644 package permissions '+name)
before={name:hashlib.sha256((root/'dist'/name).read_bytes()).hexdigest() for name in sums};subprocess.run(['python3',str(root/'tools/build_release.py')],check=True,capture_output=True);ok(all(hashlib.sha256((root/'dist'/name).read_bytes()).hexdigest()==digest for name,digest in before.items()),'deterministic rebuild and unchanged history');print('TOTAL',n,'passed')
