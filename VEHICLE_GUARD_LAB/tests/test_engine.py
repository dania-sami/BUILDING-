import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import priority,severity,event_hash,verify_chain
class EngineTests(unittest.TestCase):
 def test_priority_bounds(self):
  self.assertTrue(0<=priority(dict(cvss=9.8,exposure=5,safety=5,confidence=5))<=100)
 def test_severity(self): self.assertEqual(severity(90),'CRITICAL')
 def test_evidence_integrity(self):
  p=dict(case_id='IR-1042',event_type='Finding',detail='test',actor='analyst',timestamp='2026-11-08T00:00:00Z')
  e=dict(p,previous_hash='GENESIS',hash=event_hash('GENESIS',p))
  self.assertTrue(verify_chain([e]));e['detail']='tampered';self.assertFalse(verify_chain([e]))
if __name__=='__main__':unittest.main()
