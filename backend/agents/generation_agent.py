from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


WORKSPACE = Path("astrachip_workspace")


class GenerationAgent:
    """Mini ChipNeMo-like generation agent using deterministic templates."""

    def generate_project_artifacts(self, prompt: str) -> Dict[str, str]:
        module_name = self._infer_module_name(prompt)
        verilog_path = WORKSPACE / "src/verilog" / f"{module_name}.v"
        def_path = WORKSPACE / "phys/design.def"
        floorplan_path = WORKSPACE / "phys/floorplan.tcl"
        lef_path = WORKSPACE / "phys/lef/standard_cells.lef"

        verilog_path.parent.mkdir(parents=True, exist_ok=True)
        def_path.parent.mkdir(parents=True, exist_ok=True)
        floorplan_path.parent.mkdir(parents=True, exist_ok=True)
        lef_path.parent.mkdir(parents=True, exist_ok=True)

        verilog_path.write_text(self._verilog_template(module_name), encoding="utf-8")
        def_path.write_text(self._def_template(module_name), encoding="utf-8")
        floorplan_path.write_text(self._floorplan_template(module_name), encoding="utf-8")
        lef_path.write_text(self._lef_template(), encoding="utf-8")

        metadata_path = WORKSPACE / "analysis/reports/generation_summary.json"
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        metadata_path.write_text(
            json.dumps({"prompt": prompt, "module": module_name, "status": "generated"}, indent=2),
            encoding="utf-8",
        )

        return {
            "verilog": str(verilog_path),
            "def": str(def_path),
            "floorplan": str(floorplan_path),
            "lef": str(lef_path),
            "summary": str(metadata_path),
        }

    def _infer_module_name(self, prompt: str) -> str:
        lowered = prompt.lower()
        if "memory" in lowered:
            return "memory_controller"
        if "alu" in lowered:
            return "alu"
        return "chip_block"

    def _verilog_template(self, module_name: str) -> str:
        if module_name == "alu":
            return """module alu (
    input wire [7:0] a,
    input wire [7:0] b,
    input wire [2:0] op,
    output reg [7:0] result
);
always @(*) begin
    case(op)
        3'b000: result = a + b;
        3'b001: result = a - b;
        3'b010: result = a & b;
        3'b011: result = a | b;
        3'b100: result = a ^ b;
        3'b101: result = (a < b) ? 8'b1 : 8'b0;
        default: result = 8'b0;
    endcase
end
endmodule
"""
        return f"""module {module_name} (
    input wire clk,
    input wire rst_n,
    output reg done
);
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        done <= 1'b0;
    end else begin
        done <= ~done;
    end
end
endmodule
"""

    def _def_template(self, module_name: str) -> str:
        return f"""VERSION 5.8 ;
DIVIDERCHAR "/" ;
BUSBITCHARS "[]" ;
DESIGN {module_name} ;
DIEAREA ( 0 0 ) ( 100 100 ) ;
COMPONENTS 5 ;
- ALU U_ALU + PLACED ( 80 90 ) N ;
- RegisterFile U_RF + PLACED ( 30 50 ) N ;
- MemoryController U_MEM + PLACED ( 60 70 ) N ;
- Cache U_CACHE + PLACED ( 75 80 ) N ;
- BusInterface U_BUS + PLACED ( 20 20 ) N ;
END COMPONENTS
END DESIGN
"""

    def _floorplan_template(self, module_name: str) -> str:
        return f"""# Floorplan script for {module_name}
set_die_area 0 0 100 100
place_macro ALU 80 90
place_macro RegisterFile 30 50
place_macro MemoryController 60 70
place_macro Cache 75 80
place_macro BusInterface 20 20
"""

    def _lef_template(self) -> str:
        return """VERSION 5.8 ;
BUSBITCHARS "[]" ;
DIVIDERCHAR "/" ;
LAYER M1
  TYPE ROUTING ;
  DIRECTION HORIZONTAL ;
END M1
MACRO ALU
  CLASS CORE ;
  ORIGIN 0 0 ;
  SIZE 10 BY 10 ;
END ALU
END LIBRARY
"""
