from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from backend.parsers.def_parser import DefParser


class RefactorAgent:
    def __init__(self) -> None:
        self.workspace = Path("astrachip_workspace")
        self.parser = DefParser()

    def apply_fix(self, issue_type: str, analysis_result: Dict) -> Dict:
        def_path = self.workspace / "phys/design.def"
        components = self.parser.parse(str(def_path))

        updates: List[Dict] = []
        for component in components:
            old = (component["x"], component["y"])
            if issue_type == "thermal" and component["x"] > 70 and component["y"] > 70:
                component["x"], component["y"] = component["x"] - 35, component["y"] - 30
            if issue_type == "congestion" and component["x"] > 55:
                component["x"] = max(10, component["x"] - 20)
            new = (component["x"], component["y"])
            if old != new:
                updates.append({"module": component["name"], "from": old, "to": new})

        out_dir = self.workspace / "refactored"
        (out_dir / "verilog").mkdir(parents=True, exist_ok=True)
        (out_dir / "floorplan_updates").mkdir(parents=True, exist_ok=True)

        updated_def = self._serialize_def(components)
        def_out = out_dir / "floorplan_updates/design_refactored.def"
        report_out = out_dir / "floorplan_updates/refactor_report.json"
        def_out.write_text(updated_def, encoding="utf-8")
        report_out.write_text(
            json.dumps({"issue_type": issue_type, "updates": updates, "analysis": analysis_result}, indent=2),
            encoding="utf-8",
        )

        return {"updated_def": str(def_out), "report": str(report_out), "updates": updates}

    def _serialize_def(self, components: List[Dict]) -> str:
        lines = [
            "VERSION 5.8 ;",
            "DIVIDERCHAR \"/\" ;",
            'BUSBITCHARS "[]" ;',
            "DESIGN refactored_design ;",
            "DIEAREA ( 0 0 ) ( 100 100 ) ;",
            f"COMPONENTS {len(components)} ;",
        ]
        for c in components:
            lines.append(f"- {c['name']} U_{c['name'][:3].upper()} + PLACED ( {c['x']} {c['y']} ) N ;")
        lines.extend(["END COMPONENTS", "END DESIGN", ""])
        return "\n".join(lines)
