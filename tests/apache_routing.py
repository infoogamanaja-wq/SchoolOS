#!/usr/bin/env python3
"""Apache 2.4 + PHP CGI smoke checks, local server only."""
import urllib.request as U,urllib.error,urllib.parse as P,re,http.cookiejar,sys
base=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8092').rstrip('/')
assert P.urlsplit(base).hostname in ('localhost','127.0.0.1')
c=U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()));n=0
def request(path,data=None):
 try:
  r=c.open(base+path,P.urlencode(data).encode() if data is not None else None);return r.status,r.read().decode()
 except urllib.error.HTTPError as e:return e.code,e.read().decode()
def ok(v,label):
 global n
 assert v,label
 print('PASS',label);n+=1
s,b=request('/');ok(s==200 and 'Run your school' in b,'Apache DirectoryIndex serves PHP homepage')
s,b=request('/nonexistent-public-route');ok(s==200 and 'Run your school' in b,'Apache rewrite falls back to application')
for path in ['/storage/system/version.json','/storage/system/backups/','/config.php','/.git/config','/database/schema.sql']:
 s,b=request(path);ok(s==403,'Apache blocks '+path)
s,b=request('/parent_portal.php');ok(s==200 and 'Run your school' in b,'Apache direct portal route redirects safely')
s,b=request('/index.php?login=1');token=re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',b)[1]
s,b=request('/index.php?login=1',{'csrf':token,'login':1,'email':'parent@test.local','password':'Local-test-password-2026!'})
s,b=request('/index.php?s=family&child=1&view=homework');ok(s==200 and 'Complete page 12' in b and 'Warning:' not in b,'Apache FastCGI authenticated parent route')
print('TOTAL',n,'passed')
