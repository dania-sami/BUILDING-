import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from pipeline import distance,validate,CENTERS
class Tests(unittest.TestCase):
 def test_zero_distance(self):self.assertAlmostEqual(distance(59,18,59,18),0)
 def test_distance(self):self.assertTrue(1000<distance(59,18,59.01,18)<1200)
 def test_reject_missing(self):self.assertFalse(validate({}))
 def test_reject_bad_score(self):self.assertFalse(validate(dict(area='Solna',lat='59.3',lon='18',lighting='6',activity='3',maintenance='3',safety='2',time='day',gender_group='man')))
 def test_valid(self):self.assertTrue(validate(dict(area='Solna',lat='59.3',lon='18',lighting='4',activity='3',maintenance='3',safety='2',time='day',gender_group='man')))
if __name__=='__main__':unittest.main()
