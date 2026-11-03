from app.core import answer,evaluate,estimate,retrieve
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_grounded():
 r=answer('What is required before releasing to production?');assert r['status']=='grounded';assert r['citations']
def test_abstain():assert answer('What is the office cafeteria menu tomorrow?')['status']=='abstain'
def test_eval():
 r=evaluate();assert r['total']==8;assert r['passed']>=6
def test_cost():assert estimate(1000,500,200,2,8)['monthly_usd']==2.6
def test_api():assert client.get('/api/health').status_code==200;assert client.post('/api/ask',json={'question':'How do we measure retrieval quality?'}).status_code==200
def test_report():assert 'production_gaps' in client.get('/api/report').json()
