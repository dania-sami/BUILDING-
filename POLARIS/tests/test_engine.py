from app.engine import validate,risk_band,ingest,overview,claims,answer
from fastapi.testclient import TestClient
from app.main import app
import csv
from pathlib import Path
GOOD={'claim_id':'C1','policy_id':'P1','product':'Boat','reported_amount':'1500','status':'Open','event_date':'2026-10-01','description':'test'}
def test_valid():assert validate(GOOD) is None
def test_negative():assert validate({**GOOD,'reported_amount':'-1'})
def test_unknown_product():assert validate({**GOOD,'product':'Rocket'})
def test_bad_date():assert validate({**GOOD,'event_date':'yesterday'})
def test_missing_id():assert validate({**GOOD,'claim_id':''})
def test_risk():assert [risk_band(x) for x in [500,25000,100000]]==['Low','Medium','High']
def test_ingest_idempotent(tmp_path):
 db=tmp_path/'test.db';assert ingest([GOOD],db)['valid']==1;ingest([GOOD],db);assert overview(db)['totals']['n']==1
def test_quarantine(tmp_path):
 db=tmp_path/'test.db';r=ingest([GOOD,{**GOOD,'claim_id':'C2','reported_amount':'abc'}],db);assert r['rejected']==1;assert overview(db)['rejected']==1
def test_evidence(tmp_path):
 db=tmp_path/'test.db';ingest([GOOD],db);a=answer('open Boat claims',db);assert a['evidence'][0]['claim_id']=='C1'
def test_abstain(tmp_path):
 db=tmp_path/'test.db';ingest([GOOD],db);assert answer('Pet claims',db)['evidence']==[]
def test_health():assert TestClient(app).get('/api/health').status_code==200
def test_api_question():assert TestClient(app).post('/api/ask',json={'question':''}).status_code==400
