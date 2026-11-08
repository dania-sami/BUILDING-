'use strict';
const $=id=>document.getElementById(id);let cases=[],selected=null,events=[];
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const api=async(path,opts)=>{let r=await fetch(path,opts);let j=await r.json();if(!r.ok)throw Error(j.error||'Request failed');return j};
const choose=id=>{selected=cases.find(c=>c.id===id);render();location.hash='investigation'};
function render(){const list=cases.filter(c=>(!$('search').value||JSON.stringify(c).toLowerCase().includes($('search').value.toLowerCase()))&&($('filter').value==='ALL'||c.band===$('filter').value));$('metrics').innerHTML=[['ACTIVE CASES',cases.filter(c=>c.status!=='Closed').length],['CRITICAL PRIORITY',cases.filter(c=>c.band==='CRITICAL').length],['OPEN INVESTIGATIONS',cases.filter(c=>c.status==='Investigating').length],['EVIDENCE EVENTS',events.length]].map(([n,v])=>`<div class="metric"><strong>${v}</strong><span>${n}</span></div>`).join('');$('cases').innerHTML=list.map(c=>`<article class="case ${selected?.id===c.id?'selected':''}" data-id="${c.id}" tabindex="0" role="button"><div class="top"><span>${c.id} / ${escapeHTML(c.component)}</span><span class="tag ${c.band}">${c.band}</span></div><h3>${escapeHTML(c.title)}</h3><p>${escapeHTML(c.summary)}</p><div class="bottom"><span>${escapeHTML(c.fleet)}</span><span>PRIORITY ${c.priority}/100 ↗</span></div></article>`).join('')||'<p>No matching cases.</p>';
 document.querySelectorAll('.case').forEach(e=>{e.onclick=()=>choose(e.dataset.id);e.onkeydown=x=>{if(x.key==='Enter')choose(e.dataset.id)}});
 if(!selected)selected=cases[0];if(!selected)return;
 $('caseDetail').innerHTML=`<div class="eyebrow">${selected.id} · ${escapeHTML(selected.status)} · ${escapeHTML(selected.component)}</div><h3>${escapeHTML(selected.title)}</h3><p class="muted">${escapeHTML(selected.summary)}</p><p>Illustrative priority: <strong>${selected.priority}/100</strong> · CVSS input: ${selected.cvss} · Exposure: ${selected.exposure}/5 · Safety context: ${selected.safety}/5 · Evidence confidence: ${selected.confidence}/5</p><p class="micro">Composite priority is a transparent portfolio heuristic, not an official CVSS, ISO 21434 or UNECE R155 risk determination.</p><div class="eyebrow">SIGNALS</div>${selected.signals.map(s=>`<p class="micro">↗ ${escapeHTML(s)}</p>`).join('')}`;
 $('playbook').innerHTML=selected.actions.map((s,i)=>`<label class="check"><input type="checkbox" data-step="${i}"><span>${escapeHTML(s)}</span></label>`).join('');
 $('briefText').textContent=brief();$('events').innerHTML=events.length?events.slice().reverse().map(e=>`<div class="event"><strong>${escapeHTML(e.event_type)}</strong> · ${escapeHTML(e.case_id)} · <span>${escapeHTML(e.actor)}</span><div>${escapeHTML(e.detail)}</div><span>${escapeHTML(e.timestamp)}</span><div><code>SHA-256 ${escapeHTML(e.hash)}</code></div></div>`).join(''):'<p class="muted">No events yet. Record an investigation action to start the evidence chain.</p>';
}
function brief(){let c=selected;if(!c)return 'Select a case';let ce=events.filter(e=>e.case_id===c.id);return `VEHICLE//GUARD · PSIRT CASE BRIEF
${'='.repeat(48)}
Case: ${c.id} | ${c.title}
Component: ${c.component}
Fleet context: ${c.fleet}
Current status: ${c.status}
Illustrative priority: ${c.priority}/100 (${c.band})
CVSS source input: ${c.cvss}

OBSERVATIONS
${c.signals.map(x=>'• '+x).join('\n')}

RECOMMENDED INVESTIGATION STEPS
${c.actions.map(x=>'• '+x).join('\n')}

RECORDED CASE EVENTS (${ce.length})
${ce.map(e=>`${e.timestamp} | ${e.event_type} | ${e.actor}: ${e.detail}`).join('\n')||'No recorded events'}

LIMITATIONS
Synthetic training scenario. No actual vehicle data, exploitation, incident confirmation, or regulatory certification. Safety and containment decisions require authorized specialists.

Generated: ${new Date().toISOString()}`}
async function reload(){try{cases=await api('/api/cases');const ev=await api('/api/evidence');events=ev.events;$('integrity').textContent=ev.verified?'✓ SHA-256 CHAIN VERIFIED':'⚠ CHAIN INTEGRITY FAILED';if(selected)selected=cases.find(c=>c.id===selected.id);render()}catch(e){$('feedback').textContent=e.message}}
$('record').onclick=async()=>{if(!selected)return;const data={case_id:selected.id,event_type:$('eventType').value,detail:$('detail').value,actor:$('actor').value};try{await api('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});$('detail').value='';$('feedback').textContent='✓ Event saved to verified evidence chain';await reload()}catch(e){$('feedback').textContent='⚠ '+e.message}};
$('download').onclick=()=>{const blob=new Blob([brief()],{type:'text/plain'}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=(selected?.id||'case')+'_PSIRT_brief.txt';a.click();URL.revokeObjectURL(u)};
$('refresh').onclick=reload;$('search').oninput=render;$('filter').onchange=render;reload();
