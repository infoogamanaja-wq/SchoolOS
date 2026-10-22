#!/usr/bin/env python3
"""Local HTTP role, CMS publication, actual media, public form, routing and cron checks."""
import html
import urllib.request as U,urllib.parse as P,urllib.error,http.cookiejar,re,sys,io,subprocess,os
from pathlib import Path
from PIL import Image
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8090/services').rstrip('/');assert P.urlsplit(BASE).hostname in ('127.0.0.1','localhost');n=0
ROOT=Path(os.environ.get('SCHOOLOS_SERVICES_ROOT','/workspace/schoolos-audit/runtime/services'));assert ROOT.name=='services' and 'runtime' in ROOT.parts
PHP=os.environ.get('SCHOOLOS_PHP_COMMAND','php')
def ok(v,m):
 global n
 assert v,m;n+=1;print('PASS',m)
def client():return U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def req(c,path,data=None,headers={}):
 try:
  r=c.open(U.Request(BASE+'/'+path,data=P.urlencode(data).encode() if isinstance(data,dict) else data,headers=headers));return r.status,r.read(),r.headers
 except urllib.error.HTTPError as e:return e.code,e.read(),e.headers
def text(c,path,data=None):
 s,b,h=req(c,path,data);return s,b.decode(errors='replace'),h
def token(b):return re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',b)[1]
def login(email):
 c=client();_,b,_=text(c,'index.php?login=1');s,b,_=text(c,'index.php?login=1',{'csrf':token(b),'login':1,'email':email,'password':'Local-test-password-2026!'});ok(s==200 and 'Sign out' in b,'login '+email);return c
def clean(s,b):return s==200 and all(x not in b for x in ['Fatal error','Warning:','SQLSTATE'])
admin=login('admin@test.local');librarian=login('librarian@test.local');stock=login('stock@test.local');approver=login('approver@test.local');editor=login('editor@test.local');publisher=login('publisher@test.local');comms=login('comms@test.local');asset=login('assets@test.local');parent=login('parent@test.local');student=login('student@test.local');teacher=login('teacher@test.local');foreign=login('foreignhr@test.local')
for c,area,views in [(librarian,'library',['catalogue','resources','loans','reservations','overdue','history','reports','labels']),(stock,'inventory',['store','orders','requests','stock','suppliers','purchases','alerts','audits']),(asset,'inventory',['assets','depreciation','maintenance']),(comms,'engagement',['feed','events','messages','consent','compose','campaigns','templates','logs','credits','providers']),(admin,'website',['site','content','approval','domains','enquiries','tours'])]:
 for view in views:
  s,b,_=text(c,'index.php?s=services&area='+area+'&view='+view);ok(clean(s,b) and 'op-card' in b,'HTTP '+area+' '+view)
for c,label in [(parent,'parent'),(student,'student')]:
 for area,view in [('library','history'),('inventory','orders'),('engagement','feed'),('engagement','consent')]:
  s,b,_=text(c,'index.php?s=services&area='+area+'&view='+view);ok(clean(s,b) and 'op-card' in b and 'Private maintenance findings' not in b,label+' scoped '+area+' '+view)
 s,b,_=text(c,'index.php?s=services&area=website');ok(clean(s,b) and 'Website editor or approver access required' in b and 'visitor@test.local' not in b,label+' denied CMS management')
# Submit an identifiable gallery with a real safe image; drafts/media stay private until publication.
def upload(kind,slug,name,mime,content):
 _,b,_=text(editor,'index.php?s=services&area=website&view=content');boundary='SchoolOSCMSMediaBoundary';fields={'csrf':token(b),'sv_action':'wc_content','kind':kind,'slug':slug,'title':'HTTP '+kind,'body':'HTTP PUBLIC '+kind,'publication_consent':'yes','consent_note':'Synthetic publication-consent fixture'};parts=[]
 for k,v in fields.items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
 parts += [f'--{boundary}\r\nContent-Disposition: form-data; name="media"; filename="{name}"\r\nContent-Type: {mime}\r\n\r\n'.encode()+content+b'\r\n',f'--{boundary}--\r\n'.encode()];s,raw,_=req(editor,'index.php?s=services&area=website&view=content',b''.join(parts),{'Content-Type':'multipart/form-data; boundary='+boundary});b=raw.decode();ok(clean(s,b) and 'Draft revision saved' in b,'real CMS upload '+kind);return re.findall(r'wc_preview=(\d+)',b)[0]
