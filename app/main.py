from fastapi import FastAPI, Request
from pydantic import BaseModel, Field, field_validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.security_engine import PromptSecurityEngine

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="AI Prompt Injection Detector",
    description="Security API for detecting and analyzing prompt injection attacks.",
    version="0.2.0",
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

security_engine = PromptSecurityEngine()


class AnalyzeRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=100_000,
        description="Prompt to analyze",
    )

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Prompt must contain non-whitespace characters")
        return value


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
@limiter.limit("10/minute")
def analyze_prompt(request: Request, payload: AnalyzeRequest):
    result = security_engine.analyze(payload.prompt)
    return AnalyzeResponse(
        classification=result.classification,
        risk_score=result.risk_score,
        severity=result.severity,
        action=result.action,
        indicators=result.indicators,
    )
