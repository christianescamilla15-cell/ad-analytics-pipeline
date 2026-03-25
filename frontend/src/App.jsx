import React, { useState, useEffect, useCallback } from 'react'

/* ------------------------------------------------------------------ */
/*  i18n                                                               */
/* ------------------------------------------------------------------ */
const T = {
  en: {
    title: 'Ad Analytics Pipeline',
    subtitle: 'AWS + OCR + Meta Ads + Google Ads + GA4',
    totalSpend: 'Total Ad Spend',
    conversions: 'Total Conversions',
    blendedCpc: 'Blended CPC',
    sessions: 'Website Sessions',
    platformComparison: 'Platform Comparison',
    spendTrend: 'Daily Spend Trend (30 d)',
    campaigns: 'All Campaigns',
    ocrUpload: 'Invoice OCR',
    ocrPlaceholder: 'Paste invoice text here...',
    parse: 'Parse Invoice',
    etlPipeline: 'ETL Pipeline',
    runEtl: 'Run Pipeline',
    anomalies: 'Anomaly Alerts',
    noAnomalies: 'No anomalies detected.',
    campaign: 'Campaign',
    platform: 'Platform',
    status: 'Status',
    spend: 'Spend',
    clicks: 'Clicks',
    ctr: 'CTR',
    cpc: 'CPC',
    convs: 'Convs',
    costConv: 'Cost/Conv',
    demo: 'Demo Mode',
    meta: 'Meta Ads',
    google: 'Google Ads',
  },
  es: {
    title: 'Pipeline de Analytics Publicitario',
    subtitle: 'AWS + OCR + Meta Ads + Google Ads + GA4',
    totalSpend: 'Gasto Total',
    conversions: 'Conversiones Totales',
    blendedCpc: 'CPC Combinado',
    sessions: 'Sesiones Web',
    platformComparison: 'Comparativa de Plataformas',
    spendTrend: 'Tendencia de Gasto Diario (30 d)',
    campaigns: 'Todas las Campanas',
    ocrUpload: 'OCR de Facturas',
    ocrPlaceholder: 'Pega el texto de la factura aqui...',
    parse: 'Analizar Factura',
    etlPipeline: 'Pipeline ETL',
    runEtl: 'Ejecutar Pipeline',
    anomalies: 'Alertas de Anomalias',
    noAnomalies: 'No se detectaron anomalias.',
    campaign: 'Campana',
    platform: 'Plataforma',
    status: 'Estado',
    spend: 'Gasto',
    clicks: 'Clics',
    ctr: 'CTR',
    cpc: 'CPC',
    convs: 'Convs',
    costConv: 'Costo/Conv',
    demo: 'Modo Demo',
    meta: 'Meta Ads',
    google: 'Google Ads',
  },
}

/* ------------------------------------------------------------------ */
/*  Mock Data (embedded — no API calls needed for demo)                */
/* ------------------------------------------------------------------ */
const MOCK = {
  kpis: { total_spend: 41057.00, total_conversions: 1281, blended_cpc: 1.01, website_sessions: 34520 },
  metaCampaigns: [
    { id:'c1', name:'Brand Awareness Q1', platform:'Meta', status:'ACTIVE', spend:3245.50, impressions:245000, clicks:4890, ctr:2.0, cpc:0.66, conversions:89, cost_per_conversion:36.47 },
    { id:'c2', name:'Lead Gen - Personal Injury', platform:'Meta', status:'ACTIVE', spend:7890.25, impressions:189000, clicks:5670, ctr:3.0, cpc:1.39, conversions:234, cost_per_conversion:33.72 },
    { id:'c3', name:'Retargeting Website Visitors', platform:'Meta', status:'ACTIVE', spend:2100.00, impressions:98000, clicks:3920, ctr:4.0, cpc:0.54, conversions:156, cost_per_conversion:13.46 },
    { id:'c4', name:'Video Testimonials', platform:'Meta', status:'PAUSED', spend:1560.00, impressions:167000, clicks:2505, ctr:1.5, cpc:0.62, conversions:45, cost_per_conversion:34.67 },
  ],
  googleCampaigns: [
    { id:'g1', name:'Search - Personal Injury Attorney', platform:'Google', status:'ENABLED', spend:12450.00, impressions:89000, clicks:6230, ctr:7.0, cpc:2.00, conversions:312, cost_per_conversion:39.90 },
    { id:'g2', name:'Display - Brand Remarketing', platform:'Google', status:'ENABLED', spend:4890.50, impressions:456000, clicks:9120, ctr:2.0, cpc:0.54, conversions:178, cost_per_conversion:27.47 },
    { id:'g3', name:'Performance Max - All Channels', platform:'Google', status:'ENABLED', spend:8920.75, impressions:312000, clicks:8424, ctr:2.7, cpc:1.06, conversions:267, cost_per_conversion:33.41 },
  ],
  comparison: [
    { platform:'Meta Ads', spend:14795.75, conversions:524, cpc:0.87, ctr:2.43, cost_per_conversion:28.23 },
    { platform:'Google Ads', spend:26261.25, conversions:757, cpc:1.10, ctr:2.77, cost_per_conversion:34.69 },
  ],
  anomalies: [
    { campaign:'Search - Personal Injury Attorney', platform:'google', metric:'spend', value:12450, z_score:2.31, severity:'warning', message:'Search - Personal Injury Attorney spend ($12,450.00) is 2.3 std devs above average ($5,865.14)' },
  ],
}

