#!/usr/bin/env python3
"""HTTP Teacher/Student portal tests against a disposable local /learning installation."""
import urllib.request as U,urllib.parse as P,urllib.error,http.cookiejar,re,sys
BASE=(sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8090').rstrip('/')
assert P.urlsplit(BASE).hostname in ('127.0.0.1','localhost')
n=0
def ok(v,label):
 global n
 assert v,label;n+=1;print('PASS',label)
def client():return U.build_opener(U.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def req(c,path,data=None):
 try:
  r=c.open(BASE+'/learning/'+path,P.urlencode(data).encode() if isinstance(data,dict) else data);return r.status,r.read().decode(),r.headers
 except urllib.error.HTTPError as e:return e.code,e.read().decode(),e.headers
def token(b):return re.search(r'name=["\']?csrf["\']?\s+value=["\']([^"\']+)',b)[1]
def login(email,unlinked=False):
 c=client();_,b,_=req(c,'index.php?login=1');s,b,_=req(c,'index.php?login=1',{'csrf':token(b),'login':1,'email':email,'password':'Local-test-password-2026!'})
 ok((s==200 and 'A verified student link is still needed' in b) if unlinked else (s==200 and 'Sign out' in b),'login '+email);return c
teacher=login('teacher@test.local');student=login('student@test.local');other=login('student2@test.local');admin=login('admin@test.local');parent=login('parent@test.local')
for c,title,views in [(teacher,'Teacher Portal',['classes','attendance','timetable','lessons','syllabus','assignments','questions','scores','bulk','corrections','analytics','messages','resources','incidents','leave','pd','ai']),(student,'Student Portal',['dashboard','timetable','homework','resources','cbt','grades','attendance','feedback','announcements','clubs','library','badges','planner','ai'])]:
 for view in views:
  s,b,_=req(c,'index.php?s=learning&view='+view);ok(s==200 and title in b and 'Fatal error' not in b and 'Warning:' not in b and 'PRIVATE CONTENT' not in b and 'FOREIGN BOOK' not in b,'HTTP '+title+' '+view)
s,b,_=req(admin,'index.php?s=learning&view=manage');ok(s==200 and 'School controls and approvals' in b and 'Warning:' not in b,'school administrator approval screens')
s,b,_=req(parent,'index.php?s=learning');ok(s==403,'parent denied Teacher/Student portal')
unlinked=login('unlinked@test.local',unlinked=True);s,b,_=req(unlinked,'index.php?s=learning');ok(s==403,'unlinked student route denied')
s,b,_=req(student,'learning_portal.php');ok(s==200 and 'Student Portal' in b,'direct module routes through authenticated application')
for path in ['index.php?s=exams&attempt=1','index.php?s=learning&view=cbt&attempt=1']:
 s,b,_=req(other,path);ok(s==403,'another student attempt route denied '+path)
s,b,_=req(student,'index.php?s=learning&view=planner');csrf=token(b);s,b,_=req(student,'index.php?s=learning&view=planner',{'csrf':csrf,'lp_action':'planner','title':'HTTP study goal','due_on':'2030-01-15'});ok(s==200 and 'Study task added.' in b and 'HTTP study goal' in b,'study planner form and PRG redirect')
s,b,_=req(teacher,'index.php?s=learning&view=resources',{'csrf':'invalid','lp_action':'resource','class_id':1,'subject_id':1,'title':'CSRF ATTEMPT','url':'https://example.org'});ok(s==200 and 'Security token expired.' in b and 'CSRF ATTEMPT' not in b,'HTTP CSRF denial')
s,b,_=req(student,'index.php?s=learning&view=homework');csrf=token(b);s,b,_=req(student,'index.php?s=courses',{'csrf':csrf,'lm_action':'submit','lesson_id':1,'course_id':1,'answer':'Erase my grade via old form'});ok('Graded work is locked.' in b,'legacy LMS cannot erase a graded submission')
s,b,_=req(teacher,'index.php?s=learning&view=attendance');csrf=token(b);s,b,_=req(teacher,'index.php?s=attendance',{'csrf':csrf,'aw_action':'daily','student_id':5,'status':'present'});ok(s==403,'legacy welfare form cannot bypass teacher allocation')
for path,text in [('index.php?s=family&child=1&view=messages','Amara is improving'),('index.php?s=fees','Finance'),('index.php?s=announcements','Community')]:
 c=parent if 'family' in path else admin;s,b,_=req(c,path);ok(s==200 and text.lower() in b.lower() and 'Fatal error' not in b and 'Warning:' not in b,'existing integration '+path)
# Upload score CSV to a new test assessment (ID 3); fixture creates it for HTTP preview/commit testing.
def multipart(c,path,fields,filename,content,field='csv',mime='text/csv'):
 boundary='SchoolOSLearningBoundary';parts=[]
 for k,v in fields.items():parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
 parts += [f'--{boundary}\r\nContent-Disposition: form-data; name="{field}"; filename="{filename}"\r\nContent-Type: {mime}\r\n\r\n'.encode()+content+b'\r\n',f'--{boundary}--\r\n'.encode()]
 try:
  r=c.open(U.Request(BASE+'/learning/'+path,data=b''.join(parts),headers={'Content-Type':'multipart/form-data; boundary='+boundary}));return r.status,r.read().decode()
 except urllib.error.HTTPError as e:return e.code,e.read().decode()
s,b,_=req(teacher,'index.php?s=learning&view=bulk');csrf=token(b)
s,b=multipart(teacher,'index.php?s=learning&view=bulk',{'csrf':csrf,'lp_action':'bulk_preview','assessment_id':3},'scores.csv',b'student_no,score\nTEST-1,22\nTEST-2,24\n');ok(s==200 and 'CSV validated.' in b and 'Confirm import' in b,'actual CSV multipart upload previews rows')
s,b,_=req(teacher,'index.php?s=learning&view=bulk',{'csrf':token(b),'lp_action':'bulk_commit'});ok(s==200 and 'All CSV rows imported atomically' in b,'CSV preview confirmation commits rows')
s,b,_=req(other,'index.php?s=learning&view=homework');csrf=token(b)
s,b=multipart(other,'index.php?s=learning&view=homework',{'csrf':csrf,'lp_action':'submit','lesson_id':1,'answer':'Attached working'},'working.txt',b'Student working with fraction diagrams',field='attachment',mime='text/plain');ok(s==200 and 'Homework submitted.' in b,'actual homework attachment accepted in protected database storage')
links=re.findall(r'lp_file=(\d+)',b);assert links
s,b,h=req(other,'index.php?s=learning&lp_file='+links[0]);ok(s==200 and 'Student working' in b and h['Cache-Control']=='private, no-store','owner downloads homework attachment')
s,b,_=req(student,'index.php?s=learning&lp_file='+links[0]);ok(s==403,'other student homework download denied')
print('TOTAL',n,'passed')
