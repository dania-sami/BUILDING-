import os,tempfile
from app import core

def setup_function():
 fd,path=tempfile.mkstemp(suffix='.db');os.close(fd);core.DB=__import__('pathlib').Path(path);core.init()
def test_seed():assert len(core.allreq())==6
def test_conflicts():assert len(core.quality()['unresolved_conflicts'])==2
def test_resolve():
 core.resolve('C01','B','Dania','Agreed on risk based access for different services')
 assert core.allreq()[1]['status']=='Approved'
 assert 'C01' not in core.quality()['unresolved_conflicts']
def test_impact():assert 'R06' in [r['id'] for r in core.impact('R01')['downstream']]
def test_invalid():
 try:core.resolve('C01','X','Dania','Detailed decision rationale')
 except ValueError:return
 assert False
def test_report():assert 'Requirements review' in core.report()
