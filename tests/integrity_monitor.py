from pathlib import Path
import subprocess,tempfile,zipfile,os
r=Path(__file__).resolve().parents[1];php=os.environ.get('SCHOOLOS_PHP_COMMAND','php')
with tempfile.TemporaryDirectory(prefix='schoolos-monitor-') as d:
 p=Path(d)
 with zipfile.ZipFile(r/'dist/SchoolOS-4.6.5-Family-Portal.zip') as z:z.extractall(p)
 def check(expected,label):
  x=subprocess.run([php,str(r/'tools/integrity_check.php'),str(p),str(p/'release.json')],capture_output=True,text=True);assert x.returncode==expected,(label,x.stdout,x.stderr);print('PASS',label)
 check(0,'monitor accepts matching hashes')
 original=(p/'index.php').read_bytes();(p/'index.php').unlink();check(1,'monitor detects missing index without recreating it');assert not (p/'index.php').exists();(p/'index.php').write_bytes(original)
 (p/'parent_portal.php').write_text('altered');check(1,'monitor detects altered portal')
 (p/'release.json').write_text('{"files":{}}');check(2,'monitor refuses an incomplete baseline')
with tempfile.TemporaryDirectory(prefix='schoolos-learning-monitor-') as d:
 p=Path(d)
 with zipfile.ZipFile(r/'dist/SchoolOS-4.7.0-Teacher-Student-Portals.zip') as z:z.extractall(p)
 check(0,'monitor accepts new learning release manifest')
 (p/'learning_portal.php').unlink();check(1,'monitor detects missing learning module without recreating it')
print('TOTAL 6 passed')
