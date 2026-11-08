import sqlite3,hashlib,json,csv,datetime,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'data'/'vault360.sqlite'
SOURCES=ROOT/'data'/'source_transactions.csv'
def hk(*parts): return hashlib.sha256('|'.join(str(x).strip().upper() for x in parts).encode()).hexdigest()[:24]
def setup(conn):
 conn.executescript('''PRAGMA foreign_keys=ON;
 CREATE TABLE IF NOT EXISTS hub_customer(customer_hk TEXT PRIMARY KEY,customer_id TEXT NOT NULL,load_dts TEXT NOT NULL,record_source TEXT NOT NULL);
 CREATE TABLE IF NOT EXISTS hub_account(account_hk TEXT PRIMARY KEY,account_id TEXT NOT NULL,load_dts TEXT NOT NULL,record_source TEXT NOT NULL);
 CREATE TABLE IF NOT EXISTS hub_transaction(transaction_hk TEXT PRIMARY KEY,transaction_id TEXT NOT NULL,load_dts TEXT NOT NULL,record_source TEXT NOT NULL);
 CREATE TABLE IF NOT EXISTS link_account_customer(link_hk TEXT PRIMARY KEY,account_hk TEXT NOT NULL,customer_hk TEXT NOT NULL,load_dts TEXT NOT NULL,record_source TEXT NOT NULL);
 CREATE TABLE IF NOT EXISTS link_transaction_account(link_hk TEXT PRIMARY KEY,transaction_hk TEXT NOT NULL,account_hk TEXT NOT NULL,load_dts TEXT NOT NULL,record_source TEXT NOT NULL);
 CREATE TABLE IF NOT EXISTS sat_transaction_detail(transaction_hk TEXT NOT NULL,load_dts TEXT NOT NULL,hashdiff TEXT NOT NULL,amount REAL NOT NULL,currency TEXT NOT NULL,booked_at TEXT NOT NULL,record_source TEXT NOT NULL,PRIMARY KEY(transaction_hk,load_dts));
 CREATE TABLE IF NOT EXISTS ingestion_audit(batch_id TEXT PRIMARY KEY,loaded_at TEXT,accepted INTEGER,rejected INTEGER,source_file TEXT,source_sha256 TEXT);
 CREATE TABLE IF NOT EXISTS quarantine(batch_id TEXT,source_row INTEGER,reason TEXT,payload TEXT,PRIMARY KEY(batch_id,source_row));
 CREATE TABLE IF NOT EXISTS lineage(asset TEXT PRIMARY KEY,upstream TEXT,transformation TEXT,owner TEXT);
 ''')

def generate():
 import random
 random.seed(360)
 SOURCES.parent.mkdir(parents=True,exist_ok=True)
 with SOURCES.open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['transaction_id','account_id','customer_id','amount','currency','booked_at','record_source'])
  for i in range(1,501):
   w.writerow([f'TX{i:05}',f'AC{(i%55)+1:03}',f'C{(i%37)+1:03}',round(random.uniform(-3000,12000),2),'SEK',(datetime.date(2026,1,1)+datetime.timedelta(days=i%280)).isoformat(),'core_banking'])
  w.writerow(['TX_BAD','AC009','C002','not_a_number','SEK','2026-06-01','core_banking'])
  w.writerow(['TX_BAD2','','C003','100','SEK','2026-06-02','core_banking'])

