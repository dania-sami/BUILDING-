from fastapi.testclient import TestClient
from app.main import app,analyze,dataset
client=TestClient(app)
def test_analysis():
 a=analyze(dataset());assert a['revenue']>0 and a['margin']<1
 assert {x['id'] for x in a['findings']}=={'F01','F02','F03','F04','F05'}
def test_api():assert client.get('/api/analysis').status_code==200
def test_workflow():assert client.get('/api/workflow').json()['automated_checks']==5
def test_invalid_review():assert client.post('/api/reviews',json={'finding_id':'bad','status':'Resolved','owner':'a','note':'b'}).status_code==422
def test_prompts():assert len(client.get('/api/prompts').json())==3
