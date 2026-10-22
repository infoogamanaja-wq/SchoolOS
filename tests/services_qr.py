#!/usr/bin/env python3
"""Check generated QR modules against an independent encoder and decode the printed label.
Requires test-only qrcode, Pillow and zxing-cpp; no runtime dependency on these packages.
"""
from pathlib import Path
import subprocess,os,re,json,sys
import qrcode,zxingcpp
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1];php=os.environ.get('SCHOOLOS_PHP_COMMAND','php')
# Library-only QR has no database dependency and direct access is guarded.
source="define('SCHOOLOS_SERVICES_LIBRARY',true);require "+json.dumps(str(root/'app/library_manager.php'))+";echo lib_qr($argv[1]);"
for key in ['LIB-1-1','LIB-12345-99999999','LIB-1-12345678901234567890']:
 r=subprocess.run([php,'-r',source,key],capture_output=True,text=True,check=True);points={(int(x),int(y)) for x,y in re.findall(r'M(\d+) (\d+)h1v1h-1z',r.stdout)}
 qr=qrcode.QRCode(version=2,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=10,border=4,mask_pattern=0);qr.add_data(qrcode.util.QRData(key,mode=qrcode.util.MODE_8BIT_BYTE));qr.make(fit=False);matrix=qr.get_matrix();assert points=={(x,y) for y,row in enumerate(matrix) for x,v in enumerate(row) if v},'QR modules differ: '+key
 im=Image.new('RGB',(330,330),'white');d=ImageDraw.Draw(im)
 for x,y in points:d.rectangle((x*10,y*10,x*10+9,y*10+9),fill='black')
 decoded=zxingcpp.read_barcode(im);assert decoded and decoded.text==key,'Independent QR decoding failed'
 print('PASS independent QR matrix and decode',key)
print('TOTAL 3 passed')