def ingest(path=SOURCES,db=DB):
 path=Path(path);db=Path(db);db.parent.mkdir(parents=True,exist_ok=True)
 digest=hashlib.sha256(path.read_bytes()).hexdigest();batch=digest[:16]
 conn=sqlite3.connect(db);setup(conn)
 if conn.execute('SELECT 1 FROM ingestion_audit WHERE batch_id=?',(batch,)).fetchone():
  conn.close();return {'batch':batch,'status':'already loaded'}
 accepted=rejected=0;now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with path.open(newline='') as f:
  for n,row in enumerate(csv.DictReader(f),2):
   try:
    if not all(row.get(k,'').strip() for k in ('transaction_id','account_id','customer_id','currency','booked_at','record_source')):raise ValueError('missing required field')
    amt=float(row['amount']);datetime.date.fromisoformat(row['booked_at'])
    if not -1e9<amt<1e9:raise ValueError('amount out of allowed range')
    if row['currency']!='SEK':raise ValueError('unsupported currency')
    c=hk('CUSTOMER',row['customer_id']);a=hk('ACCOUNT',row['account_id']);t=hk('TRANSACTION',row['transaction_id']);source=row['record_source']
    conn.execute('INSERT OR IGNORE INTO hub_customer VALUES(?,?,?,?)',(c,row['customer_id'],now,source))
    conn.execute('INSERT OR IGNORE INTO hub_account VALUES(?,?,?,?)',(a,row['account_id'],now,source))
    conn.execute('INSERT OR IGNORE INTO hub_transaction VALUES(?,?,?,?)',(t,row['transaction_id'],now,source))
    conn.execute('INSERT OR IGNORE INTO link_account_customer VALUES(?,?,?,?,?)',(hk('AC',a,c),a,c,now,source))
    conn.execute('INSERT OR IGNORE INTO link_transaction_account VALUES(?,?,?,?,?)',(hk('TA',t,a),t,a,now,source))
    diff=hk(amt,row['currency'],row['booked_at'])
    last=conn.execute('SELECT hashdiff FROM sat_transaction_detail WHERE transaction_hk=? ORDER BY load_dts DESC LIMIT 1',(t,)).fetchone()
    if not last or last[0]!=diff:
     conn.execute('INSERT INTO sat_transaction_detail VALUES(?,?,?,?,?,?,?)',(t,now,diff,amt,row['currency'],row['booked_at'],source))
    accepted+=1
   except (ValueError,TypeError) as e:
    conn.execute('INSERT INTO quarantine VALUES(?,?,?,?)',(batch,n,str(e),json.dumps(row)));rejected+=1
 conn.execute('INSERT INTO ingestion_audit VALUES(?,?,?,?,?,?)',(batch,now,accepted,rejected,path.name,digest))
 for asset,upstream,transform,owner in [('hub_transaction','source_transactions.csv','SHA256 business key','Data Engineering'),('sat_transaction_detail','hub_transaction + source_transactions.csv','hashdiff change capture','Finance Data'),('mart_daily_exposure','sat_transaction_detail','latest version aggregation','Finance & Risk')]:
  conn.execute('INSERT OR REPLACE INTO lineage VALUES(?,?,?,?)',(asset,upstream,transform,owner))
 conn.commit();conn.close();return {'batch':batch,'accepted':accepted,'rejected':rejected}

def report(db=DB):
 conn=sqlite3.connect(db);conn.row_factory=sqlite3.Row
 query='''WITH latest AS (SELECT *,ROW_NUMBER() OVER(PARTITION BY transaction_hk ORDER BY load_dts DESC) rn FROM sat_transaction_detail) SELECT substr(booked_at,1,7) month,COUNT(*) transactions,ROUND(SUM(amount),2) net_amount FROM latest WHERE rn=1 GROUP BY 1 ORDER BY 1'''
 data=[dict(x) for x in conn.execute(query)]
 quality={'hubs':conn.execute('SELECT COUNT(*) FROM hub_transaction').fetchone()[0],'satellite_versions':conn.execute('SELECT COUNT(*) FROM sat_transaction_detail').fetchone()[0],'quarantined':conn.execute('SELECT COUNT(*) FROM quarantine').fetchone()[0],'batches':conn.execute('SELECT COUNT(*) FROM ingestion_audit').fetchone()[0]}
 lineage=[dict(x) for x in conn.execute('SELECT * FROM lineage')];conn.close();return {'monthly':data,'quality':quality,'lineage':lineage}
if __name__=='__main__':
 generate() if not SOURCES.exists() else None
 print(json.dumps(ingest(),indent=2));print(json.dumps(report(),indent=2))