// Generate 30-day spend trend
function generateTrend() {
  const data = []; const rng = (s) => { let x=s; return()=>{x=Math.sin(x)*10000;return x-Math.floor(x)} }; const r=rng(42)
  const base = new Date(2024, 2, 2)
  for (let i=0; i<30; i++) { const d=new Date(base); d.setDate(d.getDate()+i); const m=350+r()*300; const g=700+r()*400; data.push({date:d.toISOString().slice(0,10), meta:Math.round(m*100)/100, google:Math.round(g*100)/100, total:Math.round((m+g)*100)/100}) }
  return data
}
const TREND = generateTrend()

/* ------------------------------------------------------------------ */
/*  Styles                                                             */
/* ------------------------------------------------------------------ */
const S = {
  body: { margin:0, fontFamily:"'Segoe UI',system-ui,-apple-system,sans-serif", background:'#0a0e1a', color:'#e2e8f0', minHeight:'100vh' },
  header: { display:'flex', justifyContent:'space-between', alignItems:'center', padding:'20px 32px', borderBottom:'1px solid #1e293b' },
  h1: { fontSize:'1.5rem', fontWeight:700, color:'#f1f5f9', margin:0 },
  sub: { fontSize:'.85rem', color:'#64748b', marginTop:2 },
  langBtn: { background:'transparent', border:'1px solid #334155', color:'#94a3b8', padding:'6px 14px', borderRadius:6, cursor:'pointer', fontSize:'.8rem' },
  badge: { display:'inline-block', padding:'2px 10px', borderRadius:12, fontSize:'.7rem', fontWeight:600 },
  grid: { display:'grid', gap:20, padding:'24px 32px' },
  kpiRow: { display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(200px,1fr))', gap:16 },
  card: { background:'#111827', border:'1px solid #1e293b', borderRadius:12, padding:20 },
  kpiLabel: { fontSize:'.75rem', color:'#64748b', textTransform:'uppercase', letterSpacing:1 },
  kpiValue: { fontSize:'1.8rem', fontWeight:700, color:'#f1f5f9', marginTop:4 },
  sectionTitle: { fontSize:'1.1rem', fontWeight:600, color:'#f1f5f9', marginBottom:12 },
  table: { width:'100%', borderCollapse:'collapse', fontSize:'.82rem' },
  th: { textAlign:'left', padding:'10px 12px', borderBottom:'1px solid #1e293b', color:'#64748b', fontWeight:600, fontSize:'.72rem', textTransform:'uppercase', letterSpacing:.5 },
  td: { padding:'10px 12px', borderBottom:'1px solid #1e293b0a' },
  btn: { padding:'10px 20px', borderRadius:8, border:'none', fontWeight:600, cursor:'pointer', fontSize:'.85rem' },
  textarea: { width:'100%', minHeight:120, background:'#1e293b', border:'1px solid #334155', borderRadius:8, color:'#e2e8f0', padding:12, fontFamily:'monospace', fontSize:'.82rem', resize:'vertical', boxSizing:'border-box' },
  alert: { padding:'12px 16px', borderRadius:8, marginBottom:8, fontSize:'.82rem' },
}

