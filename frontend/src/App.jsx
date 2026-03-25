import React, { useState, useEffect, useCallback, useRef } from 'react'

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
/*  Tour Steps Config                                                  */
/* ------------------------------------------------------------------ */
const TOUR_STEPS = [
  {
    target: 'welcome',
    type: 'modal',
    title: { en: 'Ad Analytics Pipeline', es: 'Pipeline de Analytics Publicitario' },
    text: {
      en: 'This platform unifies your advertising data from Meta Ads, Google Ads, and Google Analytics into a single dashboard. It automatically detects spending anomalies, parses invoices with OCR, and runs ETL pipelines to keep your data fresh.\n\nLet me give you a guided tour!',
      es: 'Esta plataforma unifica tus datos publicitarios de Meta Ads, Google Ads y Google Analytics en un solo dashboard. Detecta anomalias de gasto automaticamente, parsea facturas con OCR, y ejecuta pipelines ETL para mantener tus datos actualizados.\n\n¡Dejame darte un tour guiado!'
    },
    btnText: { en: 'Start Tour →', es: 'Iniciar Tour →' },
    position: 'center',
  },
  {
    target: 'kpi-section',
    type: 'tooltip',
    title: { en: 'Key Performance Indicators', es: 'Indicadores Clave' },
    text: {
      en: 'These 4 cards show your unified metrics across all platforms: total ad spend, conversions, blended CPC, and website sessions from GA4.',
      es: 'Estas 4 tarjetas muestran tus metricas unificadas de todas las plataformas: gasto total, conversiones, CPC combinado, y sesiones web de GA4.'
    },
    btnText: { en: 'Next →', es: 'Siguiente →' },
    position: 'bottom',
  },
  {
    target: 'campaigns-section',
    type: 'tooltip',
    title: { en: 'Unified Campaign Table', es: 'Tabla Unificada de Campanas' },
    text: {
      en: 'All campaigns from Meta and Google are shown together. You can compare spend, CTR, CPC, and conversions across platforms in one view.',
      es: 'Todas las campanas de Meta y Google se muestran juntas. Puedes comparar gasto, CTR, CPC y conversiones entre plataformas en una sola vista.'
    },
    btnText: { en: 'Next →', es: 'Siguiente →' },
    position: 'top',
  },
  {
    target: 'ocr-section',
    type: 'action',
    title: { en: 'OCR Invoice Parser', es: 'Parser OCR de Facturas' },
    text: {
      en: 'The OCR engine extracts line items, vendor info, and totals from advertising invoices automatically. Click the button below to try it with a sample invoice!',
      es: 'El motor OCR extrae lineas, info del proveedor y totales de facturas publicitarias automaticamente. ¡Haz clic en el boton de abajo para probarlo con una factura de ejemplo!'
    },
    btnText: { en: 'Try OCR →', es: 'Probar OCR →' },
    autoAction: 'parse',
    position: 'top',
  },
  {
    target: 'etl-section',
    type: 'action',
    title: { en: 'ETL Pipeline', es: 'Pipeline ETL' },
    text: {
      en: 'The ETL pipeline extracts data from Meta, Google, and GA4, transforms it into a unified format, and loads it into the analytics engine. Click below to run it!',
      es: 'El pipeline ETL extrae datos de Meta, Google y GA4, los transforma a un formato unificado, y los carga en el motor de analitica. ¡Haz clic abajo para ejecutarlo!'
    },
    btnText: { en: 'Run Pipeline →', es: 'Ejecutar Pipeline →' },
    autoAction: 'etl',
    position: 'top',
  },
  {
    target: 'anomalies-section',
    type: 'tooltip',
    title: { en: 'Anomaly Detection', es: 'Deteccion de Anomalias' },
    text: {
      en: 'Campaigns with unusual spending patterns are flagged automatically using z-score statistical analysis. Any campaign spending more than 2 standard deviations from the mean gets an alert.',
      es: 'Las campanas con patrones de gasto inusuales se marcan automaticamente usando analisis estadistico z-score. Cualquier campana que gaste mas de 2 desviaciones estandar del promedio recibe una alerta.'
    },
    btnText: { en: 'Finish Tour ✓', es: 'Finalizar Tour ✓' },
    position: 'top',
  },
]

