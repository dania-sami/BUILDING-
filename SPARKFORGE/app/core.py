import math
import re
from dataclasses import dataclass

CASES = [
 {'id':'support','name':'Customer support knowledge assistant','industry':'Services','problem':'Support agents spend time searching policy documents and drafting repetitive replies.','hours':160,'hourly_cost':520,'automation':0.35,'setup':95000,'monthly':4500,'risk':2,'readiness':4,'approach':'Grounded RAG assistant with citations and human approval before sending','data':'Approved support articles and policies','success':'Answer acceptance rate, groundedness, handling time','owner':'Customer service lead'},
 {'id':'quality','name':'Engineering quality copilot','industry':'Software','problem':'Developers spend time triaging defects and finding relevant tests.','hours':110,'hourly_cost':680,'automation':0.28,'setup':130000,'monthly':7000,'risk':3,'readiness':3,'approach':'Repository retrieval plus read-only agent tools, with human code review','data':'Code, tests, issue history','success':'Defect triage time, false suggestions, test coverage','owner':'Engineering manager'},
 {'id':'procurement','name':'Supplier document intake','industry':'Manufacturing','problem':'Procurement staff manually extract terms from supplier documents.','hours':130,'hourly_cost':550,'automation':0.45,'setup':110000,'monthly':6000,'risk':3,'readiness':3,'approach':'Document extraction pipeline with schema validation and exception queue','data':'Synthetic supplier contracts and purchase orders','success':'Field-level precision, review rate, processing time','owner':'Procurement lead'},
 {'id':'hr','name':'Internal onboarding assistant','industry':'People operations','problem':'New colleagues struggle to find approved onboarding instructions.','hours':75,'hourly_cost':500,'automation':0.3,'setup':65000,'monthly':2500,'risk':2,'readiness':4,'approach':'Access-controlled RAG assistant with explicit source references','data':'Approved internal onboarding handbook','success':'Helpful answer rate, access violations, time to resolution','owner':'People operations lead'}
]
DOCS = [
 {'id':'K01','title':'Retrieval and citations','text':'A retrieval augmented generation assistant should retrieve authorized documents, cite its supporting passages, and abstain when the evidence does not answer the question.'},
 {'id':'K02','title':'Privacy and access control','text':'Enforce access permissions before retrieval. Do not send confidential client records to an unapproved model provider. Remove personal data from synthetic demonstrations.'},
 {'id':'K03','title':'Human oversight','text':'High impact decisions and customer-facing actions require human approval. Agent tools should use least privilege and allow a safe handoff.'},
 {'id':'K04','title':'Evaluation and release','text':'Test retrieval relevance, citation correctness, refusal behavior, latency, and cost. Regression test each release with a fixed dataset.'},
 {'id':'K05','title':'Engineering productivity','text':'AI coding suggestions require developer review, automated tests, security checks, and measurement against a baseline. Never merge unreviewed generated code.'},
 {'id':'K06','title':'Workshop facilitation','text':'Start with the business workflow and measurable pain point. Identify the data owner, assess feasibility and risk, then agree on a small pilot and acceptance criteria.'},
 {'id':'K07','title':'Agent reliability','text':'Use bounded tool permissions, typed input and output contracts, timeouts, audit logs, and human escalation when confidence or permissions are insufficient.'},
 {'id':'K08','title':'AI operating model','text':'Assign business ownership, technical ownership, evaluation ownership, and an incident response path. Review outcomes after the pilot before scaling.'}
]
EVALS = [
 {'question':'How should a knowledge assistant answer without evidence?','expected':'abstain','topic':'retrieval'},
 {'question':'What protects confidential records during retrieval?','expected':'privacy','topic':'privacy'},
 {'question':'Should an agent approve a high impact decision automatically?','expected':'human','topic':'oversight'},
 {'question':'How should teams check AI coding suggestions?','expected':'tests','topic':'engineering'},
 {'question':'What should be measured before scaling a pilot?','expected':'evaluation','topic':'evaluation'},
 {'question':'How do we start a customer AI workshop?','expected':'workflow','topic':'workshop'},
 {'question':'What controls should an agent tool have?','expected':'permissions','topic':'agent'},
 {'question':'Who owns an AI service after launch?','expected':'ownership','topic':'operating'}
]
KEYWORDS = {'retrieval':'abstain','privacy':'access','oversight':'human','engineering':'tests','evaluation':'regression','workshop':'workflow','agent':'permissions','operating':'ownership'}

def tokenize(s): return set(re.findall(r'[a-z0-9]+',s.lower())) - {'a','the','to','of','and','is','an','in','what','how','should','do','we','for','with'}

def retrieve(question, limit=3):
 q=tokenize(question)
 matches=[]
 for doc in DOCS:
  score=len(q & tokenize(doc['title']+' '+doc['text']))
  if score: matches.append((score,doc))
 matches.sort(key=lambda item:(-item[0],item[1]['id']))
 return [{'id':d['id'],'title':d['title'],'text':d['text'],'score':s} for s,d in matches[:limit]]

def answer(question):
 docs=retrieve(question)
 if not docs:return {'answer':'I cannot answer from the approved knowledge base. Please ask a subject matter expert.','citations':[],'abstained':True,'mode':'extractive demo; no external LLM'}
 return {'answer':docs[0]['text'],'citations':[{'id':d['id'],'title':d['title']} for d in docs],'abstained':False,'mode':'extractive demo; no external LLM'}

def business_case(case, adoption=0.7, volume=1):
 adoption=max(0,min(1,float(adoption)));volume=max(0.1,min(5,float(volume)))
 gross=case['hours']*case['hourly_cost']*case['automation']*adoption*volume
 net=gross-case['monthly'];payback=case['setup']/net if net>0 else None
 return {'gross_monthly_sek':round(gross),'net_monthly_sek':round(net),'annual_net_after_setup_sek':round(net*12-case['setup']),'payback_months':round(payback,1) if payback else None,'assumptions':'Illustrative estimates, not measured benefits. Savings require validation in a pilot.'}

def recommendation(case):
 if case['risk']>=4:return 'Do not automate until controls and business approval are in place.'
 if case['readiness']>=4:return 'Start with a scoped pilot and a fixed evaluation set.'
 return 'Run a data readiness and workflow discovery sprint before building.'

def run_evaluations():
 results=[]
 for e in EVALS:
  response=answer(e['question']);doc_text=' '.join(d['text'] for d in retrieve(e['question']))
  if e['expected']=='abstain': passed='abstain' in doc_text.lower()
  else: passed=KEYWORDS[e['topic']] in doc_text.lower()
  results.append({**e,'passed':passed,'citations':response['citations'],'answer':response['answer']})
 return {'passed':sum(x['passed'] for x in results),'total':len(results),'results':results,'note':'Deterministic retrieval regression checks, not LLM quality certification.'}