/* ------------------------------------------------------------------ */
/*  Components                                                         */
/* ------------------------------------------------------------------ */
function KPICard({ label, value, prefix='', suffix='' }) {
  return (
    <div style={S.card}>
      <div style={S.kpiLabel}>{label}</div>
      <div style={S.kpiValue}>{prefix}{typeof value==='number'?value.toLocaleString():value}{suffix}</div>
    </div>
  )
}

function StatusBadge({ status }) {
  const colors = { ACTIVE:'#22c55e', ENABLED:'#22c55e', PAUSED:'#f59e0b', REMOVED:'#ef4444' }
  const bg = (colors[status]||'#64748b')+'22'
  const fg = colors[status]||'#64748b'
  return <span style={{...S.badge, background:bg, color:fg}}>{status}</span>
}

function BarChart({ data, t }) {
  const maxSpend = Math.max(...data.map(d=>d.spend))
  return (
    <div style={{display:'flex',flexDirection:'column',gap:12}}>
      {data.map(d=>(
        <div key={d.platform} style={{display:'flex',alignItems:'center',gap:12}}>
          <div style={{width:100,fontSize:'.82rem',color:'#94a3b8',textAlign:'right'}}>{d.platform}</div>
          <div style={{flex:1,background:'#1e293b',borderRadius:6,height:28,overflow:'hidden',position:'relative'}}>
            <div style={{width:`${(d.spend/maxSpend*100)}%`,height:'100%',background:d.platform.includes('Meta')?'#3b82f6':'#10b981',borderRadius:6,transition:'width .5s'}} />
            <span style={{position:'absolute',right:8,top:4,fontSize:'.75rem',color:'#e2e8f0'}}>${d.spend.toLocaleString()} | {d.conversions} convs</span>
          </div>
        </div>
      ))}
    </div>
  )
}

function SpendTrendChart({ data }) {
  if(!data.length) return null
  const W=800, H=200, P=40
  const vals = data.map(d=>d.total)
  const max = Math.max(...vals)*1.1
  const min = Math.min(...vals)*0.9
  const range = max-min||1
  const xStep = (W-P*2)/(data.length-1)
  const toY = v => H-P-(v-min)/range*(H-P*2)
  const metaPath = data.map((d,i)=>`${i===0?'M':'L'}${P+i*xStep},${toY(d.meta)}`).join(' ')
  const googlePath = data.map((d,i)=>`${i===0?'M':'L'}${P+i*xStep},${toY(d.google)}`).join(' ')
  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{width:'100%',height:'auto'}}>
      <line x1={P} y1={H-P} x2={W-P} y2={H-P} stroke="#1e293b" />
      <line x1={P} y1={P} x2={P} y2={H-P} stroke="#1e293b" />
      <path d={metaPath} fill="none" stroke="#3b82f6" strokeWidth="2" />
      <path d={googlePath} fill="none" stroke="#10b981" strokeWidth="2" />
      <text x={W-P-60} y={P+10} fill="#3b82f6" fontSize="11">Meta</text>
      <text x={W-P-60} y={P+24} fill="#10b981" fontSize="11">Google</text>
      {[0,1,2,3,4].map(i=>{const v=min+(range/4)*i;return <text key={i} x={P-6} y={toY(v)+4} fill="#64748b" fontSize="9" textAnchor="end">${Math.round(v)}</text>})}
      {data.filter((_,i)=>i%7===0).map((d,i,a)=><text key={i} x={P+data.indexOf(d)*xStep} y={H-P+14} fill="#64748b" fontSize="9" textAnchor="middle">{d.date.slice(5)}</text>)}
    </svg>
  )
}