const SAMPLE_INVOICE = `Invoice #INV-2024-0381
Date: 03/15/2024
From: Meta Platforms Inc.

2 Brand Awareness Campaign $3,245.50
1 Lead Generation Campaign $7,890.25
1 Retargeting Campaign $2,100.00

Subtotal: $13,235.75
Tax: $1,058.86
Total: $14,294.61`

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
/*  TourOverlay Component                                              */
/* ------------------------------------------------------------------ */
function TourOverlay({ stepConfig, step, totalSteps, onNext, onSkip, lang }) {
  const [tooltipStyle, setTooltipStyle] = useState({})
  const [highlightStyle, setHighlightStyle] = useState({})
  const [arrowStyle, setArrowStyle] = useState({})

  const { type, target, title, text, btnText, position } = stepConfig

  useEffect(() => {
    if (type === 'modal') return // modal doesn't need positioning

    const el = document.querySelector(`[data-tour="${target}"]`)
    if (!el) return

    const rect = el.getBoundingClientRect()
    const pad = 8

    setHighlightStyle({
      position: 'fixed',
      top: rect.top - pad,
      left: rect.left - pad,
      width: rect.width + pad * 2,
      height: rect.height + pad * 2,
      borderRadius: 12,
      zIndex: 9002,
      pointerEvents: 'none',
      animation: 'tourPulse 2s infinite',
      boxSizing: 'border-box',
    })

    const tooltipW = 380
    let top, left, arrowBorder

    if (position === 'bottom') {
      top = rect.bottom + pad + 16
      left = rect.left + rect.width / 2 - tooltipW / 2
      arrowBorder = { borderLeft: '8px solid transparent', borderRight: '8px solid transparent', borderBottom: '8px solid #1e293b' }
    } else {
      top = rect.top - pad - 16
      left = rect.left + rect.width / 2 - tooltipW / 2
      arrowBorder = { borderLeft: '8px solid transparent', borderRight: '8px solid transparent', borderTop: '8px solid #1e293b' }
    }

    // Clamp horizontal
    if (left < 16) left = 16
    if (left + tooltipW > window.innerWidth - 16) left = window.innerWidth - tooltipW - 16

    if (position === 'top') {
      const approxH = 220
      top = rect.top - pad - 16 - approxH
      if (top < 10) top = rect.bottom + pad + 16
    }

    setTooltipStyle({
      position: 'fixed',
      top,
      left,
      width: tooltipW,
      zIndex: 9003,
      animation: 'tourFadeIn 0.3s ease',
    })

    setArrowStyle({
      position: 'absolute',
      ...(position === 'bottom' ? { top: -8, left: tooltipW / 2 - 8 } : { bottom: -8, left: tooltipW / 2 - 8 }),
      width: 0,
      height: 0,
      ...arrowBorder,
    })

    el.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }, [target, position, type])

  // --- MODAL type (welcome screen) ---
  if (type === 'modal') {
    return (
      <>
        <div style={{
          position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.8)',
          zIndex: 9000, display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <div style={{
            background: '#1e293b', border: '1px solid #334155', borderRadius: 16,
            padding: '32px 36px', color: '#e2e8f0', maxWidth: 480, width: '90%',
            boxShadow: '0 20px 60px rgba(0,0,0,0.5)', animation: 'tourFadeIn 0.3s ease',
          }}>
            <div style={{ fontSize: '.72rem', color: '#64748b', marginBottom: 12, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span>{lang === 'en' ? `Step ${step + 1} of ${totalSteps}` : `Paso ${step + 1} de ${totalSteps}`}</span>
              <button onClick={onSkip} style={{ background: 'transparent', border: '1px solid #475569', color: '#94a3b8', padding: '3px 10px', borderRadius: 6, cursor: 'pointer', fontSize: '.72rem' }}>
                {lang === 'en' ? 'Skip Tour' : 'Saltar Tour'}
              </button>
            </div>
            <div style={{ fontSize: '1.3rem', fontWeight: 700, color: '#f1f5f9', marginBottom: 12 }}>
              {title[lang] || title.en}
            </div>
            <div style={{ fontSize: '.9rem', color: '#cbd5e1', lineHeight: 1.6, whiteSpace: 'pre-line' }}>
              {text[lang] || text.en}
            </div>
            <button onClick={onNext} style={{
              marginTop: 20, padding: '12px 28px', borderRadius: 8, border: 'none',
              background: '#6366f1', color: '#fff', fontWeight: 600, cursor: 'pointer',
              fontSize: '.95rem', width: '100%',
            }}>
              {btnText[lang] || btnText.en}
            </button>
          </div>
        </div>
      </>
    )
  }

  // --- TOOLTIP and ACTION types ---
  const isLast = step === totalSteps - 1

  return (
    <>
      {/* Dark backdrop */}
      <div style={{
        position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)',
        zIndex: 9000, pointerEvents: 'auto',
      }} />

      {/* Highlight ring */}
      <div style={highlightStyle} />

      {/* Tooltip card */}
      <div style={{
        ...tooltipStyle, background: '#1e293b', border: '1px solid #334155',
        borderRadius: 12, padding: '20px', color: '#e2e8f0',
        boxShadow: '0 20px 60px rgba(0,0,0,0.5)',
      }}>
        <div style={arrowStyle} />

        {/* Step counter + skip */}
        <div style={{ fontSize: '.72rem', color: '#64748b', marginBottom: 8, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>{lang === 'en' ? `Step ${step + 1} of ${totalSteps}` : `Paso ${step + 1} de ${totalSteps}`}</span>
          <button onClick={onSkip} style={{ background: 'transparent', border: '1px solid #475569', color: '#94a3b8', padding: '3px 10px', borderRadius: 6, cursor: 'pointer', fontSize: '.72rem' }}>
            {lang === 'en' ? 'Skip Tour' : 'Saltar Tour'}
          </button>
        </div>

        {/* Title */}
        <div style={{ fontSize: '1rem', fontWeight: 700, color: '#f1f5f9', marginBottom: 8 }}>
          {title[lang] || title.en}
        </div>

        {/* Text */}
        <div style={{ fontSize: '.85rem', color: '#cbd5e1', lineHeight: 1.5 }}>
          {text[lang] || text.en}
        </div>

        {/* Action / Next / Finish button */}
        <button onClick={onNext} style={{
          marginTop: 16, padding: '10px 24px', borderRadius: 8, border: 'none',
          background: isLast ? '#22c55e' : type === 'action' ? '#8b5cf6' : '#6366f1',
          color: '#fff', fontWeight: 600, cursor: 'pointer', fontSize: '.85rem', width: '100%',
        }}>
          {btnText[lang] || btnText.en}
        </button>
      </div>
    </>
  )
}

/* ------------------------------------------------------------------ */
/*  Components                                                         */
/* ------------------------------------------------------------------ */
function KPICard({ label, value, prefix='', suffix='', onClick }) {
  return (
    <div style={{...S.card, cursor: onClick ? 'pointer' : 'default'}} onClick={onClick}>
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

  // Tour state
  const [tourStep, setTourStep] = useState(0)
  const [tourActive, setTourActive] = useState(true)

  const allCampaigns = [...MOCK.metaCampaigns, ...MOCK.googleCampaigns]

  const skipTour = useCallback(() => {
    setTourActive(false)
    setTourStep(-1)
  }, [])

  const restartTour = useCallback(() => {
    setTourStep(0)
    setTourActive(true)
  }, [])

  const handleParse = useCallback(() => {
    let textToParse = invoiceText
    if(!textToParse.trim()) {
      setInvoiceText(SAMPLE_INVOICE)
      textToParse = SAMPLE_INVOICE
    }
    // Client-side regex parse (mirrors backend InvoiceParser)
    const inv = textToParse.match(/(?:Invoice|Inv|#)\s*[:#]?\s*(\w+[-/]?\w+)/i)
    const dt = textToParse.match(/(?:Date|Fecha)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})/i)
    const tot = textToParse.match(/(?:Total|Amount Due|Grand Total)[:\s]*\$?([\d,]+\.?\d*)/i)
    const sub = textToParse.match(/(?:Subtotal|Sub-total)[:\s]*\$?([\d,]+\.?\d*)/i)
    const tax = textToParse.match(/(?:Tax|IVA|VAT)[:\s]*\$?([\d,]+\.?\d*)/i)
    const vendor = textToParse.match(/(?:From|Bill From|Vendor)[:\s]*([A-Za-z\s&.,]+)/i)
    const items = [...textToParse.matchAll(/(\d+)\s+(.+?)\s+\$?([\d,]+\.?\d*)/g)]
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

  const handleFileUpload = useCallback((e) => {
    const file = e.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    if (file.type === 'text/plain') {
      reader.onload = (ev) => setInvoiceText(ev.target.result)
      reader.readAsText(file)
    } else if (file.type.startsWith('image/')) {
      setInvoiceText(`[${lang === 'en' ? 'Image uploaded' : 'Imagen subida'}: ${file.name}]\n\n${lang === 'en' ? 'In production, this image would be processed by AWS Textract OCR.\nFor this demo, paste the invoice text manually or use the sample.' : 'En produccion, esta imagen seria procesada por AWS Textract OCR.\nPara esta demo, pega el texto de la factura manualmente o usa el ejemplo.'}`)
    } else if (file.name.endsWith('.pdf')) {
      setInvoiceText(`[${lang === 'en' ? 'PDF uploaded' : 'PDF subido'}: ${file.name}]\n\n${lang === 'en' ? 'In production, this PDF would be processed by AWS Textract OCR.\nFor this demo, paste the invoice text manually or use the sample.' : 'En produccion, este PDF seria procesado por AWS Textract OCR.\nPara esta demo, pega el texto de la factura manualmente o usa el ejemplo.'}`)
    }
  }, [lang])

  // Tour "Next" handler — handles scroll + actions
  const handleTourNext = useCallback(() => {
    const currentStep = TOUR_STEPS[tourStep]
    const nextStepIdx = tourStep + 1

    // If action step, trigger the action
    if (currentStep?.autoAction === 'parse') {
      // Auto-fill sample and parse
      setInvoiceText(SAMPLE_INVOICE)
      setTimeout(() => {
        // Trigger parse with sample
        const textToParse = SAMPLE_INVOICE
        const inv = textToParse.match(/(?:Invoice|Inv|#)\s*[:#]?\s*(\w+[-/]?\w+)/i)
        const dt = textToParse.match(/(?:Date|Fecha)[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})/i)
        const tot = textToParse.match(/(?:Total|Amount Due|Grand Total)[:\s]*\$?([\d,]+\.?\d*)/i)
        const sub = textToParse.match(/(?:Subtotal|Sub-total)[:\s]*\$?([\d,]+\.?\d*)/i)
        const tax = textToParse.match(/(?:Tax|IVA|VAT)[:\s]*\$?([\d,]+\.?\d*)/i)
        const vendor = textToParse.match(/(?:From|Bill From|Vendor)[:\s]*([A-Za-z\s&.,]+)/i)
        const items = [...textToParse.matchAll(/(\d+)\s+(.+?)\s+\$?([\d,]+\.?\d*)/g)]
        setParsed({
          invoice_number: inv?inv[1]:'',
          date: dt?dt[1]:'',
          vendor_name: vendor?vendor[1].trim():'',
          subtotal: sub?parseFloat(sub[1].replace(/,/g,'')):0,
          tax: tax?parseFloat(tax[1].replace(/,/g,'')):0,
          total: tot?parseFloat(tot[1].replace(/,/g,'')):0,
          line_items: items.map(m=>({qty:parseInt(m[1]),description:m[2].trim(),amount:parseFloat(m[3].replace(/,/g,''))})),
        })
      }, 100)
    }

    if (currentStep?.autoAction === 'etl') {
      setEtlStatus('running')
      setTimeout(()=>{
        setEtlResult({status:'completed',records:7,sources:['meta','google','ga4'],elapsed:'0.042s'})
        setEtlStatus('completed')
      }, 1500)
    }

    // Advance or finish
    if (nextStepIdx >= TOUR_STEPS.length) {
      setTourActive(false)
      setTourStep(-1)
      return
    }

    setTourStep(nextStepIdx)

    // Auto-scroll next target into view
    const nextTarget = TOUR_STEPS[nextStepIdx]?.target
    if (nextTarget && nextTarget !== 'welcome') {
      setTimeout(() => {
        const el = document.querySelector(`[data-tour="${nextTarget}"]`)
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }, 100)
    }
  }, [tourStep])

  // Determine which sections get elevated z-index during tour
  const tourTargetZStyle = (sectionName) => {
    if (!tourActive || tourStep < 0) return {}
    const currentTarget = TOUR_STEPS[tourStep]?.target
    if (currentTarget === sectionName) {
      return { position: 'relative', zIndex: 9001 }
    }
    return {}
  }

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
          {/* Restart Tour button */}
          <button
            onClick={restartTour}
            title={lang === 'en' ? 'Restart Tour' : 'Reiniciar Tour'}
            style={{
              background: 'transparent',
              border: '1px solid #334155',
              color: '#94a3b8',
              width: 32,
              height: 32,
              borderRadius: '50%',
              cursor: 'pointer',
              fontSize: '.9rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 700,
            }}
          >
            ?
          </button>
        </div>
      </header>

      <div style={{...S.grid,gap:24}}>
        {/* KPIs */}
        <div data-tour="kpi-section" style={{...S.kpiRow, ...tourTargetZStyle('kpi-section')}}>
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
        <div data-tour="campaigns-section" style={{...S.card, ...tourTargetZStyle('campaigns-section')}}>
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
                  <tr key={c.id} style={{transition:'background .2s', cursor: 'pointer'}}
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
          <div data-tour="ocr-section" style={{...S.card, ...tourTargetZStyle('ocr-section')}}>
            <div style={S.sectionTitle}>{t.ocrUpload}</div>
            <div style={{display:'flex',gap:12,marginBottom:12}}>
              <label style={{
                flex:1, display:'flex', alignItems:'center', justifyContent:'center', gap:8,
                padding:'16px', border:'2px dashed #334155', borderRadius:8, cursor:'pointer',
                color:'#64748b', fontSize:'.85rem', transition:'all 0.2s',
              }}>
                <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
                  <path d="M12 16V4m0 0l-4 4m4-4l4 4M4 20h16"/>
                </svg>
                {lang === 'en' ? 'Upload file (PDF, JPG, PNG, TXT)' : 'Subir archivo (PDF, JPG, PNG, TXT)'}
                <input type="file" accept=".pdf,.jpg,.jpeg,.png,.txt" style={{display:'none'}} onChange={handleFileUpload} />
              </label>
              <button onClick={() => setInvoiceText(SAMPLE_INVOICE)} style={{...S.btn, background:'#334155', color:'#e2e8f0', flex:'0 0 auto'}}>
                {lang === 'en' ? '\u{1F4C4} Load Sample' : '\u{1F4C4} Cargar Ejemplo'}
              </button>
            </div>
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
          <div data-tour="etl-section" style={{...S.card, ...tourTargetZStyle('etl-section')}}>
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
                    {i<2 && <span style={{color:'#64748b'}}>&#8594;</span>}
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
          <div data-tour="anomalies-section" style={{...S.card, ...tourTargetZStyle('anomalies-section')}}>
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

      {/* Tour Overlay */}
      {tourActive && tourStep >= 0 && tourStep < TOUR_STEPS.length && (
        <TourOverlay
          stepConfig={TOUR_STEPS[tourStep]}
          step={tourStep}
          totalSteps={TOUR_STEPS.length}
          onNext={handleTourNext}
          onSkip={skipTour}
          lang={lang}
        />
      )}

      <style>{`
        @keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
        @keyframes tourPulse {
          0%, 100% { box-shadow: 0 0 0 0 rgba(99,102,241,0.4); }
          50% { box-shadow: 0 0 0 12px rgba(99,102,241,0); }
        }
        @keyframes tourFadeIn {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  )
}
