"""Local-only demo API, standard-library only. Never expose to the internet."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import json, sqlite3, datetime, os, sys
from engine import priority, severity, event_hash, verify_chain
ROOT=Path(__file__).resolve().parent
DB=ROOT/'data'/'lab.sqlite3'
SCENARIOS=json.loads((ROOT/'data'/'scenarios.json').read_text())

def connect():
    db=sqlite3.connect(DB); db.row_factory=sqlite3.Row
    db.execute('CREATE TABLE IF NOT EXISTS cases(id TEXT PRIMARY KEY, status TEXT NOT NULL, owner TEXT NOT NULL DEFAULT "Unassigned")')
    db.execute('CREATE TABLE IF NOT EXISTS evidence(seq INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL, event_type TEXT NOT NULL, detail TEXT NOT NULL, actor TEXT NOT NULL, timestamp TEXT NOT NULL, previous_hash TEXT NOT NULL, hash TEXT NOT NULL)')
    for c in SCENARIOS: db.execute('INSERT OR IGNORE INTO cases(id,status) VALUES(?,?)',(c['id'],c['status']))
    db.commit(); return db

def events(db): return [dict(x) for x in db.execute('SELECT * FROM evidence ORDER BY seq')]

def add_event(db,case_id,event_type,detail,actor):
    es=events(db)
    if not verify_chain(es): raise ValueError('Evidence integrity check failed; no changes allowed')
    previous=es[-1]['hash'] if es else 'GENESIS'
    payload=dict(case_id=case_id,event_type=event_type,detail=detail,actor=actor,timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat())
    db.execute('INSERT INTO evidence(case_id,event_type,detail,actor,timestamp,previous_hash,hash) VALUES(?,?,?,?,?,?,?)',(*payload.values(),previous,event_hash(previous,payload)))
    db.commit()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=str(ROOT/'web'),**kw)
    def send_json(self,data,code=200):
        b=json.dumps(data).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/api/cases':
            with connect() as db:
                states={x['id']:dict(x) for x in db.execute('SELECT * FROM cases')}
                self.send_json([dict(c,priority=priority(c),band=severity(priority(c)),status=states[c['id']]['status'],owner=states[c['id']]['owner']) for c in SCENARIOS]); return
        if path=='/api/evidence':
            with connect() as db:
                es=events(db); self.send_json({'verified':verify_chain(es),'events':es}); return
        if path=='/api/health': self.send_json({'service':'VEHICLE//GUARD LAB','mode':'local synthetic demo'}); return
        if path.startswith('/api/'): self.send_json({'error':'Not found'},404); return
        super().do_GET()
    def do_POST(self):
        if urlparse(self.path).path!='/api/action': self.send_json({'error':'Not found'},404); return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size>12000: raise ValueError('Request too large')
            data=json.loads(self.rfile.read(size)); cid=data.get('case_id'); kind=data.get('event_type'); detail=str(data.get('detail','')).strip(); actor=str(data.get('actor','Analyst')).strip()
            if cid not in {c['id'] for c in SCENARIOS}: raise ValueError('Unknown case')
            if kind not in ('Finding','Decision','Handoff','Status'): raise ValueError('Invalid event type')
            if not (2<=len(detail)<=600 and 1<=len(actor)<=60): raise ValueError('Invalid detail or actor length')
            with connect() as db:
                if kind=='Status':
                    if detail not in ('New','Investigating','Monitoring','Mitigated','Closed'): raise ValueError('Invalid status')
                    db.execute('UPDATE cases SET status=? WHERE id=?',(detail,cid)); db.commit()
                add_event(db,cid,kind,detail,actor)
            self.send_json({'ok':True})
        except (ValueError,KeyError,json.JSONDecodeError) as e: self.send_json({'error':str(e)},400)
    def log_message(self,*args): pass

if __name__=='__main__':
    connect().close(); port=int(os.environ.get('PSIRT_PORT','8765'))
    print(f'VEHICLE//GUARD LAB running at http://127.0.0.1:{port}')
    print('Local demo only. Press Ctrl+C to stop.')
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
