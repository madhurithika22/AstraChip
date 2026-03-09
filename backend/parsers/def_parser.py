from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List


COMPONENT_PATTERN = re.compile(r"-\s+(?P<name>\w+)\s+\w+\s+\+\s+PLACED\s+\(\s*(?P<x>\d+)\s+(?P<y>\d+)\s*\)")


class DefParser:
    """Extract macro placements from a simplified DEF file."""

    materials = ["Copper", "Gold", "Tungsten", "Silicon"]

    def parse(self, path: str) -> List[Dict]:
        text = Path(path).read_text(encoding="utf-8")
        components: List[Dict] = []
        for idx, match in enumerate(COMPONENT_PATTERN.finditer(text)):
            components.append(
                {
                    "name": match.group("name"),
                    "x": int(match.group("x")),
                    "y": int(match.group("y")),
                    "material": self.materials[idx % len(self.materials)],
                }
            )
        return components
