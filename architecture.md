# AstraChip AI Architecture

## System Modules
1. **Intelligent Workspace** (`astrachip_workspace`)
2. **Generation Agent** (`backend/agents/generation_agent.py`)
3. **AstraBrain Analysis Engine** (`backend/analysis/*` + `backend/services/analysis_service.py`)
4. **Refactor Agent** (`backend/agents/refactor_agent.py`)
5. **Developer Interfaces** (FastAPI + CLI + React dashboard)

## Data Flow
User Prompt -> Generation Agent -> Verilog/DEF/Floorplan
-> Feature Extraction -> Graph Builder -> Mock GNN Model
-> Analysis Reports/Heatmaps -> Refactor Agent -> Updated DEF

## Backend API
- `POST /generate`
- `POST /analyze`
- `POST /fix/{issue_type}`
- `GET /health`

## Frontend
- Trigger generation and analysis
- View summary metrics
- Visualize thermal hotspots on floorplan canvas
- Run auto-fix operations
