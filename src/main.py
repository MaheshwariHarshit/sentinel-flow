from fastapi import FastAPI
from src.api.webhooks import router as webhooks_router
from src.services.db import init_db

# Initialize database tables on startup
init_db()

app = FastAPI(
    title="Sentinel-Flow",
    description="Agentic SRE Assistant for CI/CD Incident Remediation",
    version="1.0.0"
)

app.include_router(webhooks_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
