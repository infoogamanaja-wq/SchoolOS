"""Real HTTP boundary checks against the disposable portal fixture."""
import urllib.request as U,urllib.parse as P,urllib.error,http.cookiejar,re,json
base='http://127.0.0.1:8090/experience/index.php';n=0

def ok(v,m):
 global n
 assert v,m;n+=1;print('PASS',m)
def request(c,q='',data=None,headers={}):
 try:
  r=c.open(U.Request(base+q,data=P.urlencode(data).encode() if data is not None else None,headers=headers));return r.status,r.read().decode(),r.headers
 except urllib.error.HTTPError as e:return e.code,e.read().decode(),e.headers
def token(b):return re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',b)[1]
def login(email):
 c=U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()));_,b,_=request(c,'?login=1');s,b,_=request(c,'?login=1',{'csrf':token(b),'login':1,'email':email,'password':'Local-test-password-2026!'});assert s==200 and 'Sign out' in b;return c,token(b)
parent,csrf=login('parent@test.local');teacher,tcsrf=login('teacher@test.local');outsider,ocsrf=login('other@test.local');foreign,fcsrf=login('foreign@test.local');learner,lcsrf=login('student@test.local')
s,b,h=request(parent,'?s=chat');thread=int(re.search(r'thread=(\d+)',b)[1]);s,b,h=request(parent,f'?px_api=chat_fetch&id={thread}&after=0',headers={'X-CSRF-Token':csrf});ok(s==200 and json.loads(b)['ok'],'member receives chat JSON');ok('no-store' in h['Cache-Control'],'conversation response cannot be cached')
for c,key,label in [(outsider,ocsrf,'unrelated parent'),(foreign,fcsrf,'foreign school')]:
 s,b,_=request(c,f'?px_api=chat_fetch&id={thread}',headers={'X-CSRF-Token':key});ok(s==403 and not json.loads(b)['ok'],label+' cannot fetch private conversation')
s,b,_=request(parent,f'?px_api=chat_fetch&id={thread}',headers={'X-CSRF-Token':'invalid'});ok(s==403,'API rejects invalid CSRF');s,b,_=request(parent,f'?px_api=chat_send&id={thread}',headers={'X-CSRF-Token':csrf});ok(s==403,'GET cannot send a message')
for area in ['operations','intelligence']:
 s,b,_=request(teacher,'?s='+area);ok(s==403,'teacher denied unassigned '+area)
s,b,_=request(teacher,'?s=services&area=website');ok(s==403,'teacher denied unrelated CMS');s,b,_=request(learner,'?s=family');ok('Parent & Guardian Portal' not in b,'learner cannot render parent portal');s,b,_=request(parent,'?fn_receipt=1');ok(s==200 and 'receipt' in b,'verified parent can open own receipt');s,b,_=request(foreign,'?fn_receipt=1');ok('receipt-totals' not in b,'foreign parent cannot open school receipt')
for f in ['portal_experience.php','portal_collaboration.php','classroom.php']:
 try:r=parent.open(base.rsplit('/',1)[0]+'/'+f);s=r.status
 except urllib.error.HTTPError as e:s=e.code
 ok(s==404,'direct module access denied '+f)
for key in ['owner','teacher','parent','student','driver','platform']:
 # Download with a fresh public client; PDFs have binary streams.
 r=U.urlopen(base+'?guide='+key+'&download=pdf');body=r.read();ok(r.status==200 and body.startswith(b'%PDF-'),'downloadable role guide '+key)
print('Portal HTTP:',n,'assertions passed.')
