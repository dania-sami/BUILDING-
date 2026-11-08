import sys,tempfile,unittest,csv
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'app'))
from pipeline import hk,ingest,report
class PipelineTests(unittest.TestCase):
 def test_deterministic_hash(self):self.assertEqual(hk(' a '),hk('A'))
 def test_pipeline_and_idempotency(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'source.csv';db=Path(d)/'test.db'
   with p.open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['transaction_id','account_id','customer_id','amount','currency','booked_at','record_source']);w.writerow(['T1','A1','C1','10','SEK','2026-01-01','test']);w.writerow(['T2','A2','C2','bad','SEK','2026-01-02','test'])
   self.assertEqual(ingest(p,db)['accepted'],1)
   self.assertEqual(ingest(p,db)['status'],'already loaded')
   self.assertEqual(report(db)['quality']['quarantined'],1)
   self.assertEqual(report(db)['quality']['hubs'],1)
if __name__=='__main__':unittest.main()
