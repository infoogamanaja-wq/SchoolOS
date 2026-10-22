#!/usr/bin/env python3
import urllib.request as U,urllib.error,http.cookiejar,urllib.parse as P,re
BASE='http://127.0.0.1:8090/experience/';n=0
client=U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def req(path,data=None,headers={}):
 try:
  r=client.open(U.Request(BASE+path,data=P.urlencode(data).encode() if data is not None else None,headers=headers));return r.status,r.read().decode()
 except urllib.error.HTTPError as e:return e.code,e.read().decode()
def ok(v,m):
 global n
 assert v,m;n+=1;print('PASS',m)
for name in ['affiliate.php','affiliate_worker.php','public_site.php','public_guides.php']:
 s,b=req(name);ok(s==404 and 'function ' not in b,'standalone module denied '+name)
s,b=req('index.php?v23_webhook=paystack',{}, {'X-Paystack-Signature':'invalid'});ok(s==401,'anonymous invalid payment callback rejected before homepage')
s,b=req('index.php?login=1');csrf=re.search('name="csrf" value="([^"]+)"',b)[1]
s,b=req('index.php?login=1',{'csrf':csrf,'login':1,'demo_mode':'yes','email':'schooladmin@demo.schoolos.test','password':'SchoolOS-Demo-Explore-2026!'});ok(s==200 and 'DEMO SANDBOX' in b,'isolated school demo login')
s,b=req('index.php?page=affiliate-account');ok(s==200 and 'unavailable in the shared school demo' in b,'demo cannot enroll or expose live affiliate finances')
s,b=req('index.php?page=affiliate-account',{'csrf':csrf,'af_action':'install'});ok('disabled in the shared demo' in b,'demo affiliate financial mutation fails closed')
s,b=req('index.php?logout=1');s,b=req('index.php?page=affiliate-account');ok('Sign in with your SchoolOS account' in b,'anonymous affiliate has explicit login route')
print('Affiliate HTTP:',n,'assertions passed.')
