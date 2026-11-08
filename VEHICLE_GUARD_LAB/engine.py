"""Transparent illustrative triage engine. NOT a CVSS implementation."""
import hashlib, json

def priority(case):
    """0-100 composite, explicitly NOT a CVSS or ISO 21434 risk rating."""
    return round(min(100, case['cvss'] * 4.5 + case['exposure'] * 6 + case['safety'] * 4 + case['confidence'] * 2))

def severity(score):
    return 'CRITICAL' if score >= 85 else 'HIGH' if score >= 65 else 'MODERATE' if score >= 45 else 'LOW'

def event_hash(previous_hash, payload):
    canonical=json.dumps(payload,sort_keys=True,separators=(',',':'))
    return hashlib.sha256((previous_hash+'|'+canonical).encode()).hexdigest()

def verify_chain(events):
    prev='GENESIS'
    for e in events:
        payload={k:e[k] for k in ('case_id','event_type','detail','actor','timestamp')}
        if e['previous_hash']!=prev or e['hash']!=event_hash(prev,payload): return False
        prev=e['hash']
    return True
