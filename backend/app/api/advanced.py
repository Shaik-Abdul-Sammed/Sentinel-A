from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.api.auth import require_roles
from app.services.advanced_security import advanced_security

router = APIRouter()


class IndicatorRequest(BaseModel):
    indicator: str
    source: str = Field(default="manual")


class TravelPoint(BaseModel):
    lat: float
    lon: float
    timestamp: str


class ImpossibleTravelRequest(BaseModel):
    last: TravelPoint
    current: TravelPoint


class DeviceTrustRequest(BaseModel):
    known: Dict[str, Any]
    current: Dict[str, Any]


class HoneypotRequest(BaseModel):
    endpoint: str
    actor_id: str
    ip: str


class DecoyCredentialRequest(BaseModel):
    username: str
    password: str


class AdaptiveThrottleRequest(BaseModel):
    requests_per_minute: int
    failed_ratio: float
    risk_score: int


class IOCExtractRequest(BaseModel):
    text: str


class CampaignCorrelateRequest(BaseModel):
    alerts: List[Dict[str, Any]]


class ForensicBundleRequest(BaseModel):
    incident_id: str
    alerts: List[Dict[str, Any]]
    timeline: List[Dict[str, Any]]


class PlaybookRequest(BaseModel):
    threat_type: str
    risk_level: str


class ConsoleLogAnalysisRequest(BaseModel):
    logs: List[str] = Field(default_factory=list)
    scenario_id: str | None = None


class RuntimeConsoleIngestRequest(BaseModel):
    message: str
    source: str = Field(default="window.onerror")
    level: str = Field(default="error")
    stack: str | None = None
    url: str | None = None
    user_agent: str | None = None
    timestamp: str | None = None


@router.post("/threat-intel/blocklist/add")
async def blocklist_add(request: IndicatorRequest, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.add_indicator(request.indicator, request.source)


@router.get("/threat-intel/blocklist")
async def blocklist_get(_: dict = Depends(require_roles("soc", "admin"))):
    return {
        "indicators": sorted(advanced_security.blocklist),
        "total": len(advanced_security.blocklist),
    }


@router.delete("/threat-intel/blocklist/{indicator}")
async def blocklist_delete(indicator: str, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.remove_indicator(indicator)


@router.post("/threat-intel/blocklist/lookup")
async def blocklist_lookup(request: IndicatorRequest, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.lookup_indicator(request.indicator)


@router.post("/geo/impossible-travel")
async def impossible_travel(request: ImpossibleTravelRequest, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.impossible_travel(request.last.model_dump(), request.current.model_dump())


@router.post("/device/trust-check")
async def device_trust(request: DeviceTrustRequest, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.device_trust(request.known, request.current)


@router.post("/honeypot/tripwire")
async def honeypot_tripwire(request: HoneypotRequest, _: dict = Depends(require_roles("sensor", "admin", "soc"))):
    return advanced_security.honeypot_tripwire(request.endpoint, request.actor_id, request.ip)


@router.post("/identity/decoy-credential-check")
async def decoy_check(request: DecoyCredentialRequest, _: dict = Depends(require_roles("sensor", "admin", "soc"))):
    return advanced_security.decoy_credential_check(request.username, request.password)


@router.post("/network/adaptive-throttle")
async def adaptive_throttle(request: AdaptiveThrottleRequest, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.adaptive_throttle(
        requests_per_minute=request.requests_per_minute,
        failed_ratio=request.failed_ratio,
        risk_score=request.risk_score,
    )


@router.post("/ioc/extract")
async def ioc_extract(request: IOCExtractRequest, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.extract_iocs(request.text)


@router.post("/campaign/correlate")
async def correlate_campaigns(request: CampaignCorrelateRequest, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.correlate_campaigns(request.alerts)


@router.post("/forensics/export")
async def forensics_export(request: ForensicBundleRequest, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.forensic_bundle(request.incident_id, request.alerts, request.timeline)


@router.post("/playbook/generate")
async def generate_playbook(request: PlaybookRequest, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.generate_playbook(request.threat_type, request.risk_level)


@router.get("/console/scenarios")
async def console_scenarios(_: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.get_console_scenarios()


@router.post("/console/analyze")
async def console_analyze(request: ConsoleLogAnalysisRequest, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.analyze_console_logs(request.logs, request.scenario_id)


@router.post("/console/runtime/ingest")
async def console_runtime_ingest(request: RuntimeConsoleIngestRequest, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.ingest_runtime_console_event(request.model_dump())


@router.get("/console/runtime/events")
async def console_runtime_events(limit: int = 200, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.get_runtime_console_events(limit=limit)


@router.delete("/console/runtime/events")
async def console_runtime_events_clear(_: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.clear_runtime_console_events()


@router.post("/console/runtime/analyze")
async def console_runtime_analyze(limit: int = 250, _: dict = Depends(require_roles("soc", "admin"))):
    return advanced_security.analyze_runtime_console_events(limit=limit)
