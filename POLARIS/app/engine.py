"""Deterministic insurance ETL and explainable retrieval. No external APIs."""
import csv, io, sqlite3, json, hashlib, datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'polaris.db'
SCHEMA="""CREATE TABLE IF NOT EXISTS raw_claims(claim_id TEXT PRIMARY KEY, policy_id TEXT, product TEXT, reported_amount REAL, status TEXT, event_date TEXT, description TEXT, ingested_at TEXT);
CREATE TABLE IF NOT EXISTS fact_claims(claim_id TEXT PRIMARY KEY, policy_id TEXT, product TEXT, reported_amount REAL, status TEXT, event_date TEXT, description TEXT, risk_band TEXT);
CREATE TABLE IF NOT EXISTS quarantine(claim_id TEXT PRIMARY KEY, reason TEXT, payload TEXT);
CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY AUTOINCREMENT, run_at TEXT, loaded INTEGER, valid INTEGER, rejected INTEGER, checksum TEXT);
CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT, event_at TEXT, action TEXT, detail TEXT);"""
PRODUCTS={'Motorcycle','Boat','Pet','Car','Home','Business'}
STATUSES={'Open','Review','Settled'}
def connect(path=DB):
 c=sqlite3.connect(str(path)); c.row_factory=sqlite3.Row; c.executescript(SCHEMA); return c
def validate(row):
 if not row.get('claim_id') or not row.get('policy_id'): return 'Missing claim or policy identifier'
 if row.get('product') not in PRODUCTS:return 'Unknown product'
 try: amount=float(row.get('reported_amount',''))
 except (ValueError,TypeError):return 'Invalid amount'
 if amount<0 or amount>2000000:return 'Amount outside allowed range'
 if row.get('status') not in STATUSES:return 'Unknown status'
 try:datetime.date.fromisoformat(row.get('event_date',''))
 except (ValueError,TypeError):return 'Invalid event date'
 return None
def risk_band(amount):return 'High' if amount>=100000 else ('Medium' if amount>=25000 else 'Low')
def ingest(rows,path=DB):
 c=connect(path); now=datetime.datetime.now(datetime.timezone.utc).isoformat(); loaded=0;valid=0;rejected=0
 for row in rows:
  loaded+=1; row=dict(row); cid=row.get('claim_id') or 'INVALID-'+str(loaded)
  reason=validate(row)
  if reason:
   rejected+=1;c.execute('INSERT OR REPLACE INTO quarantine VALUES(?,?,?)',(cid,reason,json.dumps(row)));continue
  valid+=1;amount=float(row['reported_amount']); vals=(cid,row['policy_id'],row['product'],amount,row['status'],row['event_date'],row.get('description',''))
  c.execute('INSERT OR REPLACE INTO raw_claims VALUES(?,?,?,?,?,?,?,?)',(*vals,now))
  c.execute('INSERT OR REPLACE INTO fact_claims VALUES(?,?,?,?,?,?,?,?)',(*vals,risk_band(amount)))
 checksum=hashlib.sha256(json.dumps([loaded,valid,rejected],sort_keys=True).encode()).hexdigest()[:12]
 c.execute('INSERT INTO runs(run_at,loaded,valid,rejected,checksum) VALUES(?,?,?,?,?)',(now,loaded,valid,rejected,checksum))
 c.execute('INSERT INTO audit(event_at,action,detail) VALUES(?,?,?)',(now,'pipeline_run',json.dumps({'loaded':loaded,'valid':valid,'rejected':rejected})))
 c.commit();c.close();return {'loaded':loaded,'valid':valid,'rejected':rejected,'checksum':checksum}
def overview(path=DB):
 c=connect(path); rows=c.execute('SELECT product,COUNT(*) n,ROUND(SUM(reported_amount),2) amount FROM fact_claims GROUP BY product ORDER BY amount DESC').fetchall()
 totals=c.execute('SELECT COUNT(*) n,COALESCE(SUM(reported_amount),0) amount,COUNT(DISTINCT policy_id) policies FROM fact_claims').fetchone()
 rejected=c.execute('SELECT COUNT(*) n FROM quarantine').fetchone()['n'];runs=[dict(r) for r in c.execute('SELECT * FROM runs ORDER BY id DESC LIMIT 8')];c.close()
 return {'totals':dict(totals),'products':[dict(r) for r in rows],'rejected':rejected,'runs':runs}
def claims(product=None,status=None,path=DB):
 c=connect(path);q='SELECT * FROM fact_claims WHERE 1=1';args=[]
 if product:q+=' AND product=?';args.append(product)
 if status:q+=' AND status=?';args.append(status)
 q+=' ORDER BY reported_amount DESC LIMIT 250';data=[dict(r) for r in c.execute(q,args)];c.close();return data
def answer(question,path=DB):
 """Local deterministic retrieval, not an LLM. Return cited rows and an abstention if no evidence."""
 words=set(question.lower().split()); data=claims(path=path)
 product=next((x for x in PRODUCTS if x.lower() in question.lower()),None)
 if product:data=[r for r in data if r['product']==product]
 if 'open' in words:data=[r for r in data if r['status']=='Open']
 if 'settled' in words:data=[r for r in data if r['status']=='Settled']
 if not data:return {'answer':'No matching verified claims found. I cannot answer from available evidence.','evidence':[],'mode':'grounded deterministic retrieval'}
 n=len(data); amount=round(sum(r['reported_amount'] for r in data),2)
 return {'answer':f'{n} matching claims with SEK {amount:,.0f} in reported amounts. These are reported amounts, not paid losses.','evidence':[{'claim_id':r['claim_id'],'product':r['product'],'amount':r['reported_amount'],'status':r['status']} for r in data[:6]],'mode':'grounded deterministic retrieval'}
def audit(path=DB):
 c=connect(path);r=[dict(x) for x in c.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 30')];c.close();return r
