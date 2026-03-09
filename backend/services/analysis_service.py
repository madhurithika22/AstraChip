from __future__ import annotations

import json
from pathlib import Path

from backend.analysis.congestion_model import CongestionModel
from backend.analysis.feature_extractor import FeatureExtractor
from backend.analysis.graph_builder import GraphBuilder
from backend.parsers.def_parser import DefParser
from backend.parsers.verilog_parser import VerilogParser


class AnalysisService:
    def __init__(self) -> None:
        self.workspace = Path("astrachip_workspace")
        self.verilog_parser = VerilogParser()
        self.def_parser = DefParser()
        self.feature_extractor = FeatureExtractor()
        self.graph_builder = GraphBuilder()
        self.model = CongestionModel(self.workspace / "models/astrachip_v1.pth")

    def run_analysis(self) -> dict:
        verilog_path = self.workspace / "src/verilog/alu.v"
        def_path = self.workspace / "phys/design.def"

        if not verilog_path.exists() or not def_path.exists():
            raise FileNotFoundError("Design artifacts missing. Run `astra generate` first.")

        verilog_meta = self.verilog_parser.parse(str(verilog_path))
        macros = self.def_parser.parse(str(def_path))
        features = self.feature_extractor.extract(macros)
        graph = self.graph_builder.build(features)
        prediction = self.model.predict(graph)
        prediction["verilog"] = verilog_meta

        self._write_outputs(prediction, graph)
        return prediction

    def _write_outputs(self, prediction: dict, graph: dict) -> None:
        analysis_dir = self.workspace / "analysis"
        (analysis_dir / "reports").mkdir(parents=True, exist_ok=True)
        (analysis_dir / "congestion_maps").mkdir(parents=True, exist_ok=True)
        (analysis_dir / "thermal_maps").mkdir(parents=True, exist_ok=True)

        (analysis_dir / "reports/analysis_report.json").write_text(
            json.dumps(prediction, indent=2), encoding="utf-8"
        )
        (analysis_dir / "floorplan_heatmap.json").write_text(
            json.dumps({"graph": graph, "prediction": prediction}, indent=2), encoding="utf-8"
        )
        (analysis_dir / "congestion_maps/routing_congestion.json").write_text(
            json.dumps({"routing_congestion": prediction["routing_congestion"]}, indent=2), encoding="utf-8"
        )
        (analysis_dir / "thermal_maps/thermal_hotspots.json").write_text(
            json.dumps({"thermal_hotspots": prediction["thermal_hotspots"]}, indent=2), encoding="utf-8"
        )
