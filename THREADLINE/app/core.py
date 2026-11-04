import json,sqlite3,os
from pathlib import Path
DB=Path(os.environ.get('THREADLINE_DB',Path(__file__).resolve().parents[1]/'threadline.db'))
STAKEHOLDERS=[{'id':'S1','name':'Maja Lind','role':'Service owner','goal':'Launch a usable booking service this quarter'},{'id':'S2','name':'Oskar Berg','role':'Security lead','goal':'Protect sensitive resident information'},{'id':'S3','name':'Elin Holm','role':'Accessibility advisor','goal':'Make the service usable for everyone'},{'id':'S4','name':'Noah Ek','role':'Delivery lead','goal':'Keep scope and dependencies manageable'},{'id':'S5','name':'Sara Nilsson','role':'Citizen representative','goal':'Make booking fast and understandable'}]
REQUIREMENTS=[{'id':'R01','title':'Book a municipal appointment','description':'Residents can reserve an available service appointment.','owner':'S1','priority':'Must','status':'Proposed','acceptance':'Given an available slot, when a resident confirms, then a booking reference is issued.','depends':[],'stories':['US01']},{'id':'R02','title':'Optional sign-in for low-risk bookings','description':'Allow guest bookings for general information appointments.','owner':'S5','priority':'Should','status':'Proposed','acceptance':'Given a general appointment, when a guest books, then no account is required.','depends':['R01'],'stories':['US01']},{'id':'R03','title':'Verified identity for sensitive services','description':'Require verified identity for appointments involving protected records.','owner':'S2','priority':'Must','status':'Proposed','acceptance':'Given a sensitive service, when identity is unverified, then booking is blocked with guidance.','depends':['R01'],'stories':['US02']},{'id':'R04','title':'Accessible booking journey','description':'Support keyboard navigation and clear error messages.','owner':'S3','priority':'Must','status':'Proposed','acceptance':'Given keyboard-only use, when booking, then every step is operable without a mouse.','depends':['R01'],'stories':['US03']},{'id':'R05','title':'Appointment reminders','description':'Send reminders with consent and minimal personal data.','owner':'S1','priority':'Could','status':'Proposed','acceptance':'Given consent, when the reminder window starts, then one reminder is delivered.','depends':['R01'],'stories':['US04']},{'id':'R06','title':'Capacity synchronization','description':'Prevent double bookings using the legacy calendar API.','owner':'S4','priority':'Must','status':'Proposed','acceptance':'Given two simultaneous requests, when the last slot is booked, then only one succeeds.','depends':['R01'],'stories':['US05']}]
CONFLICTS=[{'id':'C01','title':'Fast access vs identity assurance','left':'R02','right':'R03','stakeholders':['S5','S2'],'question':'Should every booking require verified identity?','options':[{'id':'A','label':'Require identity for every booking','rationale':'Stronger identity assurance, higher friction','effects':{'R02':'Deferred','R03':'Approved'}},{'id':'B','label':'Risk-based sign-in by service type','rationale':'Guest access for general services; verification for sensitive services','effects':{'R02':'Approved','R03':'Approved'}}]},{'id':'C02','title':'Launch scope vs accessibility','left':'R04','right':'R05','stakeholders':['S3','S4'],'question':'What must be delivered in the first release?','options':[{'id':'A','label':'Accessibility first; reminders later','rationale':'Protect core usability while reducing initial scope','effects':{'R04':'Approved','R05':'Deferred'}},{'id':'B','label':'Deliver both with added testing capacity','rationale':'Broader scope with higher delivery risk','effects':{'R04':'Approved','R05':'Approved'}}]}]
QUOTES=[{'stakeholder':'S1','quote':'People should be able to book without calling our office.'},{'stakeholder':'S5','quote':'I should not need an account just to ask a general question.'},{'stakeholder':'S2','quote':'Sensitive appointments must not expose personal information.'},{'stakeholder':'S3','quote':'A keyboard-only user must be able to finish the booking.'},{'stakeholder':'S4','quote':'The old calendar can fail under simultaneous requests.'}]
def connect():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
def init():
 with connect() as c:
  c.execute('CREATE TABLE IF NOT EXISTS requirements(id TEXT PRIMARY KEY,title TEXT,description TEXT,owner TEXT,priority TEXT,status TEXT,acceptance TEXT,depends TEXT,stories TEXT)')
  c.execute('CREATE TABLE IF NOT EXISTS decisions(id INTEGER PRIMARY KEY AUTOINCREMENT,conflict TEXT,choice TEXT,rationale TEXT,facilitator TEXT,created TEXT DEFAULT CURRENT_TIMESTAMP)')
  c.execute('CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,kind TEXT,detail TEXT,created TEXT DEFAULT CURRENT_TIMESTAMP)')
  if not c.execute('SELECT COUNT(*) FROM requirements').fetchone()[0]:
   c.executemany('INSERT INTO requirements VALUES(?,?,?,?,?,?,?,?,?)',[(r['id'],r['title'],r['description'],r['owner'],r['priority'],r['status'],r['acceptance'],json.dumps(r['depends']),json.dumps(r['stories'])) for r in REQUIREMENTS])
