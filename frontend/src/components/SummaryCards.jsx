export default function SummaryCards({ result }) {
  return (
    <div className="grid">
      <div className="card"><span>Routing Congestion</span><strong>{result?.routing_congestion ?? '--'}</strong></div>
      <div className="card"><span>Power Density</span><strong>{result?.power_density ?? '--'}</strong></div>
      <div className="card"><span>Thermal Hotspots</span><strong>{result?.thermal_hotspots?.length ?? 0}</strong></div>
    </div>
  )
}
