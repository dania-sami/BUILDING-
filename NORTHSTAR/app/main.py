from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pathlib import Path
import json, sqlite3, datetime
ROOT=Path(__file__).resolve().parent.parent
DB=ROOT/'northstar.db'
app=FastAPI(title='NORTHSTAR Systems Engineering Lab',version='1.0')
app.mount('/static',StaticFiles(directory=ROOT/'static'),name='static')
def conn():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
def init():
 with conn() as c:
  c.execute('CREATE TABLE IF NOT EXISTS requirements (id TEXT PRIMARY KEY, title TEXT, statement TEXT, priority TEXT, status TEXT, version INTEGER)')
  c.execute('CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, time TEXT, kind TEXT, detail TEXT)')
  if not c.execute('SELECT 1 FROM requirements LIMIT 1').fetchone():
   c.executemany('INSERT INTO requirements VALUES (?,?,?,?,?,?)',[(r['id'],r['title'],r['statement'],r['priority'],'Baselined',1) for r in SEED['requirements']])
init_seed_path=ROOT/'data'/'scenario.json'
SEED=json.loads(init_seed_path.read_text())
init()
def reqs():
 with conn() as c:return [dict(x) for x in c.execute('SELECT * FROM requirements ORDER BY id')]
def log(kind,detail):
 with conn() as c:c.execute('INSERT INTO events(time,kind,detail) VALUES(?,?,?)',(now(),kind,detail))
def graph():
 r=reqs(); links=SEED['links'];comps=SEED['components'];tests=SEED['tests'];risks=SEED['risks']
 return {'requirements':r,'components':comps,'tests':tests,'risks':risks,'links':links,'interfaces':SEED['interfaces']}
def impact(rid):
 g=graph(); ids={x['id'] for x in g['requirements']}
 if rid not in ids:raise HTTPException(404,'Unknown requirement')
 components=[x for x in g['components'] if {'from':rid,'to':x['id'],'type':'allocated_to'} in g['links']]
 compids={x['id'] for x in components}
 tests=[x for x in g['tests'] if {'from':rid,'to':x['id'],'type':'verified_by'} in g['links']]
 risks=[x for x in g['risks'] if {'from':rid,'to':x['id'],'type':'exposed_to'} in g['links']]
 interfaces=[x for x in g['interfaces'] if x['from'] in compids or x['to'] in compids]
 return {'requirement':rid,'components':components,'tests':tests,'risks':risks,'interfaces':interfaces,'review_actions':['Review allocated component design','Reassess interface compatibility','Update verification evidence','Revisit safety and reliability assumptions']}
class Change(BaseModel):
 statement:str=Field(min_length=15,max_length=500)
 reason:str=Field(min_length=8,max_length=300)
@app.get('/')
def home():return FileResponse(ROOT/'static'/'index.html')
@app.get('/api/graph')
def get_graph():return graph()
@app.get('/api/impact/{rid}')
def get_impact(rid:str):return impact(rid)
@app.post('/api/requirements/{rid}/change')
def change(rid:str,payload:Change):
 result=impact(rid)
 with conn() as c:
  c.execute("UPDATE requirements SET statement=?, status='Change review',version=version+1 WHERE id=?",(payload.statement,rid))
 log('CHANGE',f'{rid}: {payload.reason}; impacted {len(result["components"])} components, {len(result["tests"])} tests')
 return {'status':'review_required','impact':impact(rid)}
@app.get('/api/coverage')
def coverage():
 g=graph(); links=g['links']; rows=[]
 for r in g['requirements']:
  allocated=any(x['from']==r['id'] and x['type']=='allocated_to' for x in links)
  verified=any(x['from']==r['id'] and x['type']=='verified_by' for x in links)
  rows.append({'id':r['id'],'title':r['title'],'allocated':allocated,'verified':verified,'complete':allocated and verified})
 return {'rows':rows,'covered':sum(x['complete'] for x in rows),'total':len(rows)}
@app.get('/api/risks')
def risk_matrix():
 return [{**r,'score':r['severity']*r['likelihood'],'band':('High' if r['severity']*r['likelihood']>=12 else 'Medium' if r['severity']*r['likelihood']>=6 else 'Low')} for r in SEED['risks']]
@app.get('/api/review')
def review():
 return {'scenario':SEED['scenario'],'coverage':coverage(),'risks':risk_matrix(),'requirements':reqs(),'note':'Fictional engineering training scenario. No operational or classified information.'}
@app.get('/api/events')
def events():
 with conn() as c:return [dict(x) for x in c.execute('SELECT * FROM events ORDER BY id DESC LIMIT 100')]
