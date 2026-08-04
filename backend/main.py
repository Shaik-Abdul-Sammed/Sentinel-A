from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import advanced, auth, threats, telemetry
from app.core.telemetry_push_middleware import TelemetryPushMiddleware

app = FastAPI(
    title="Sentinel-A: India’s AI Agent Cyber Shield",
    description="Advanced AI-driven cybersecurity protection platform.",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TelemetryPushMiddleware)

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(threats.router, prefix="/analyze", tags=["Threat Detection"])
app.include_router(telemetry.router, prefix="/telemetry", tags=["Telemetry & Orchestration"])
app.include_router(advanced.router, prefix="/advanced", tags=["Advanced Security Features"])
@app.get("/")
async def root():
    return {"message": "Sentinel-A Shield is Online", "status": "active"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "engine": "Sentinel-A AI Core"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
