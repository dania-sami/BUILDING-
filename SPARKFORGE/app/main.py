import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from .core import CASES, DOCS, answer, business_case, recommendation, run_evaluations

BASE=Path(__file__).resolve().parents[1]
DB=BASE/'sparkforge.db'
app=FastAPI(title='SPARKFORGE',version='1.0.0')

def connection():
 db=sqlite3.connect(DB)
 db.row_factory=sqlite3.Row
 db.execute('CREATE TABLE IF NOT EXISTS decisions (id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT NOT NULL, decision TEXT NOT NULL, owner TEXT NOT NULL, notes TEXT NOT NULL, created_at TEXT NOT NULL)')
 db.commit()
 return db

class Question(BaseModel):
 question:str=Field(min_length=3,max_length=1000)
class Scenario(BaseModel):
 case_id:str
 adoption:float=Field(default=.7,ge=0,le=1)
 volume:float=Field(default=1,ge=.1,le=5)
class Decision(BaseModel):
 case_id:str
 decision:str=Field(min_length=5,max_length=300)
 owner:str=Field(min_length=2,max_length=100)
 notes:str=Field(min_length=10,max_length=2000)

def find_case(id):
 return next((c for c in CASES if c['id']==id),None)

@app.get('/')
def home():return FileResponse(BASE/'static'/'index.html')
@app.get('/api/cases')
def cases():return CASES
@app.get('/api/knowledge')
def knowledge():return DOCS
@app.post('/api/ask')
def ask(payload:Question):return answer(payload.question)
@app.post('/api/scenario')
def scenario(payload:Scenario):
 case=find_case(payload.case_id)
 if not case:raise HTTPException(404,'Unknown scenario')
 return {'case':case,'financials':business_case(case,payload.adoption,payload.volume),'recommendation':recommendation(case),'architecture':{'ingest':'Approved documents / event stream','control':'Access filtering and policy checks','intelligence':case['approach'],'validation':'Evaluation suite + human review','operations':'Monitoring, incident response and change control'}}
@app.get('/api/evaluations')
def evaluations():return run_evaluations()
@app.get('/api/decisions')
def decisions():
 with connection() as db:return [dict(r) for r in db.execute('SELECT * FROM decisions ORDER BY id DESC LIMIT 100')]
@app.post('/api/decisions',status_code=201)
def save_decision(payload:Decision):
 if not find_case(payload.case_id):raise HTTPException(404,'Unknown scenario')
 now=datetime.now(timezone.utc).isoformat()
 with connection() as db:
  cur=db.execute('INSERT INTO decisions(case_id,decision,owner,notes,created_at) VALUES (?,?,?,?,?)',(payload.case_id,payload.decision,payload.owner,payload.notes,now))
  db.commit()
 return {'id':cur.lastrowid,'created_at':now}
@app.get('/api/workshop/{case_id}')
def workshop(case_id:str):
 case=find_case(case_id)
 if not case:raise HTTPException(404,'Unknown scenario')
 return {'title':'From pain point to pilot','duration_minutes':45,'case':case['name'],'agenda':[{'minutes':8,'activity':'Map the current workflow and quantify the pain'},{'minutes':10,'activity':'Review available data and ownership'},{'minutes':10,'activity':'Choose AI pattern and define human control'},{'minutes':10,'activity':'Define evaluation metrics and pilot guardrails'},{'minutes':7,'activity':'Agree owners, next steps and go/no-go criteria'}],'questions':['Who owns the outcome?','Which data can the solution access?','What would make the pilot unsafe?','How will we know if it actually helps?'],'deliverable':'One-page pilot charter with baseline, owner, evaluation and stop conditions'}
