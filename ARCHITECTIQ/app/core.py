import math,re,hashlib
from collections import Counter
from pathlib import Path
import json
BASE=Path(__file__).resolve().parent.parent
DOCS=json.loads((BASE/'data'/'knowledge.json').read_text())
TOKEN=re.compile(r'[a-zåäö0-9]+',re.I)
STOP={'the','a','an','and','or','of','to','for','in','on','is','are','with','what','how','do','we','our','can','i','it','be','by','from','that','as','at','should','does','about'}
def tokens(s):return [t for t in TOKEN.findall(s.lower()) if t not in STOP]
def retrieve(question,k=3):
 q=Counter(tokens(question)); corpus=[Counter(tokens(d['text']+' '+d['title'])) for d in DOCS]; n=len(corpus)
 df=Counter(t for c in corpus for t in c)
 scores=[]
 for d,c in zip(DOCS,corpus):
  score=sum((1+math.log(1+c[t]))*math.log(1+(n+1)/(df[t]+1))*v for t,v in q.items() if t in c)
  if score:scores.append({**d,'score':round(score,3)})
 return sorted(scores,key=lambda x:-x['score'])[:k]
def answer(question):
 hits=retrieve(question)
 if not hits:return {'status':'abstain','answer':'I could not find supporting evidence in the available knowledge base. Route this question to a subject matter expert.','citations':[],'confidence':0,'policy':'No grounded source found'}
 top=hits[0]['score']; selected=[d for d in hits if d['score']>=top*.32][:2]
 snippets=[re.split(r'(?<=[.!?])\s+',d['text'])[0] for d in selected]
 return {'status':'grounded','answer':' '.join(snippets),'citations':[{'id':d['id'],'title':d['title'],'score':d['score']} for d in selected],'confidence':round(min(.94,top/(top+4)),2),'policy':'Extractive response from synthetic approved documents; no model-generated claims'}
def evaluate():
 cases=json.loads((BASE/'data'/'evals.json').read_text()); results=[]
 for c in cases:
  r=answer(c['question']); passed=r['status']==c['expected_status'] and (not c.get('expected_source') or c['expected_source'] in [x['id'] for x in r['citations']]);results.append({'question':c['question'],'expected':c['expected_status'],'actual':r['status'],'passed':passed,'source':c.get('expected_source')})
 return {'passed':sum(x['passed'] for x in results),'total':len(results),'results':results}
def estimate(requests,avg_input,avg_output,input_rate,output_rate):
 return {'monthly_usd':round(requests*(avg_input*input_rate+avg_output*output_rate)/1_000_000,2),'monthly_tokens':requests*(avg_input+avg_output),'assumptions':'Illustrative token pricing entered by user, not a live provider quote'}
