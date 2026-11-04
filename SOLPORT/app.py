from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from datetime import date
from io import StringIO
import sqlite3, csv, os

BASE=os.path.dirname(__file__)
DB=os.path.join(BASE,'solport.db')
app=FastAPI(title='SOLPORT | CFO Daily Desk')

def conn():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init():
 with conn() as c:
  c.executescript('''CREATE TABLE IF NOT EXISTS invoices(id INTEGER PRIMARY KEY, supplier TEXT, property TEXT, amount REAL, due TEXT, status TEXT, account TEXT);
 CREATE TABLE IF NOT EXISTS rents(id INTEGER PRIMARY KEY, tenant TEXT, property TEXT, amount REAL, due TEXT, status TEXT, note TEXT DEFAULT '');
 CREATE TABLE IF NOT EXISTS bank(id INTEGER PRIMARY KEY, description TEXT, amount REAL, matched INTEGER DEFAULT 0, reference TEXT DEFAULT '');
 CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT DEFAULT CURRENT_TIMESTAMP, action TEXT, detail TEXT);''')
  if not c.execute('SELECT 1 FROM invoices LIMIT 1').fetchone():
   c.executemany('INSERT INTO invoices VALUES (?,?,?,?,?,?,?)',[(1,'Nordic Heating','Solna 01',18450,'2026-11-08','pending','5060'),(2,'City Electric','Sundbyberg 04',7300,'2026-11-03','pending','5170'),(3,'Lift Service','Stockholm 12',12600,'2026-11-15','approved','5170'),(4,'Waterworks','Enköping 22',4950,'2026-11-06','pending','5140')])
   c.executemany('INSERT INTO rents(id,tenant,property,amount,due,status) VALUES (?,?,?,?,?,?)',[(1,'Northstar Studio','Solna 01',25500,'2026-10-31','overdue'),(2,'Green Corner','Sundbyberg 04',18900,'2026-11-01','overdue'),(3,'Atelier Eight','Stockholm 12',32000,'2026-11-30','current'),(4,'Bright Office','Enköping 22',14000,'2026-11-30','current')])
   c.executemany('INSERT INTO bank(id,description,amount,matched,reference) VALUES (?,?,?,?,?)',[(1,'Nordic Heating payment',-18450,0,''),(2,'Rent Atelier Eight',32000,0,''),(3,'Bank fee',-95,0,''),(4,'Green Corner rent',18900,0,'')])
init()

def rows(table):
 with conn() as c: return [dict(r) for r in c.execute('SELECT * FROM '+table+' ORDER BY id')]

@app.get('/api/desk')
def desk():
 inv=rows('invoices'); rent=rows('rents'); bank=rows('bank')
 return {'invoices':inv,'rents':rent,'bank':bank,'audit':rows('audit')[::-1][:30], 'metrics':{'pending_invoices':sum(x['status']=='pending' for x in inv),'overdue_rent_sek':sum(x['amount'] for x in rent if x['status']=='overdue'),'unmatched_bank':sum(not x['matched'] for x in bank),'approved_payments_sek':sum(x['amount'] for x in inv if x['status']=='approved')}}
class Action(BaseModel):
 note:str=''
@app.post('/api/invoices/{id}/approve')
def approve(id:int):
 with conn() as c:
  r=c.execute('SELECT * FROM invoices WHERE id=?',(id,)).fetchone()
  if not r: raise HTTPException(404,'Invoice not found')
  if r['status']!='pending': raise HTTPException(409,'Only pending invoices can be approved')
  c.execute("UPDATE invoices SET status='approved' WHERE id=?",(id,))
  c.execute('INSERT INTO audit(action,detail) VALUES (?,?)',('Invoice approved',f"#{id} {r['supplier']} SEK {r['amount']:,.2f}"))
 return {'ok':True}
@app.post('/api/rents/{id}/follow-up')
def followup(id:int,a:Action):
 if not a.note.strip(): raise HTTPException(400,'Enter a follow-up note')
 with conn() as c:
  r=c.execute('SELECT * FROM rents WHERE id=?',(id,)).fetchone()
  if not r: raise HTTPException(404,'Rent record not found')
  c.execute('UPDATE rents SET note=? WHERE id=?',(a.note.strip(),id))
  c.execute('INSERT INTO audit(action,detail) VALUES (?,?)',('Rent follow-up',f"#{id} {r['tenant']}: {a.note.strip()}"))
 return {'ok':True}
@app.post('/api/bank/{id}/match')
def match(id:int,a:Action):
 if not a.note.strip(): raise HTTPException(400,'A reconciliation reference is required')
 with conn() as c:
  r=c.execute('SELECT * FROM bank WHERE id=?',(id,)).fetchone()
  if not r: raise HTTPException(404,'Transaction not found')
  if r['matched']: raise HTTPException(409,'Already reconciled')
  c.execute('UPDATE bank SET matched=1, reference=? WHERE id=?',(a.note.strip(),id))
  c.execute('INSERT INTO audit(action,detail) VALUES (?,?)',('Bank matched',f"#{id} {r['description']} against {a.note.strip()}"))
 return {'ok':True}
@app.get('/api/payment-preview')
def payments():
 return {'notice':'DEMO ONLY. This preview cannot transmit payments to a bank.', 'items':[{'invoice_id':i['id'],'supplier':i['supplier'],'amount_sek':i['amount']} for i in rows('invoices') if i['status']=='approved']}
@app.get('/api/payment-export')
def export():
 s=StringIO(); w=csv.writer(s);w.writerow(['DEMO ONLY - NOT A BANK PAYMENT FILE']);w.writerow(['Invoice ID','Supplier','Amount SEK'])
 for i in rows('invoices'):
  if i['status']=='approved':w.writerow([i['id'],i['supplier'],f"{i['amount']:.2f}"])
 s.seek(0)
 return StreamingResponse(iter([s.getvalue()]),media_type='text/csv',headers={'Content-Disposition':'attachment; filename=solport_demo_payment_preview.csv'})
@app.get('/',response_class=HTMLResponse)
def home():return open(os.path.join(BASE,'index.html'),encoding='utf8').read()
