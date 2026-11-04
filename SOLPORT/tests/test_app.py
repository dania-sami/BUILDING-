import os,sys,tempfile
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
import app
from fastapi.testclient import TestClient
client=TestClient(app.app)
def test_desk():
 r=client.get('/api/desk');assert r.status_code==200;assert len(r.json()['invoices'])==4
def test_preview():
 r=client.get('/api/payment-preview');assert r.status_code==200;assert 'DEMO ONLY' in r.json()['notice']
def test_export():
 r=client.get('/api/payment-export');assert r.status_code==200;assert 'DEMO ONLY' in r.text
def test_invalid_invoice():
 assert client.post('/api/invoices/99999/approve').status_code==404
def test_followup_validation():
 assert client.post('/api/rents/1/follow-up',json={'note':''}).status_code==400
def test_reconciliation_validation():
 assert client.post('/api/bank/1/match',json={'note':''}).status_code==400