def allreq():
 with connect() as c: rows=[dict(r) for r in c.execute('SELECT * FROM requirements ORDER BY id')]
 for r in rows:r['depends']=json.loads(r['depends']);r['stories']=json.loads(r['stories'])
 return rows
def decisions():
 with connect() as c:return [dict(x) for x in c.execute('SELECT * FROM decisions ORDER BY id DESC')]
def events():
 with connect() as c:return [dict(x) for x in c.execute('SELECT * FROM events ORDER BY id DESC LIMIT 100')]
def resolve(conflict,choice,facilitator,rationale):
 match=next((x for x in CONFLICTS if x['id']==conflict),None)
 if not match:raise ValueError('Unknown conflict')
 opt=next((x for x in match['options'] if x['id']==choice),None)
 if not opt:raise ValueError('Unknown option')
 if not facilitator.strip() or len(rationale.strip())<12:raise ValueError('Facilitator and meaningful decision rationale required')
 with connect() as c:
  for req,status in opt['effects'].items():c.execute('UPDATE requirements SET status=? WHERE id=?',(status,req))
  c.execute('INSERT INTO decisions(conflict,choice,rationale,facilitator) VALUES(?,?,?,?)',(conflict,opt['label'],rationale.strip(),facilitator.strip()))
  c.execute('INSERT INTO events(kind,detail) VALUES(?,?)',('Decision',f'{conflict}: {opt["label"]} by {facilitator.strip()}'))
 return {'conflict':conflict,'choice':opt['label'],'effects':opt['effects']}
def impact(reqid):
 reqs=allreq();target=next((r for r in reqs if r['id']==reqid),None)
 if not target:raise ValueError('Unknown requirement')
 downstream=[r for r in reqs if reqid in r['depends']]
 conflicts=[x['id'] for x in CONFLICTS if reqid in (x['left'],x['right'])]
 return {'target':target,'downstream':downstream,'conflicts':conflicts,'stories':target['stories']+list({s for r in downstream for s in r['stories']})}
def quality():
 reqs=allreq();missing=[r['id'] for r in reqs if not r['acceptance'].strip() or not r['owner'] or not r['stories']];unresolved=[x['id'] for x in CONFLICTS if not any(d['conflict']==x['id'] for d in decisions())];deferred=[r['id'] for r in reqs if r['status']=='Deferred']
 return {'requirements':len(reqs),'approved':sum(r['status']=='Approved' for r in reqs),'missing_traceability':missing,'unresolved_conflicts':unresolved,'deferred':deferred,'ready':not missing and not unresolved and all(r['status']!='Proposed' for r in reqs)}
def report():
 reqs=allreq();q=quality();return '\n'.join(['# THREADLINE | Requirements review','',f'Baseline ready: {q["ready"]}',f'Approved: {q["approved"]}/{q["requirements"]}',f'Unresolved conflicts: {", ".join(q["unresolved_conflicts"]) or "None"}','', '## Requirements']+[f'- {r["id"]} [{r["status"]}] {r["title"]} | {r["priority"]} | Owner {r["owner"]} | Tests: {r["acceptance"]}' for r in reqs]+['','## Decisions']+[f'- {d["conflict"]}: {d["choice"]} | {d["rationale"]} | {d["facilitator"]}' for d in decisions()])
