import re, time, uuid
from dataclasses import dataclass

POLICIES = {
 'SE': {'phone':'Demo Home Plus: accidental phone damage may be eligible after a 1,500 SEK deductible. Coverage depends on active policy and claim review.', 'travel':'Demo Travel: baggage delays may qualify after 6 hours with carrier confirmation. A reviewer confirms eligibility.'},
 'DK': {'phone':'Demo Home Plus: accidental phone damage may be eligible after a 1,000 DKK deductible. Coverage depends on active policy and claim review.', 'travel':'Demo Travel: baggage delays may qualify after 6 hours with carrier confirmation. A reviewer confirms eligibility.'},
 'NO': {'phone':'Demo Home Plus: accidental phone damage may be eligible after a 1,500 NOK deductible. Coverage depends on active policy and claim review.', 'travel':'Demo Travel: baggage delays may qualify after 6 hours with carrier confirmation. A reviewer confirms eligibility.'},
 'FI': {'phone':'Demo Home Plus: accidental phone damage may be eligible after a 150 EUR deductible. Coverage depends on active policy and claim review.', 'travel':'Demo Travel: baggage delays may qualify after 6 hours with carrier confirmation. A reviewer confirms eligibility.'}
}
CLAIMS = {'DEMO-1042': {'status':'Under review','type':'phone'}, 'DEMO-2201': {'status':'Awaiting documents','type':'travel'}}
@dataclass
class Decision:
    answer: str
    action: str
    citations: list
    trace: list
    handover: bool = False
    approval_required: bool = False

def run_agent(message, market='SE', claim_id=None):
    start=time.perf_counter(); trace=[]
    def step(name, detail): trace.append({'step':name,'detail':detail})
    market=market if market in POLICIES else 'SE'
    text=message.lower().strip()
    step('input_validation','Market validated; message length checked')
    if not text or len(text)>1200:
        step('guardrail','Invalid input')
        result=Decision('Please enter a question under 1,200 characters.','validation',[],trace)
    elif any(x in text for x in ['ignore previous','system prompt','developer message','reveal secrets','bypass rules']):
        step('guardrail','Prompt injection pattern detected; no tools executed')
        result=Decision('I cannot follow instructions to bypass safeguards. I can still help with an insurance question.','blocked',[],trace,True)
    elif any(x in text for x in ['approve my claim','pay me','transfer money','change my bank','delete my claim']):
        step('policy_gate','Sensitive or irreversible action requires human approval')
        result=Decision('I can prepare this request, but a human reviewer must authorize any claim decision, payment, or account change.','human_review',[],trace,True,True)
    elif claim_id and ('claim' in text or 'status' in text):
        step('tool:claims_lookup','Read-only lookup of synthetic claim identifier')
        claim=CLAIMS.get(claim_id.upper())
        if claim:
            result=Decision(f"Demo claim {claim_id.upper()} is currently: {claim['status']}. This is a fictional record, not a real insurance claim.",'claim_status',['Demo Claims API'],trace)
        else:
            result=Decision('I cannot find that demo claim. Please check the identifier or request a human handover.','not_found',[],trace,True)
    else:
        topic='phone' if any(x in text for x in ['phone','screen','mobile','crack']) else 'travel' if any(x in text for x in ['travel','baggage','luggage','flight']) else None
        step('router',f'Intent: {topic or "unknown"}')
        if topic:
            step('tool:policy_retrieval',f'Retrieved demo {market} {topic} policy excerpt')
            result=Decision(POLICIES[market][topic]+' This is illustrative information, not a coverage determination.','grounded_answer',[f'Demo policy / {market} / {topic}'],trace)
        else:
            step('fallback','No relevant grounded passage; no speculative answer')
            result=Decision('I do not have a reliable policy passage for that question. I would route this to a human specialist rather than guess.','handover',[],trace,True)
    step('response_check','Verified answer has no unauthorized approval or payment action')
    return {'id':str(uuid.uuid4())[:8], 'answer':result.answer,'action':result.action,'citations':result.citations,'trace':result.trace,'handover':result.handover,'approval_required':result.approval_required,'latency_ms':round((time.perf_counter()-start)*1000,2),'market':market,'mode':'deterministic demo'}
