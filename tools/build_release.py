#!/usr/bin/env python3
"""Build deterministic Update Manager payloads; excludes private files and databases."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'app';OUT=ROOT/'dist';OUT.mkdir(exist_ok=True)
def release(name,version,files,requires):
 payload={f:(APP/f).read_bytes() for f in files}
 manifest={'version':version,'files':{f:hashlib.sha256(b).hexdigest() for f,b in payload.items()},'requires':requires}
 payload['release.json']=(json.dumps(manifest,indent=2)+'\n').encode()
 with zipfile.ZipFile(OUT/name,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for f,b in sorted(payload.items()):
   i=zipfile.ZipInfo(f,date_time=(2026,10,22,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,b)
 return hashlib.sha256((OUT/name).read_bytes()).hexdigest()
checks={}
# Published historical archives are immutable. Never rebuild an old version from newer source.
for name in ['SchoolOS-4.6.4-Updater-Repair.zip','SchoolOS-4.6.5-Family-Portal.zip','SchoolOS-4.6.6-Learning-Updater.zip','SchoolOS-4.7.0-Teacher-Student-Portals.zip','SchoolOS-4.7.1-Operations-Updater.zip','SchoolOS-4.8.0-HR-Transport-Boarding.zip','SchoolOS-4.8.1-Services-Updater.zip','SchoolOS-4.9.0-Library-Inventory-Engagement-CMS.zip','SchoolOS-4.9.1-Intelligence-Updater.zip','SchoolOS-5.0.0-Intelligence-Innovations.zip','SchoolOS-5.0.1-Experience-Updater.zip','SchoolOS-5.1.0-Platform-Experience.zip','SchoolOS-5.1.1-Website-Affiliate-Updater.zip','SchoolOS-5.2.0-Website-Affiliates.zip']:
 if (OUT/name).is_file():checks[name]=hashlib.sha256((OUT/name).read_bytes()).hexdigest()
checks['SchoolOS-5.2.1-Interactive-Website.zip']=release('SchoolOS-5.2.1-Interactive-Website.zip','5.2.1',['index.php','experience_ui.php','public_site.php','public_site.css','public_site.js','VERSION.txt'],['config.php','experience.php','affiliate.php','public_guides.php','experience_admin.php','experience_demo.php'])
(OUT/'SHA256SUMS').write_text(''.join(f'{v}  {k}\n' for k,v in checks.items()))
print(json.dumps(checks,indent=2))
