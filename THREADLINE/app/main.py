from fastapi import FastAPI,HTTPException
from fastapi.responses import FileResponse,PlainTextResponse
from pydantic import BaseModel,Field
from pathlib import Path
from . import core
app=FastAPI(title='THREADLINE Requirements Studio',version='1.0')
ROOT=Path(__file__).resolve().parents[1]
core.init()
class Decision(BaseModel):
 conflict:str;choice:str;facilitator:str=Field(min_length=1);rationale:str=Field(min_length=12)
@app.get('/')
def home():return FileResponse(ROOT/'static/index.html')
@app.get('/api/workspace')
def workspace():return {'stakeholders':core.STAKEHOLDERS,'quotes':core.QUOTES,'requirements':core.allreq(),'conflicts':core.CONFLICTS,'decisions':core.decisions(),'quality':core.quality(),'events':core.events()}
@app.post('/api/decisions')
def decide(data:Decision):
 try:return core.resolve(**data.model_dump())
 except ValueError as e:raise HTTPException(400,str(e))
@app.get('/api/impact/{reqid}')
def impact(reqid:str):
 try:return core.impact(reqid)
 except ValueError as e:raise HTTPException(404,str(e))
@app.get('/api/report',response_class=PlainTextResponse)
def report():return core.report()
