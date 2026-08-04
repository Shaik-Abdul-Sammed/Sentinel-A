from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from app.api.auth import require_roles
from app.core import security
from app.services.telemetry_engine import TelemetryEvent, engine
from app.services.ws_manager import ws_manager

router = APIRouter()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class LogEventRequest(BaseModel):
    source: str = Field(default="web-portal")
    event_type: str = Field(default="AUTH")
    actor_id: str = Field(default="anonymous")
    ip: str = Field(default="0.0.0.0")
    endpoint: str = Field(default="/")
    status: str = Field(default="SUCCESS")
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=now_iso)


class BatchLogRequest(BaseModel):
    logs: List[LogEventRequest]


class PhishingScanRequest(BaseModel):
    content: str


class ResolveAlertRequest(BaseModel):
    note: str = Field(default="Resolved by SOC analyst")


async def broadcast_state(snapshot: Dict[str, Any] | None = None):
    packet = {
        "type": "telemetry.update",
        "status": engine.get_status(),
        "latest_alert": (snapshot or {}).get("alert"),
        "latest_timeline": engine.get_timeline(1),
    }
    await ws_manager.broadcast(packet)


@router.post("/logs")
async def ingest_log(request: LogEventRequest, _: dict = Depends(require_roles("sensor", "admin"))):
    event = TelemetryEvent(**request.model_dump())
    result = await engine.ingest(event)
    await broadcast_state(result)
    return result


@router.post("/logs/batch")
async def ingest_log_batch(request: BatchLogRequest, _: dict = Depends(require_roles("sensor", "admin"))):
    results = []
    for item in request.logs:
        results.append(await engine.ingest(TelemetryEvent(**item.model_dump())))
    await broadcast_state(results[-1] if results else None)
    return {"processed": len(results), "results": results}


@router.post("/phishing-scan")
async def phishing_scan(request: PhishingScanRequest):
    return await engine.run_phishing_scan(request.content)


@router.get("/status")
async def status():
    return engine.get_status()


@router.get("/alerts")
async def alerts(limit: int = 25, _: dict = Depends(require_roles("soc", "admin"))):
    return {"items": engine.get_alerts(limit)}


@router.get("/timeline")
async def timeline(limit: int = 50, _: dict = Depends(require_roles("soc", "admin"))):
    return {"items": engine.get_timeline(limit)}


@router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str, request: ResolveAlertRequest, user: dict = Depends(require_roles("soc", "admin"))):
    result = engine.resolve_alert(alert_id)
    if not result:
        raise HTTPException(status_code=404, detail="Alert not found")
    result["resolution_note"] = request.note
    result["resolved_by"] = user.get("username")
    await broadcast_state()
    return result


@router.post("/simulate/{scenario}")
async def simulate_scenario(scenario: str, _: dict = Depends(require_roles("soc", "admin"))):
    scenario = scenario.lower()

    if scenario == "phishing":
        sample = LogEventRequest(
            source="citizen-portal",
            event_type="EMAIL",
            actor_id="target_user_12",
            ip="185.199.110.1",
            endpoint="/inbox/message/991",
            status="DELIVERED",
            payload={"content": "URGENT: verify your account now at http://secure-bank-login-update.bit.ly/verify"},
        )
        result = await engine.ingest(TelemetryEvent(**sample.model_dump()))
        await broadcast_state(result)
        return {"scenario": scenario, "result": result}

    if scenario == "insider":
        sample = LogEventRequest(
            source="gov-hr-portal",
            event_type="AUTH",
            actor_id="emp_094",
            ip="10.20.8.11",
            endpoint="/api/payroll/export",
            status="FAILED",
            payload={"action_count": 140, "hour_of_day": 2, "data_volume_mb": 1250},
        )
        result = await engine.ingest(TelemetryEvent(**sample.model_dump()))
        await broadcast_state(result)
        return {"scenario": scenario, "result": result}

    return {"error": "Unknown scenario. Use phishing or insider."}


@router.websocket("/ws")
async def telemetry_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        auth_header = websocket.headers.get("authorization", "")
        if auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ", 1)[1]

    payload = security.decode_access_token(token) if token else None
    if not payload or payload.get("role") not in {"soc", "admin"}:
        await websocket.close(code=1008)
        return

    await ws_manager.connect(websocket)
    try:
        await websocket.send_json(
            {
                "type": "telemetry.bootstrap",
                "status": engine.get_status(),
                "latest_alert": engine.get_alerts(1),
                "latest_timeline": engine.get_timeline(5),
                "viewer_role": payload.get("role"),
            }
        )
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