/* ------------------------------------------------------------------ */
/*  App                                                                */
/* ------------------------------------------------------------------ */
export default function App() {
  const [lang, setLang] = useState(()=>navigator.language.startsWith('es')?'es':'en')
  const t = T[lang]

  const [invoiceText, setInvoiceText] = useState('')
  const [parsed, setParsed] = useState(null)
  const [etlStatus, setEtlStatus] = useState('idle')
  const [etlResult, setEtlResult] = useState(null)

  const allCampaigns = [...MOCK.metaCampaigns, ...MOCK.googleCampaigns]

  const handleParse = useCallback(() => {
    if(!invoiceText.trim()) return
    // Client-side regex parse (mirrors backend InvoiceParser)
    const inv = invoiceText.match(/(?:Invoice|Inv|#)\s*[:#]?\s*(\w+[-/]?\w+)/i)
    const dt = invoiceText.match(/(?:Date|Fecha)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})/i)
    const tot = invoiceText.match(/(?:Total|Amount Due|Grand Total)[:\s]*\$?([\d,]+\.?\d*)/i)
    const sub = invoiceText.match(/(?:Subtotal|Sub-total)[:\s]*\$?([\d,]+\.?\d*)/i)
    const tax = invoiceText.match(/(?:Tax|IVA|VAT)[:\s]*\$?([\d,]+\.?\d*)/i)
    const vendor = invoiceText.match(/(?:From|Bill From|Vendor)[:\s]*([A-Za-z\s&.,]+)/i)
    const items = [...invoiceText.matchAll(/(\d+)\s+(.+?)\s+\$?([\d,]+\.?\d*)/g)]
    setParsed({
      invoice_number: inv?inv[1]:'',
      date: dt?dt[1]:'',
      vendor_name: vendor?vendor[1].trim():'',
      subtotal: sub?parseFloat(sub[1].replace(/,/g,'')):0,
      tax: tax?parseFloat(tax[1].replace(/,/g,'')):0,
      total: tot?parseFloat(tot[1].replace(/,/g,'')):0,
      line_items: items.map(m=>({qty:parseInt(m[1]),description:m[2].trim(),amount:parseFloat(m[3].replace(/,/g,''))})),
    })
  }, [invoiceText])

  const handleETL = useCallback(() => {
    setEtlStatus('running')
    setTimeout(()=>{
      setEtlResult({status:'completed',records:7,sources:['meta','google','ga4'],elapsed:'0.042s'})
      setEtlStatus('completed')
    }, 1500)
  }, [])

  return (
    <div style={S.body}>
      {/* Header */}
      <header style={S.header}>
        <div>
          <h1 style={S.h1}>{t.title}</h1>
          <div style={S.sub}>{t.subtitle}</div>
        </div>
        <div style={{display:'flex',gap:10,alignItems:'center'}}>
          <span style={{...S.badge,background:'#22c55e22',color:'#22c55e'}}>{t.demo}</span>
          <button style={S.langBtn} onClick={()=>setLang(l=>l==='en'?'es':'en')}>{lang==='en'?'ES':'EN'}</button>
        </div>
      </header>

      <div style={{...S.grid,gap:24}}>
        {/* KPIs */}
        <div style={S.kpiRow}>
          <KPICard label={t.totalSpend} value={MOCK.kpis.total_spend} prefix="$" />
          <KPICard label={t.conversions} value={MOCK.kpis.total_conversions} />
          <KPICard label={t.blendedCpc} value={MOCK.kpis.blended_cpc} prefix="$" />
          <KPICard label={t.sessions} value={MOCK.kpis.website_sessions} />
        </div>

        {/* Charts row */}
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:20}}>
          <div style={S.card}>
            <div style={S.sectionTitle}>{t.platformComparison}</div>
            <BarChart data={MOCK.comparison} t={t} />
          </div>
          <div style={S.card}>
            <div style={S.sectionTitle}>{t.spendTrend}</div>
            <SpendTrendChart data={TREND} />
          </div>
        </div>

        {/* Campaign table */}
        <div style={S.card}>
          <div style={S.sectionTitle}>{t.campaigns}</div>
          <div style={{overflowX:'auto'}}>
            <table style={S.table}>
              <thead>
                <tr>
                  {[t.campaign,t.platform,t.status,t.spend,t.clicks,t.ctr,t.cpc,t.convs,t.costConv].map(h=>
                    <th key={h} style={S.th}>{h}</th>
                  )}
                </tr>
              </thead>
              <tbody>
                {allCampaigns.sort((a,b)=>b.spend-a.spend).map(c=>(
                  <tr key={c.id} style={{transition:'background .2s'}}
                      onMouseOver={e=>e.currentTarget.style.background='#1e293b44'}
                      onMouseOut={e=>e.currentTarget.style.background='transparent'}>
                    <td style={S.td}>{c.name}</td>
                    <td style={S.td}><span style={{color:c.platform==='Meta'?'#3b82f6':'#10b981'}}>{c.platform}</span></td>
                    <td style={S.td}><StatusBadge status={c.status} /></td>
                    <td style={S.td}>${c.spend.toLocaleString()}</td>
                    <td style={S.td}>{c.clicks.toLocaleString()}</td>
                    <td style={S.td}>{c.ctr}%</td>
                    <td style={S.td}>${c.cpc}</td>
                    <td style={S.td}>{c.conversions}</td>
                    <td style={S.td}>${c.cost_per_conversion}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Bottom row: OCR + ETL + Anomalies */}
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:20}}>
          {/* OCR */}
          <div style={S.card}>
            <div style={S.sectionTitle}>{t.ocrUpload}</div>
            <textarea style={S.textarea} placeholder={t.ocrPlaceholder} value={invoiceText} onChange={e=>setInvoiceText(e.target.value)} />
            <button style={{...S.btn,background:'#3b82f6',color:'#fff',marginTop:10,width:'100%'}} onClick={handleParse}>{t.parse}</button>
            {parsed && (
              <div style={{marginTop:12,fontSize:'.8rem',background:'#1e293b',padding:12,borderRadius:8}}>
                <div><b>Invoice:</b> {parsed.invoice_number}</div>
                <div><b>Date:</b> {parsed.date}</div>
                <div><b>Vendor:</b> {parsed.vendor_name}</div>
                <div><b>Subtotal:</b> ${parsed.subtotal.toLocaleString()}</div>
                <div><b>Tax:</b> ${parsed.tax.toLocaleString()}</div>
                <div><b>Total:</b> ${parsed.total.toLocaleString()}</div>
                {parsed.line_items.length>0 && (
                  <div style={{marginTop:8}}>
                    <b>Items:</b>
                    {parsed.line_items.map((it,i)=><div key={i} style={{paddingLeft:8}}>{it.qty}x {it.description} - ${it.amount.toLocaleString()}</div>)}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* ETL */}
          <div style={S.card}>
            <div style={S.sectionTitle}>{t.etlPipeline}</div>
            <div style={{display:'flex',flexDirection:'column',gap:12,alignItems:'center',paddingTop:20}}>
              <div style={{display:'flex',gap:8,alignItems:'center'}}>
                {['Extract','Transform','Load'].map((step,i)=>(
                  <React.Fragment key={step}>
                    <div style={{
                      padding:'8px 16px',borderRadius:8,fontSize:'.8rem',fontWeight:600,
                      background: etlStatus==='running'?'#3b82f622':'#1e293b',
                      color: etlStatus==='completed'?'#22c55e': etlStatus==='running'?'#3b82f6':'#64748b',
                      border:`1px solid ${etlStatus==='completed'?'#22c55e44':'#334155'}`,
                      animation: etlStatus==='running'?'pulse 1s infinite':undefined,
                    }}>{step}</div>
                    {i<2 && <span style={{color:'#64748b'}}>→</span>}
                  </React.Fragment>
                ))}
              </div>
              <button style={{...S.btn,background:etlStatus==='running'?'#334155':'#8b5cf6',color:'#fff',marginTop:12}} onClick={handleETL} disabled={etlStatus==='running'}>
                {etlStatus==='running'?'Running...':t.runEtl}
              </button>
              {etlResult && (
                <div style={{fontSize:'.8rem',color:'#22c55e',textAlign:'center',marginTop:8}}>
                  Status: {etlResult.status} | Records: {etlResult.records} | Time: {etlResult.elapsed}
                </div>
              )}
            </div>
          </div>

          {/* Anomalies */}
          <div style={S.card}>
            <div style={S.sectionTitle}>{t.anomalies}</div>
            {MOCK.anomalies.length===0 ? (
              <div style={{color:'#64748b',fontSize:'.85rem'}}>{t.noAnomalies}</div>
            ) : (
              MOCK.anomalies.map((a,i)=>(
                <div key={i} style={{...S.alert,background:a.severity==='critical'?'#ef444422':'#f59e0b22',borderLeft:`3px solid ${a.severity==='critical'?'#ef4444':'#f59e0b'}`}}>
                  <div style={{fontWeight:600,marginBottom:4}}>{a.campaign} <span style={{color:'#64748b',fontWeight:400}}>({a.platform})</span></div>
                  <div style={{color:'#94a3b8'}}>{a.message}</div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Footer */}
        <div style={{textAlign:'center',padding:'12px 0',fontSize:'.75rem',color:'#475569'}}>
          Ad Analytics Pipeline v1.0.0 &mdash; Demo Mode &mdash; AWS + OCR + Marketing APIs
        </div>
      </div>

      <style>{`@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}`}</style>
    </div>
  )
}
