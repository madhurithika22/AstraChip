from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.agents.generation_agent import GenerationAgent
from backend.agents.refactor_agent import RefactorAgent
from backend.services.analysis_service import AnalysisService


app = FastAPI(title="AstraChip AI API", version="1.0.0")
generation_agent = GenerationAgent()
analysis_service = AnalysisService()
refactor_agent = RefactorAgent()


class GenerateRequest(BaseModel):
    prompt: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "AstraChip AI"}


@app.post("/generate")
def generate_design(request: GenerateRequest) -> dict:
    outputs = generation_agent.generate_project_artifacts(request.prompt)
    return {"status": "generated", "artifacts": outputs}


@app.post("/analyze")
def analyze_design() -> dict:
    try:
        return analysis_service.run_analysis()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/fix/{issue_type}")
def fix_issue(issue_type: str) -> dict:
    if issue_type not in {"thermal", "congestion"}:
        raise HTTPException(status_code=400, detail="issue_type must be thermal or congestion")

    analysis_result = analysis_service.run_analysis()
    output = refactor_agent.apply_fix(issue_type, analysis_result)
    return {"status": "refactored", "issue_type": issue_type, "output": output}
