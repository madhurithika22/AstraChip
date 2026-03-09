# AstraChip AI

AI-Driven Chip Design Copilot that simulates a Mini ChipNeMo-like workflow for RTL generation, physical-aware analysis, and automated refactoring.

## Features
- **Generation Agent**: creates Verilog, floorplan TCL, LEF/DEF placeholders.
- **AstraBrain Analysis Engine**: parses RTL + DEF, builds mock graph, predicts congestion and thermal hotspots.
- **Refactor Agent**: applies thermal/congestion fixes and writes updated DEF/report under `refactored/`.
- **CLI**: `astra generate`, `astra analyze`, `astra fix thermal`, `astra fix congestion`.
- **Frontend Dashboard**: run generation/analysis and visualize hotspot markers.

## Project Structure
- `astrachip_workspace/`: managed design artifacts and reports.
- `backend/`: FastAPI app + agents/parsers/analysis/services.
- `frontend/`: React dashboard.
- `astra.py`: CLI entrypoint.

## Quickstart
### Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```

### CLI
```bash
./astra.py generate "Design an 8-bit RISC-V ALU optimized for low power"
./astra.py analyze
./astra.py fix thermal
./astra.py fix congestion
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Analysis Output JSON
```json
{
  "routing_congestion": 0.82,
  "thermal_hotspots": [
    {"x": 80, "y": 90, "temperature": 105}
  ],
  "power_density": 0.73,
  "warnings": [],
  "suggestions": []
}
```
