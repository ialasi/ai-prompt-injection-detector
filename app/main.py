from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.security_engine import PromptSecurityEngine


app = FastAPI(
    title="AI Prompt Injection Detector",
    description="Security API for detecting and analyzing prompt injection attacks.",
    version="0.2.0",
)

security_engine = PromptSecurityEngine()


class AnalyzeRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Prompt to analyze")


class AnalyzeResponse(BaseModel):
    classification: str
    risk_score: int
    severity: str
    action: str
    indicators: list[str]


@app.get("/")
def root():
    return {
        "service": "AI Prompt Injection Detector",
        "status": "online",
        "version": "0.2.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_prompt(request: AnalyzeRequest):
    result = security_engine.analyze(request.prompt)

    return AnalyzeResponse(
        classification=result.classification,
        risk_score=result.risk_score,
        severity=result.severity,
        action=result.action,
        indicators=result.indicators,
    )

