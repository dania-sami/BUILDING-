import csv,sqlite3,math,statistics,json,argparse,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
FIELDS=['response_id','area','lat','lon','time','lighting','activity','maintenance','safety','gender_group']
CENTERS={'Sodermalm':(59.314,18.072),'Solna':(59.360,18.000),'Kista':(59.403,17.944),'Ostermalm':(59.338,18.087)}
def distance(a,b,c,d):
 r=6371000;p1,p2=math.radians(a),math.radians(c);dp=math.radians(c-a);dl=math.radians(d-b)
 x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
 return 2*r*math.asin(math.sqrt(x))
def validate(row):
 try:
  assert row['area'] in CENTERS
  assert -90<=float(row['lat'])<=90 and -180<=float(row['lon'])<=180
  assert all(1<=int(row[k])<=5 for k in ['lighting','activity','maintenance','safety'])
  assert row['time'] in ('day','evening')
  assert row['gender_group'] in ('woman','man','other','prefer_not_to_say')
  return True
 except (ValueError,KeyError,AssertionError):return False
def run():
 rows=list(csv.DictReader(open(ROOT/'data'/'synthetic_survey.csv',encoding='utf-8')))
 good=[r for r in rows if validate(r)]; bad=[r for r in rows if not validate(r)]
 out=ROOT/'outputs';out.mkdir(exist_ok=True)
 db=sqlite3.connect(out/'urban_safety.sqlite');db.execute('DROP TABLE IF EXISTS survey');db.execute('CREATE TABLE survey (response_id TEXT PRIMARY KEY,area TEXT,lat REAL,lon REAL,time TEXT,lighting INTEGER,activity INTEGER,maintenance INTEGER,safety INTEGER,gender_group TEXT,distance_to_center_m REAL)')
 for r in good:
  lat,lon=CENTERS[r['area']]
  db.execute('INSERT INTO survey VALUES (?,?,?,?,?,?,?,?,?,?,?)',(r['response_id'],r['area'],float(r['lat']),float(r['lon']),r['time'],int(r['lighting']),int(r['activity']),int(r['maintenance']),int(r['safety']),r['gender_group'],round(distance(float(r['lat']),float(r['lon']),lat,lon),1)))
 db.commit();db.close()
 groups={a:[r for r in good if r['area']==a] for a in CENTERS}
 summary=[{'area':a,'n':len(v),'mean_safety':round(statistics.mean(int(x['safety']) for x in v),2) if v else None,'mean_lighting':round(statistics.mean(int(x['lighting']) for x in v),2) if v else None} for a,v in groups.items()]
 (out/'summary.json').write_text(json.dumps({'dataset':'synthetic demonstration only','valid':len(good),'rejected':len(bad),'areas':summary},indent=2))
 with open(out/'validated.csv','w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(good)
 print(f'Validated {len(good)} rows, rejected {len(bad)}; SQLite, CSV and JSON created in outputs/')
if __name__=='__main__':run()
