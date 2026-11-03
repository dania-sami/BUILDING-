from fastapi import FastAPI,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel,Field
from pathlib import Path
from .core import answer,evaluate,estimate,DOCS
import sqlite3,datetime,json,uuid
ROOT=Path(__file__).resolve().parent.parent
DB=ROOT/'architectiq.db'
app=FastAPI(title='ARCHITECTIQ | AI Architecture Delivery Lab',version='1.0')
app.mount('/static',StaticFiles(directory=ROOT/'static'),name='static')
def connect():
 con=sqlite3.connect(DB);con.row_factory=sqlite3.Row;return con
def init():
 with connect() as con:
  con.execute('CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY,at TEXT,kind TEXT,payload TEXT)')
  con.execute('CREATE TABLE IF NOT EXISTS decisions(id TEXT PRIMARY KEY,at TEXT,title TEXT,choice TEXT,rationale TEXT,risk TEXT,status TEXT)')
init()
def log(kind,payload):
 with connect() as con:con.execute('INSERT INTO events VALUES(?,?,?,?)',(str(uuid.uuid4())[:8],datetime.datetime.now(datetime.timezone.utc).isoformat(),kind,json.dumps(payload)))
class Question(BaseModel):question:str=Field(min_length=3,max_length=1000)
class Cost(BaseModel):requests:int=Field(ge=0,le=100000000);avg_input:int=Field(ge=0,le=1000000);avg_output:int=Field(ge=0,le=1000000);input_rate:float=Field(ge=0);output_rate:float=Field(ge=0)
class Decision(BaseModel):title:str=Field(min_length=3,max_length=120);choice:str=Field(min_length=3,max_length=300);rationale:str=Field(min_length=5,max_length=2000);risk:str=Field(min_length=3,max_length=1000)
@app.get('/')
def home():return FileResponse(ROOT/'static'/'index.html')
@app.get('/api/health')
def health():return {'status':'ok','mode':'synthetic offline evidence lab','documents':len(DOCS)}
@app.get('/api/documents')
def documents():return [{'id':d['id'],'title':d['title'],'domain':d['domain'],'text':d['text']} for d in DOCS]
@app.post('/api/ask')
def ask(q:Question):
 r=answer(q.question);log('retrieval',{'question':q.question,'status':r['status'],'citations':[x['id'] for x in r['citations']]});return r
@app.post('/api/evaluate')
def run_evals():
 r=evaluate();log('evaluation',{'passed':r['passed'],'total':r['total']});return r
@app.post('/api/cost')
def cost(c:Cost):return estimate(**c.model_dump())
@app.get('/api/decisions')
def decisions():
 with connect() as con:return [dict(r) for r in con.execute('SELECT * FROM decisions ORDER BY at DESC')]
@app.post('/api/decisions')
def create_decision(d:Decision):
 row={'id':str(uuid.uuid4())[:8],'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),**d.model_dump(),'status':'Proposed'}
 with connect() as con:con.execute('INSERT INTO decisions VALUES(:id,:at,:title,:choice,:rationale,:risk,:status)',row)
 log('architecture_decision',row);return row
@app.post('/api/decisions/{decision_id}/approve')
def approve(decision_id:str):
 with connect() as con:
  row=con.execute('SELECT * FROM decisions WHERE id=?',(decision_id,)).fetchone()
  if not row:raise HTTPException(404,'Decision not found')
  con.execute('UPDATE decisions SET status=? WHERE id=?',('Approved (simulation)',decision_id))
 log('approval_simulation',{'decision_id':decision_id});return {'status':'Approved (simulation)'}
@app.get('/api/events')
def events():
 with connect() as con:return [dict(r) for r in con.execute('SELECT * FROM events ORDER BY at DESC LIMIT 100')]
@app.get('/api/report')
def report():
 with connect() as con:ds=[dict(r) for r in con.execute('SELECT * FROM decisions ORDER BY at DESC')]
 return {'project':'Enterprise Knowledge Assistant','architecture':{'entry':'API gateway and enterprise identity','retrieval':'Document indexing, lexical evidence retrieval, permission-filtering requirement','response':'Extractive grounded response or abstention','observability':'SQLite local audit events; production tracing proposed','actions':'Human approval required for high-impact tools'},'evaluation':evaluate(),'decisions':ds,'production_gaps':['Connect real identity provider and enforce document ACLs','Replace lexical baseline with production retrieval and reranking','Add LLM with grounded response validation and prompt-injection defenses','Add distributed tracing, SLO dashboards, and alerts','Load test, threat model, and deploy via CI/CD'],'disclaimer':'Demonstration only. No production AI model, cloud deployment or real client data.'}
