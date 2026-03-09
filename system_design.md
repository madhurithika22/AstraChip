# System Design

## Workspace Artifacts
- `src/`: RTL/Verilog sources.
- `phys/`: LEF/DEF/floorplan constraints.
- `analysis/`: reports, congestion maps, thermal maps, floorplan heatmap JSON.
- `refactored/`: improved floorplans and reports.
- `models/astrachip_v1.pth`: mock model placeholder.

## Mock GNN Pipeline
1. Parse Verilog module metadata.
2. Parse DEF macro coordinates.
3. Build node features: power, location, density, material.
4. Build graph edges by geometric proximity.
5. Infer routing congestion, thermal hotspots, power density.
6. Generate warnings and suggestions.

## Refactor Strategy
- Thermal fix: shift high-power macros away from north-east quadrant.
- Congestion fix: spread macros on dense side of die.

## Extensibility
- Replace `CongestionModel` with PyTorch Geometric model.
- Add websocket stream for live progress.
- Extend parser coverage for full DEF/LEF syntax.
