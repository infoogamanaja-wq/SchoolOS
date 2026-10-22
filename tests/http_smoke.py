#!/usr/bin/env python3
"""HTTP tests against an isolated installation + seeded schoolos_test database.
Usage: python tests/http.py http://127.0.0.1:8090
Never point this script at production: it creates test data and installs a database.
"""
import urllib.request as U, urllib.parse as P, urllib.error, http.cookiejar, re, sys, json
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8090').rstrip('/')
assert P.urlsplit(BASE).hostname in ('127.0.0.1','localhost'), 'Local test server only'
count=0
def ok(v,label):
 global count
 assert v,label
 count+=1;print('PASS',label)
def client(): return U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def req(c,path,data=None):
 try:
  r=c.open(BASE+path,P.urlencode(data).encode() if data is not None else None)
  return r.status,r.read().decode('utf8'),r.headers
 except urllib.error.HTTPError as e: return e.code,e.read().decode('utf8'),e.headers
def csrf(body):
 m=re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',body)
 assert m,'CSRF token present';return m[1]
def login(email):
 c=client();status,b,_=req(c,'/app/index.php?login=1');token=csrf(b)
 status,b,_=req(c,'/app/index.php?login=1',{'login':1,'email':email,'password':'Local-test-password-2026!','csrf':token})
 ok(status==200 and 'Sign out' in b,'login '+email)
 return c
c=client();s,b,h=req(c,'/installer/install.php');ok(s==200 and 'SchoolOS installation' in b,'fresh installer route');token=csrf(b)
s,b,h=req(c,'/installer/install.php',{'csrf':'invalid'});ok(s==200 and 'Installation failed.' in b,'installer rejects CSRF')
s,b,h=req(c,'/installer/install.php',{'csrf':token,'host':'localhost','name':'schoolos_installer','user':'root','pass':'','email':'installer@test.local','admin_pass':'Installer-test-password-2026!'})
ok(s==200 and 'Installation complete.' in b,'fresh installation on MariaDB')
s,b,h=req(c,'/installer/install.php');ok(s==403 and 'Already installed.' in b,'repeat installation blocked')
s,b,h=req(c,'/installer/index.php?login=1');ok(s==200 and 'SchoolOS Nigeria' in b,'fresh login route')
s,b,h=req(c,'/installer/index.php');ok(s==200 and 'Run your school' in b,'fresh public homepage')
c=client();s,b,h=req(c,'/app/index.php');ok(s==200 and 'Run your school' in b,'existing application homepage')
s,b,h=req(c,'/app/parent_portal.php');ok(s==200 and 'Sign in to your dashboard' not in b and 'SchoolOS Nigeria' in b,'direct parent module safely routes anonymous visitor to public application')
parent=login('parent@test.local')
for view in ['children','results','attendance','fees','receipts','homework','messages','calendar','bookings','absence','consent','pickup','transport','meals','documents','support','surveys']:
 s,b,h=req(parent,'/app/index.php?s=family&child=1&view='+view)
 ok(s==200 and 'Parent & Guardian Portal' in b and 'Fatal error' not in b and 'Warning:' not in b and 'PRIVATE-RECEIPT' not in b,'family HTTP '+view)
s,b,h=req(parent,'/app/index.php?s=family&child=0');ok(s==200 and 'Parent & Guardian Portal' in b,'zero child selects first linked child')
s,b,h=req(parent,'/app/index.php?s=family&child=-1');ok(s==403,'negative child ID forbidden')
s,b,h=req(parent,'/app/index.php?s=family&child=3');ok(s==403,'unlinked child route forbidden')
s,b,h=req(parent,'/app/index.php?s=family&child=4');ok(s==403,'foreign child route forbidden')
s,b,h=req(parent,'/app/index.php?s=family&child=1&pp_document=1');ok(s==200 and b.startswith('%PDF') and h['Content-Type']=='application/pdf' and 'no-store' in h['Cache-Control'],'authorized document download')
other=login('other@test.local');s,b,h=req(other,'/app/index.php?s=family&child=1&pp_document=1');ok(s==403,'unlinked document download forbidden')
s,b,h=req(parent,'/app/index.php?fn_receipt=1');ok(s==200 and 'Official payment receipt' in b and 'TEST-RECEIPT' in b,'linked child confirmed receipt')
s,b,h=req(parent,'/app/index.php?fn_receipt=2');ok(s==404,'same-tenant private receipt IDOR blocked')
s,b,h=req(parent,'/app/index.php?s=announcements');ok(s==200 and 'Class announcement' in b and 'PRIVATE POST' not in b,'Community Hub parent class integration')
s,b,h=req(parent,'/app/index.php?s=family&child=1&view=support');token=csrf(b)
s,b,h=req(parent,'/app/index.php?s=family&child=1&view=support',{'csrf':token,'pp_action':'ticket','child':1,'subject':'HTTP test ticket','body':'Please help with the parent portal'})
ok(s==200 and 'Support ticket opened' in b and 'HTTP test ticket' in b,'HTTP support form and redirect')
s,b,h=req(parent,'/app/index.php?s=family&child=1&view=absence',{'csrf':'bad','pp_action':'absence','child':1,'subject':'Invalid CSRF','body':'Must not save','starts_on':'2030-01-01','ends_on':'2030-01-02'})
ok(s==200 and 'Security token expired.' in b,'HTTP action rejects CSRF')
admin=login('admin@test.local')
for section,expected in [('family','school workspace'),('fees','Finance'),('announcements','Community'),('portal_links','Account links'),('students','Student directory')]:
 s,b,h=req(admin,'/app/index.php?s='+section);ok(s==200 and expected.lower() in b.lower() and 'Fatal error' not in b and 'Warning:' not in b,'school admin route '+section)
teacher=login('teacher@test.local');s,b,h=req(teacher,'/app/index.php?s=family');ok(s==200 and 'Requests and messages' in b,'teacher Family Space route')
platform=login('platform@test.local');s,b,h=req(platform,'/app/index.php?s=system');ok(s==200 and 'System Management' in b,'authenticated Update Manager route')
s,b,h=req(parent,'/app/index.php?s=system');ok('System Management' not in b,'parent denied Update Manager')
print('TOTAL',count,'passed')
