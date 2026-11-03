from fastapi.testclient import TestClient
from app.main import app
from app.core import CASES, answer, business_case, run_evaluations
client=TestClient(app)
def test_cases():assert len(client.get('/api/cases').json())==4
def test_scenario():
 r=client.post('/api/scenario',json={'case_id':'support','adoption':.7,'volume':1});assert r.status_code==200;assert 'payback_months' in r.json()['financials']
def test_invalid_case():assert client.post('/api/scenario',json={'case_id':'none'}).status_code==404
def test_unknown_question_abstains():assert answer('zzzz nonexistent quantum pineapple')['abstained']
def test_evaluations():
 result=run_evaluations();assert result['total']==8;assert result['passed']>=7
def test_workshop():assert len(client.get('/api/workshop/support').json()['agenda'])==5
def test_decision_validation():assert client.post('/api/decisions',json={'case_id':'support','decision':'go','owner':'a','notes':'x'}).status_code==422
def test_estimates():assert business_case(CASES[0],0)['net_monthly_sek']<business_case(CASES[0],1)['net_monthly_sek']
