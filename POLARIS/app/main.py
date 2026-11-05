from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from .engine import ROOT,DB,connect,ingest,overview,claims,answer,audit
import csv
app=FastAPI(title='POLARIS Insurance Data & AI Mission Control',version='1.0')
app.mount('/static',StaticFiles(directory=ROOT/'static'),name='static')
class Question(BaseModel):question:str
@app.get('/')
def home():return FileResponse(ROOT/'static/index.html')
@app.get('/api/overview')
def get_overview():return overview()
@app.get('/api/claims')
def get_claims(product:str|None=None,status:str|None=None):return claims(product,status)
@app.get('/api/quarantine')
def quarantine():
 c=connect();rows=[dict(x) for x in c.execute('SELECT * FROM quarantine ORDER BY claim_id')];c.close();return rows
@app.get('/api/audit')
def get_audit():return audit()
@app.post('/api/run')
def run():
 with (ROOT/'data/claims.csv').open(newline='') as f:rows=list(csv.DictReader(f))
 return ingest(rows)
@app.post('/api/ask')
def ask(q:Question):
 if not q.question.strip():raise HTTPException(400,'Question required')
 return answer(q.question)
@app.get('/api/health')
def health():return {'status':'ok','warehouse':'sqlite local demo','llm':'not connected'}
