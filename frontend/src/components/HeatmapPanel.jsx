export default function HeatmapPanel({ hotspots = [] }) {
  return (
    <div className="panel">
      <h3>Thermal Hotspots</h3>
      <div className="floorplan">
        {hotspots.map((h, idx) => (
          <div
            key={idx}
            className="hotspot"
            style={{ left: `${h.x}%`, top: `${100 - h.y}%` }}
            title={`${h.module}: ${h.temperature}°C`}
          />
        ))}
      </div>
      <p className="caption">Red markers indicate predicted thermal risk in die coordinates.</p>
    </div>
  )
}
