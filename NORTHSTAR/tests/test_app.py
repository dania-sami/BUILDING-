from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_graph():
 d=client.get('/api/graph').json();assert len(d['requirements'])==6 and len(d['interfaces'])==4
def test_coverage():
 d=client.get('/api/coverage').json();assert d['covered']==d['total']==6
def test_impact():
 d=client.get('/api/impact/REQ-001').json();assert len(d['components'])==2 and len(d['tests'])==1 and len(d['risks'])==1
def test_invalid_requirement():assert client.get('/api/impact/UNKNOWN').status_code==404
def test_change_validation():assert client.post('/api/requirements/REQ-001/change',json={'statement':'short','reason':'no'}).status_code==422
def test_review():assert client.get('/api/review').json()['scenario']['name']=='Harbor Safety Monitoring System'
