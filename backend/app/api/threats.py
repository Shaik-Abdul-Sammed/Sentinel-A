from fastapi import APIRouter, Depends, HTTPException
from app.api.auth import oauth2_scheme
from pydantic import BaseModel
from ai_layer.phishing.detector import PhishingDetector
from ai_layer.anomaly.detector import AnomalyDetector
from ai_layer.agent_orch.orchestrator import AgentOrchestrator
import sys
import os

# Add project root to sys.path to allow sibling imports (ai_layer)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

router = APIRouter()
phishing_detector = PhishingDetector()
anomaly_detector = AnomalyDetector()
agent_orch = AgentOrchestrator()

class URLAnalysisRequest(BaseModel):
    url: str

class BehaviorAnalysisRequest(BaseModel):
    user_id: str
    activity_logs: list

class PrivacyScanRequest(BaseModel):
    content: str

@router.post("/url")
async def analyze_url(request: URLAnalysisRequest, token: str = Depends(oauth2_scheme)):
    analysis = await phishing_detector.analyze(request.url)
    suggestions = await agent_orch.get_mitigation_suggestions("PHISHING", analysis)
    return {
        "url": request.url,
        "analysis": analysis,
        "recommendations": suggestions
    }

@router.post("/behavior")
async def analyze_behavior(request: BehaviorAnalysisRequest, token: str = Depends(oauth2_scheme)):
    analysis = anomaly_detector.predict(request.activity_logs)
    suggestions = await agent_orch.get_mitigation_suggestions("INSIDER_THREAT", analysis)
    return {
        "user_id": request.user_id,
        "analysis": analysis,
        "recommendations": suggestions
    }

@router.post("/privacy")
async def scan_privacy(request: PrivacyScanRequest, token: str = Depends(oauth2_scheme)):
    # Placeholder for PII detection
    return {
        "content_length": len(request.content),
        "pii_detected": False,
        "findings": []
    }