_,b,_=text(admin,'index.php?s=services&area=website&view=site');site=re.search(r'school=([a-f0-9]{40})',b)[1];public=client()
im=Image.new('RGB',(12,12),(25,130,120));buf=io.BytesIO();im.save(buf,format='PNG');image=buf.getvalue();gallery=upload('gallery','http-gallery','gallery.png','image/png',image)
s,b,_=text(public,'index.php?school='+site+'&media='+gallery);ok(s==404,'unpublished gallery media unavailable publicly')
s,b,_=text(parent,'index.php?wc_preview='+gallery);ok(s==403,'parent denied private content preview');s,b,_=text(foreign,'index.php?wc_preview='+gallery);ok(s==403,'cross-school private preview denied');s,b,_=text(editor,'index.php?wc_preview='+gallery);ok(clean(s,b) and 'Private preview' in b,'editor authenticated preview')
def post(c,view,data):
 _,b,_=text(c,'index.php?s=services&area=website&view='+view);return text(c,'index.php?s=services&area=website&view='+view,{'csrf':token(b)}|data)
def publish(id):
 s,b,_=post(editor,'content',{'sv_action':'wc_submit','content_id':id});assert clean(s,b) and 'Content submitted' in b
 s,b,_=post(publisher,'approval',{'sv_action':'wc_review','content_id':id,'status':'published','review_note':'Synthetic safe media reviewed'});ok(clean(s,b) and 'Content review saved' in b,'independent CMS approval #'+id)
publish(gallery);s,b,h=req(public,'index.php?school='+site+'&media='+gallery);ok(s==200 and b==image and h.get('Content-Type')=='image/png' and h.get('X-Content-Type-Options')=='nosniff','approved gallery image safely served')
pdf=b'%PDF-1.4\n1 0 obj << /Type /Catalog >> endobj\n%%EOF';prospectus=upload('prospectus','http-prospectus','prospectus.pdf','application/pdf',pdf);publish(prospectus);s,b,h=req(public,'index.php?school='+site+'&media='+prospectus);ok(s==200 and b==pdf and 'attachment' in h.get('Content-Disposition','') and h.get('Content-Security-Policy')=='sandbox','approved prospectus downloaded with safe headers')
# Prevent executable files masquerading as gallery images.
_,b,_=text(editor,'index.php?s=services&area=website&view=content');boundary='CMSInvalidFile';body=(f'--{boundary}\r\nContent-Disposition: form-data; name="csrf"\r\n\r\n{token(b)}\r\n--{boundary}\r\nContent-Disposition: form-data; name="sv_action"\r\n\r\nwc_content\r\n--{boundary}\r\nContent-Disposition: form-data; name="kind"\r\n\r\ngallery\r\n--{boundary}\r\nContent-Disposition: form-data; name="slug"\r\n\r\nunsafe\r\n--{boundary}\r\nContent-Disposition: form-data; name="publication_consent"\r\n\r\nyes\r\n--{boundary}\r\nContent-Disposition: form-data; name="consent_note"\r\n\r\nTest\r\n--{boundary}\r\nContent-Disposition: form-data; name="media"; filename="malicious.png"\r\nContent-Type: image/png\r\n\n<?php echo 1; ?>\r\n--{boundary}--\r\n').encode();s,b,_=req(editor,'index.php?s=services&area=website&view=content',body,{'Content-Type':'multipart/form-data; boundary='+boundary});ok(s==200 and b'Only PDF, JPEG, PNG or WebP' in b,'disguised executable CMS upload rejected')
# Approved plain text remains escaped.
s,b,_=post(editor,'content',{'sv_action':'wc_content','kind':'news','slug':'http-xss','title':'<script>alert(1)</script>','body':'<img src=x onerror=alert(1)>'});assert 'Draft revision saved' in b;xss=re.findall(r'wc_preview=(\d+)',b)[0];publish(xss)
for page,label in [('home','Home'),('news','News'),('galleries','Gallery'),('admissions','Admissions'),('events','Events'),('staff','Our people'),('testimonials','Testimonials'),('prospectus','Prospectus'),('tours','School tours')]:
 s,b,h=text(public,'index.php?school='+site+'&page='+page);ok(clean(s,b) and 'Test Academy' in b and 'visitor@test.local' not in b and h.get('Referrer-Policy')=='no-referrer','public CMS '+page)
