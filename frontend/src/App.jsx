import { useState } from 'react'
import HeatmapPanel from './components/HeatmapPanel'
import SummaryCards from './components/SummaryCards'
import { analyze, fix, generate } from './services/api'

export default function App() {
  const [prompt, setPrompt] = useState('Design an 8-bit RISC-V ALU optimized for low power')
  const [result, setResult] = useState(null)
  const [logs, setLogs] = useState([])

  const pushLog = (message) => setLogs((prev) => [message, ...prev].slice(0, 8))

  return (
    <main className="container">
      <h1>AstraChip AI — Hardware Design Copilot</h1>
      <div className="actions">
        <input value={prompt} onChange={(e) => setPrompt(e.target.value)} />
        <button onClick={async () => { const r = await generate(prompt); pushLog(`Generated: ${Object.keys(r.artifacts || {}).join(', ')}`) }}>Generate</button>
        <button onClick={async () => { const r = await analyze(); setResult(r); pushLog('Analysis complete') }}>Analyze</button>
        <button onClick={async () => { await fix('thermal'); const r = await analyze(); setResult(r); pushLog('Thermal fix applied') }}>Fix Thermal</button>
        <button onClick={async () => { await fix('congestion'); const r = await analyze(); setResult(r); pushLog('Congestion fix applied') }}>Fix Congestion</button>
      </div>

      <SummaryCards result={result} />
      <HeatmapPanel hotspots={result?.thermal_hotspots} />

      <section className="panel">
        <h3>AI Suggestions</h3>
        <ul>{(result?.suggestions || []).map((s, i) => <li key={i}>{s}</li>)}</ul>
      </section>

      <section className="panel">
        <h3>Activity Log</h3>
        <ul>{logs.map((l, i) => <li key={i}>{l}</li>)}</ul>
      </section>
    </main>
  )
}
