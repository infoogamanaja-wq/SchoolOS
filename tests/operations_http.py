#!/usr/bin/env python3
"""Role, private-file and routing checks against a disposable local operations fixture."""
import urllib.request as U,urllib.parse as P,urllib.error,http.cookiejar,re,sys
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8090/operations').rstrip('/');assert P.urlsplit(BASE).hostname in ('127.0.0.1','localhost');n=0
def ok(v,m):
 global n
 assert v,m;n+=1;print('PASS',m)
def client():return U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def req(c,path,data=None,headers={}):
 try:
  r=c.open(U.Request(BASE+'/'+path,data=P.urlencode(data).encode() if isinstance(data,dict) else data,headers=headers));return r.status,r.read().decode(),r.headers
 except urllib.error.HTTPError as e:return e.code,e.read().decode(),e.headers
def token(b):return re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',b)[1]
def login(email):
 c=client();_,b,_=req(c,'index.php?login=1');s,b,_=req(c,'index.php?login=1',{'csrf':token(b),'login':1,'email':email,'password':'Local-test-password-2026!'});ok(s==200 and 'Sign out' in b,'login '+email);return c
def clean(s,b):return s==200 and 'Fatal error' not in b and 'Warning:' not in b and 'SQLSTATE' not in b
hr=login('hr@test.local');admin=login('admin@test.local');driver=login('driver@test.local');warden=login('warden@test.local');otherwarden=login('otherwarden@test.local');parent=login('parent@test.local');student=login('student@test.local');teacher=login('teacher@test.local');foreign=login('foreignhr@test.local')
for c,area,views in [(hr,'hr',['records','recruitment','onboarding','contracts','departments','attendance','leave','duties','salaries','allowances','policy','payslips','advances','evaluations','development','grievances','exit']),(admin,'transport',['vehicles','drivers','routes','assignments','fees','trips','events','suggestions']),(driver,'transport',['trips','events']),(warden,'boarding',['dashboard','rooms','allocations','fees','movements','leave','visitors','roll','incidents','maintenance','supplies','meals']),(teacher,'hr',['records','onboarding','contracts','attendance','leave','duties','payslips','advances','evaluations','development','grievances','exit'])]:
 for view in views:
  s,b,_=req(c,'index.php?s=operations&area='+area+'&view='+view);ok(clean(s,b) and 'op-card' in b,'HTTP '+area+' '+view)
for c,label in [(parent,'parent'),(student,'student')]:
 for area in ['transport','boarding']:
  s,b,_=req(c,'index.php?s=operations&area='+area);ok(clean(s,b) and 'Amara' in b and 'Private resident details' not in b and 'Guardian visitor' not in b,label+' linked child '+area)
 s,b,_=req(c,'index.php?s=operations&area=hr');ok(s==403,label+' denied HR route')
s,b,_=req(otherwarden,'index.php?s=operations&area=boarding&view=incidents');ok(clean(s,b) and 'Private resident details' not in b,'unassigned warden private data denied')
s,b,_=req(foreign,'index.php?s=operations&area=hr&view=records');ok(clean(s,b) and 'Payroll Teacher' not in b,'other school personnel hidden')
s,b,_=req(teacher,'index.php?s=operations&op_payslip=1');ok(clean(s,b) and 'Payslip' in b and 'no-store' in _.get('Cache-Control',''),'own payslip private download')
for c,label in [(driver,'driver'),(parent,'parent'),(foreign,'foreign')]:
 s,b,_=req(c,'index.php?s=operations&op_payslip=1');ok(s==403,label+' cannot download another employee payslip')
s,b,_=req(hr,'index.php?s=operations&area=hr&view=contracts');csrf=token(b)
boundary='SchoolOSPersonnelBoundary';fields={'csrf':csrf,'op_action':'hr_item','employee_id':'1','kind':'contract','title':'HTTP private contract','body':'PRIVATE HTTP CONTRACT','starts_at':'2026-01-01T08:00','ends_at':'2027-01-01T08:00'};parts=[]
for k,v in fields.items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
pdf=b'%PDF-1.4\n1 0 obj << /Type /Catalog >> endobj\n%%EOF';parts += [f'--{boundary}\r\nContent-Disposition: form-data; name="document"; filename="terms.pdf"\r\nContent-Type: application/pdf\r\n\r\n'.encode()+pdf+b'\r\n',f'--{boundary}--\r\n'.encode()]
s,b,_=req(hr,'index.php?s=operations&area=hr&view=contracts',b''.join(parts),{'Content-Type':'multipart/form-data; boundary='+boundary});ok(clean(s,b) and 'Personnel item saved privately.' in b,'private PDF upload and PRG')
fileid=re.findall(r'op_hr_file=(\d+)',b)[-1];s,b,h=req(teacher,'index.php?s=operations&op_hr_file='+fileid);ok(s==200 and b.startswith('%PDF-') and h.get('X-Content-Type-Options')=='nosniff' and 'no-store' in h.get('Cache-Control',''),'employee private PDF access')
for c,label in [(driver,'peer'),(foreign,'cross-school'),(parent,'parent')]:
 s,b,_=req(c,'index.php?s=operations&op_hr_file='+fileid);ok(s==403,label+' private contract denied')
s,b,_=req(hr,'index.php?s=operations&area=hr&view=records',{'csrf':'bad','op_action':'hr_staff','name':'CSRF INJECTION','role_title':'Bad'});ok(clean(s,b) and 'Security token expired' in b and 'CSRF INJECTION' not in b,'HTTP CSRF denial')
for f in ['operations_core.php','hr_payroll.php','transport_portal.php','boarding_portal.php']:
 s,b,_=req(client(),f);ok(s==403 or (clean(s,b) and ('Sign in' in b or 'School Operations' in b)),'direct library guarded '+f)
for route in ['staff','vehicles','hostels']:
 s,b,_=req(admin,'index.php?s='+route);ok(clean(s,b) and 'School Operations' in b,'legacy route '+route)
for path,text in [('index.php','Run your school'),('index.php?s=family&child=1&view=homework','Complete page 12'),('index.php?s=learning&view=classes','Teacher Portal'),('index.php?s=fees','Finance'),('index.php?s=announcements','Community')]:
 c=client() if path=='index.php' else parent if 'family' in path else teacher if 'learning' in path else admin;s,b,_=req(c,path);ok(clean(s,b) and text.lower() in b.lower(),'existing application '+path)
print('TOTAL',n,'passed')
