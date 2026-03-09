from __future__ import annotations

from pathlib import Path
from typing import Dict


class CongestionModel:
    """Simulated GNN model that predicts congestion/thermal risk."""

    def __init__(self, model_path: str = "astrachip_workspace/models/astrachip_v1.pth") -> None:
        self.model_path = Path(model_path)
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.model_path.exists():
            self.model_path.write_text("mock-gnn-weights", encoding="utf-8")

    def predict(self, graph: Dict) -> Dict:
        nodes = graph["nodes"]
        avg_density = sum(node["density"] for node in nodes) / max(1, len(nodes))
        avg_power = sum(node["power"] for node in nodes) / max(1, len(nodes))
        edge_factor = min(1.0, len(graph["edges"]) / 8)

        routing = min(0.99, 0.45 * avg_density + 0.35 * edge_factor + 0.2 * avg_power)
        power_density = min(0.99, 0.6 * avg_power + 0.4 * avg_density)

        hotspots = []
        for node in nodes:
            temperature = 50 + (node["power"] * 35) + (node["density"] * 30)
            if temperature >= 95:
                hotspots.append({"x": node["x"], "y": node["y"], "temperature": round(temperature, 1), "module": node["name"]})

        warnings = []
        suggestions = []
        if routing > 0.75:
            warnings.append(f"Routing congestion risk is high ({routing:.2f}).")
            suggestions.append("Spread tightly connected macros across die quadrants.")
        if hotspots:
            warnings.append(f"Detected {len(hotspots)} thermal hotspot(s).")
            suggestions.append("Move high-power macros away from North-East region.")

        return {
            "routing_congestion": round(routing, 2),
            "thermal_hotspots": hotspots,
            "power_density": round(power_density, 2),
            "warnings": warnings,
            "suggestions": suggestions,
        }
