from __future__ import annotations

from typing import Dict, List


class FeatureExtractor:
    """Extracts synthetic numerical features for a chip graph."""

    def extract(self, macros: List[Dict]) -> List[Dict]:
        features = []
        for macro in macros:
            x, y = macro["x"], macro["y"]
            power = self._power_hint(macro["name"])
            density = min(1.0, (x + y) / 180)
            features.append(
                {
                    "name": macro["name"],
                    "x": x,
                    "y": y,
                    "power": power,
                    "density": density,
                    "material": macro.get("material", "Silicon"),
                }
            )
        return features

    def _power_hint(self, name: str) -> float:
        key = name.lower()
        if "alu" in key:
            return 0.92
        if "cache" in key or "memory" in key:
            return 0.84
        if "register" in key:
            return 0.62
        return 0.45