s,b,_=text(public,'index.php?school='+site+'&page=news');ok('&lt;script&gt;' in b and '<script>alert(1)</script>' not in b and '<img src=x onerror=' not in b,'public CMS escapes untrusted content')
s,b,_=text(public,'index.php?school='+site);nonce=re.search(r'name="nonce" value="([a-f0-9]{64})"',b)[1];fields={'csrf':token(b),'nonce':nonce,'wc_public_action':'enquiry','privacy_consent':'yes','name':'HTTP Prospective Guardian','email':'httpprospect@test.local','phone':'08000000009','interest':'Primary','message':'Please contact me'};s,b,_=text(public,'index.php?school='+site,fields);ok(clean(s,b) and 'Enquiry received' in b,'public enquiry form and PRG');s,b,_=text(public,'index.php?school='+site,fields);ok(clean(s,b) and 'Form expired' in b,'public enquiry replay denied');s,b,_=text(publisher,'index.php?s=services&area=website&view=enquiries');ok(clean(s,b) and 'HTTP Prospective Guardian' in b,'public enquiry appears in authorized admissions list')
s,b,_=text(public,'index.php?school='+('0'*40));ok(s==404,'unknown school token is a 404');s,b,_=text(public,'index.php?school='+site+'&booking='+('0'*64));ok(s==404,'unknown private booking token denied');s,b,_=text(public,'index.php?eg_webhook=1',{'invalid':'body'});ok(s==403,'unsigned provider callback denied over HTTP')
for f in ['services_core.php','library_manager.php','inventory_manager.php','engagement_manager.php','website_cms.php']:
 s,b,_=text(public,f);ok(s==403 or clean(s,b),'direct service library guarded '+f)
s,b,_=text(public,'services_worker.php');ok(s==403,'cron worker denied through web')
r=subprocess.run([PHP,str(ROOT/'services_worker.php'),'--tenant=1','--limit=10'],capture_output=True,text=True);ok(r.returncode==0 and r.stdout.startswith('Processed ') and '<html' not in r.stdout,'actual cPanel-style CLI worker bootstraps without webpage output')
_,b,_=text(admin,'index.php?s=services&area=engagement&view=providers');s,b,_=text(admin,'index.php?s=services&area=engagement&view=providers',{'csrf':token(b),'sv_action':'eg_provider_settings','termii_key':'HTTPPrivateSyntheticKey490'});ok(clean(s,b) and 'Provider settings encrypted and saved' in b and 'HTTPPrivateSyntheticKey490' not in b,'HTTP encrypted provider save never redisplays secret');_,b,_=text(comms,'index.php?s=services&area=engagement&view=consent');s,b,_=text(comms,'index.php?s=services&area=engagement&view=providers',{'csrf':token(b),'sv_action':'eg_provider_settings','termii_key':'ForbiddenKey'});ok(clean(s,b) and 'Only the school administrator' in b and 'ForbiddenKey' not in b,'provider settings require school administrator');
_,b,_=text(parent,'index.php?s=announcements');match=re.search(r'name=\"post_id\" value=\"(\d+)\"',b);assert match
_,b,_=text(admin,'index.php?s=announcements');s,b,_=text(admin,'index.php?s=announcements',{'csrf':token(b),'cm_action':'email','post_id':match[1],'email':'unverified@test.local'});ok(clean(s,b) and 'Choose one verified recipient' in b,'legacy Community email action uses verified-contact queue guard');
for area in ['library','inventory','engagement','website']:
 s,b,_=text(admin,'index.php?s=services&area='+area,{'csrf':'invalid','sv_action':'activate'});ok(clean(s,b) and 'Security token expired' in b,'HTTP CSRF denial '+area)
for path,expected,c in [('index.php','Give your school',public),('index.php?s=family&child=1&view=homework','Complete page 12',parent),('index.php?s=learning&view=classes','Teacher Portal',teacher),('index.php?s=fees','Finance',admin),('index.php?s=announcements','Community',admin),('index.php?s=operations&area=hr','Staff records',admin),('index.php?s=books','Catalogue & ISBN',admin),('index.php?s=inventory','School store',admin),('index.php?s=assets','Asset register',admin)]:
 s,b,_=text(c,path);ok(clean(s,b) and expected.lower() in html.unescape(b).lower(),'existing route '+path)
print('TOTAL',n,'passed')
