/* Financial logic: all values are SEK millions. Illustrative simplified valuation, not fund NAV. */
const Engine={
 equity:(c,m=c.multiple,e=c.ebitda,d=c.netDebt)=>e*m-d,
 ev:(c,m=c.multiple,e=c.ebitda)=>e*m,
 margin:c=>c.ebitda/c.revenue*100,
 growth:c=>(c.ebitda/c.priorEbitda-1)*100,
 conversion:c=>c.fcf/c.ebitda*100,
 leverage:c=>c.netDebt/c.ebitda,
 sum:(a,f)=>a.reduce((s,x)=>s+f(x),0),
 fmt:(n,d=1)=>Number(n).toLocaleString('en-SE',{minimumFractionDigits:d,maximumFractionDigits:d}),
 money:n=>'SEK '+Engine.fmt(n)+'m',
 portfolio:cs=>({revenue:Engine.sum(cs,c=>c.revenue),ebitda:Engine.sum(cs,c=>c.ebitda),equity:Engine.sum(cs,c=>Engine.equity(c)),fcf:Engine.sum(cs,c=>c.fcf)}),
 flags:c=>{let a=[];if(Engine.conversion(c)<70)a.push({type:'Cash conversion',severity:'High',detail:'FCF / EBITDA below 70%. Validate working capital, cash adjustments and cash flow bridge.'});if(Engine.leverage(c)>3.5)a.push({type:'Leverage',severity:'High',detail:'Net debt / EBITDA above 3.5x. Review debt covenants and refinancing sensitivity.'});if(c.reportedRevenue!==c.revenue)a.push({type:'Revenue reconciliation',severity:'High',detail:'Reported revenue does not match the underlying synthetic ledger revenue.'});if(c.reportingCoverage<.85)a.push({type:'ESG data coverage',severity:'Medium',detail:'Reporting coverage below 85%. Request complete underlying portfolio company data.'});if(Engine.growth(c)<0)a.push({type:'Earnings trend',severity:'Medium',detail:'EBITDA declined year on year. Review operating drivers and forecasts.'});return a},
 scenario:(c,deltaE,deltaM,deltaD)=>({base:Engine.equity(c),case:Engine.equity(c,c.multiple+deltaM,c.ebitda*(1+deltaE/100),c.netDebt+deltaD)}),
 csv:(rows)=>rows.map(row=>row.map(x=>'"'+String(x??'').replaceAll('"','""')+'"').join(',')).join('\r\n')
};