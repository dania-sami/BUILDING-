from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import json, sqlite3, datetime
BASE=Path(__file__).resolve().parents[1]
app=FastAPI(title='DEALROOM | M&A Intelligence Workbench',version='1.0')
app.mount('/static',StaticFiles(directory=BASE/'static'),name='static')
def dataset():return json.loads((BASE/'data'/'deal.json').read_text())
def conn():
 c=sqlite3.connect(BASE/'dealroom.db');c.row_factory=sqlite3.Row;c.execute('CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, finding_id TEXT, status TEXT, owner TEXT, note TEXT, created TEXT)');return c
@app.get('/')
def home():return FileResponse(BASE/'static'/'index.html')
@app.get('/api/deal')
def deal():return dataset()
def analyze(d):
 months=d['months']; revenue=sum(m['revenue'] for m in months);ebitda=sum(m['ebitda'] for m in months)
 customers=d['customers'];total=sum(x['revenue'] for x in customers)
 ar=sum(x['balance'] for x in d['receivables']);overdue=sum(x['balance'] for x in d['receivables'] if x['days_overdue']>60)
 findings=[]
 def add(id,level,title,detail,evidence,action):findings.append(dict(id=id,level=level,title=title,detail=detail,evidence=evidence,action=action))
 top=max(customers,key=lambda x:x['revenue']);share=top['revenue']/total
 if share>.25:add('F01','High','Customer concentration',f"{top['name']} represents {share:.1%} of reported customer revenue.",['customers.csv: top customer revenue','customers.csv: all customer revenue'],'Validate contract duration, churn risk and renewal terms.')
 if overdue/ar>.15:add('F02','High','Overdue receivables',f'{overdue/ar:.1%} of receivables are more than 60 days overdue.',['receivables.csv: balance','receivables.csv: days_overdue'],'Reconcile aged debtors with post-period cash receipts.')
 if d['reported_revenue']!=revenue:add('F03','Medium','Revenue reconciliation gap',f"Management reports {d['reported_revenue']:,.0f} SEK while monthly ledger totals {revenue:,.0f} SEK; variance {d['reported_revenue']-revenue:,.0f} SEK.",['management_pack.pdf: reported revenue','monthly_ledger.csv: monthly revenue'],'Request reconciliation and supporting journal entries.')
 if d['adjustments']:
  unsupported=[x for x in d['adjustments'] if not x['supported']]
  if unsupported:add('F04','High','Unsupported EBITDA add-back',f"{sum(x['amount'] for x in unsupported):,.0f} SEK of proposed adjustments lack supporting evidence.",['ebitda_adjustments.xlsx: supported flag'],'Request invoices, contracts and rationale before accepting add-backs.')
 if min(m['ebitda'] for m in months)<0:add('F05','Medium','Negative monthly EBITDA','At least one month has negative EBITDA.',['monthly_ledger.csv: EBITDA by month'],'Investigate seasonality and recurring cost drivers.')
 return dict(revenue=revenue,ebitda=ebitda,margin=ebitda/revenue,reported_revenue=d['reported_revenue'],receivables=ar,overdue=overdue,concentration=share,adjusted_ebitda=ebitda+sum(x['amount'] for x in d['adjustments'] if x['supported']),findings=findings)
@app.get('/api/analysis')
def analysis():return analyze(dataset())
@app.get('/api/reviews')
def reviews():
 c=conn();rows=[dict(x) for x in c.execute('SELECT * FROM reviews ORDER BY id DESC')];c.close();return rows
class Review(BaseModel):
 finding_id:str;status:str;owner:str;note:str
@app.post('/api/reviews')
def review(r:Review):
 ids={x['id'] for x in analyze(dataset())['findings']}
 if r.finding_id not in ids or r.status not in {'Open','Investigating','Resolved','Escalated'} or not r.owner.strip() or not r.note.strip():raise HTTPException(422,'Valid finding, status, owner and review note required')
 c=conn();c.execute('INSERT INTO reviews(finding_id,status,owner,note,created) VALUES(?,?,?,?,?)',(r.finding_id,r.status,r.owner.strip(),r.note.strip(),datetime.datetime.now(datetime.timezone.utc).isoformat()));c.commit();c.close();return {'saved':True}
@app.get('/api/prompts')
def prompts():return [{'name':'Quality of earnings','prompt':'Review the supplied financial statements for nonrecurring adjustments. Cite every claim and mark unsupported adjustments for human review.'},{'name':'Commercial diligence','prompt':'Summarize customer concentration and contract renewal risks. Use only supplied documents and distinguish facts from assumptions.'},{'name':'Management questions','prompt':'Draft five specific management questions for each unresolved finding, referencing the underlying source and amount.'}]
@app.get('/api/workflow')
def workflow():
 a=analyze(dataset());return {'steps':[{'name':'Ingest synthetic evidence','status':'complete'},{'name':'Reconcile ledger and management pack','status':'complete'},{'name':'Screen concentration and working capital','status':'complete'},{'name':'Flag unsupported EBITDA adjustments','status':'complete'},{'name':'Human validation before client use','status':'required'}],'findings':len(a['findings']),'automated_checks':5}
