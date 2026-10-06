from fastapi import FastAPI

app = FastAPI(
    title="AI Prompt Injection Detector",
    description="Security API for detecting and analyzing prompt injection attacks.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "service": "AI Prompt Injection Detector",
        "status": "online",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }