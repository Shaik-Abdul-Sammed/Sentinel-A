from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4
from zoneinfo import ZoneInfo

from ai_layer.agent_orch.orchestrator import AgentOrchestrator
from ai_layer.anomaly.detector import AnomalyDetector
from ai_layer.phishing.detector import PhishingDetector
from app.core.database import get_db_session
from app.models.telemetry import AlertORM, TelemetryEventORM, TimelineORM
from sqlalchemy import func


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class TelemetryEvent:
    source: str
    event_type: str
    actor_id: str
    ip: str
    endpoint: str
    status: str
    payload: Dict[str, Any]
    timestamp: str


class TelemetryEngine:
    """Persistent telemetry pipeline backed by PostgreSQL."""

    def __init__(self) -> None:
        self._phishing = PhishingDetector()
        self._anomaly = AnomalyDetector()
        self._orchestrator = AgentOrchestrator()

    async def ingest(self, event: TelemetryEvent) -> Dict[str, Any]:
        event_id = f"evt_{uuid4().hex[:12]}"
        event_obj = {
            "id": event_id,
            "source": event.source,
            "event_type": event.event_type,
            "actor_id": event.actor_id,
            "ip": event.ip,
            "endpoint": event.endpoint,
            "status": event.status,
            "payload": event.payload,
            "timestamp": event.timestamp or utc_now_iso(),
        }

        detection = await self._detect(event_obj)
        decision = await self._orchestrator.decide_response(
            threat_type=detection["threat_type"],
            score=detection["risk_score"],
            evidence=detection,
        )

        alert = {
            "alert_id": f"alt_{uuid4().hex[:12]}",
            "event_id": event_id,
            "title": decision["title"],
            "threat_type": detection["threat_type"],
            "risk_score": detection["risk_score"],
            "risk_level": decision["risk_level"],
            "decision": decision["decision"],
            "actions": decision["actions"],
            "actor_id": event.actor_id,
            "source": event.source,
            "status": "OPEN" if detection["risk_score"] >= 50 else "INFO",
            "reasoning": detection["reasoning"],
            "created_at": utc_now_iso(),
        }

        with get_db_session() as db:
            db.add(
                TelemetryEventORM(
                    id=event_id,
                    source=event_obj["source"],
                    event_type=event_obj["event_type"],
                    actor_id=event_obj["actor_id"],
                    ip=event_obj["ip"],
                    endpoint=event_obj["endpoint"],
                    status=event_obj["status"],
                    payload=event_obj["payload"],
                    timestamp=self._to_dt(event_obj["timestamp"]),
                )
            )
            # Flush parent row first so FK checks on alerts always pass in Postgres.
            db.flush()

            db.add(
                TimelineORM(
                    time=self._to_dt(alert["created_at"]),
                    event="DETECTION",
                    message=f"{alert['threat_type']} detected for {event.actor_id}",
                    risk_score=alert["risk_score"],
                )
            )

            if detection["risk_score"] >= 35:
                db.add(
                    AlertORM(
                        alert_id=alert["alert_id"],
                        event_id=event_id,
                        title=alert["title"],
                        threat_type=alert["threat_type"],
                        risk_score=alert["risk_score"],
                        risk_level=alert["risk_level"],
                        decision=alert["decision"],
                        actions=alert["actions"],
                        actor_id=alert["actor_id"],
                        source=alert["source"],
                        status=alert["status"],
                        reasoning=alert["reasoning"],
                        created_at=self._to_dt(alert["created_at"]),
                    )
                )
                db.add(
                    TimelineORM(
                        time=self._to_dt(utc_now_iso()),
                        event="RESPONSE",
                        message=f"Action: {alert['decision']}",
                        risk_score=alert["risk_score"],
                    )
                )

        return {"event": event_obj, "detection": detection, "alert": alert}

    async def run_phishing_scan(self, text: str) -> Dict[str, Any]:
        analysis = await self._phishing.analyze(text)
        score = int(float(analysis.get("confidence", 0.0)) * 100)
        decision = await self._orchestrator.decide_response(
            threat_type="PHISHING",
            score=score,
            evidence=analysis,
        )
        return {
            "analysis": analysis,
            "risk_score": score,
            "decision": decision,
        }

    def get_alerts(self, limit: int = 25) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            rows = db.query(AlertORM).order_by(AlertORM.created_at.desc()).limit(limit).all()
            return [
                {
                    "alert_id": row.alert_id,
                    "event_id": row.event_id,
                    "title": row.title,
                    "threat_type": row.threat_type,
                    "risk_score": row.risk_score,
                    "risk_level": row.risk_level,
                    "decision": row.decision,
                    "actions": row.actions,
                    "actor_id": row.actor_id,
                    "source": row.source,
                    "status": row.status,
                    "reasoning": row.reasoning,
                    "created_at": row.created_at.isoformat(),
                }
                for row in rows
            ]

    def get_timeline(self, limit: int = 50) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            rows = db.query(TimelineORM).order_by(TimelineORM.time.desc()).limit(limit).all()
            return [
                {
                    "time": row.time.isoformat(),
                    "event": row.event,
                    "message": row.message,
                    "risk_score": row.risk_score,
                }
                for row in rows
            ]

    def get_status(self) -> Dict[str, Any]:
        with get_db_session() as db:
            events_processed = db.query(func.count(TelemetryEventORM.id)).scalar() or 0
            alerts_total = db.query(func.count(AlertORM.alert_id)).scalar() or 0
            open_alerts = db.query(func.count(AlertORM.alert_id)).filter(AlertORM.status == "OPEN").scalar() or 0
            blocked = db.query(func.count(AlertORM.alert_id)).filter(AlertORM.decision == "BLOCK").scalar() or 0
            escalated = db.query(func.count(AlertORM.alert_id)).filter(AlertORM.decision == "ESCALATE").scalar() or 0
            avg_risk = db.query(func.avg(AlertORM.risk_score)).scalar() or 0.0

        return {
            "shield_status": "ACTIVE",
            "events_processed": int(events_processed),
            "alerts_total": int(alerts_total),
            "alerts_open": open_alerts,
            "auto_blocked": blocked,
            "escalations": escalated,
            "average_risk_score": round(float(avg_risk), 2),
            "last_updated": utc_now_iso(),
        }

    def resolve_alert(self, alert_id: str) -> Dict[str, Any] | None:
        with get_db_session() as db:
            row = db.query(AlertORM).filter(AlertORM.alert_id == alert_id).first()
            if not row:
                return None
            row.status = "RESOLVED"
            db.add(
                TimelineORM(
                    time=self._to_dt(utc_now_iso()),
                    event="SOC_ACTION",
                    message=f"Alert {alert_id} resolved by analyst",
                    risk_score=row.risk_score,
                )
            )
            return {
                "alert_id": row.alert_id,
                "status": row.status,
                "decision": row.decision,
            }

    async def _detect(self, event: Dict[str, Any]) -> Dict[str, Any]:
        etype = event["event_type"].upper()
        payload = event.get("payload", {})

        if etype in {"EMAIL", "URL_SUBMISSION", "PHISHING_TEXT"}:
            text = payload.get("content") or payload.get("url") or ""
            p = await self._phishing.analyze(text)
            score = int(float(p.get("confidence", 0.0)) * 100)
            return {
                "threat_type": "PHISHING",
                "risk_score": score,
                "reasoning": p.get("ai_reasoning", "Phishing analysis complete."),
                "raw": p,
            }

        # Treat auth/user activity as behavioral analytics input
        features = [
            [
                float(payload.get("action_count", 1)),
                float(payload.get("hour_of_day", 12)),
                float(payload.get("data_volume_mb", payload.get("duration", 1))),
            ]
        ]
        result = self._anomaly.predict(features)
        details = result["details"][0] if result.get("details") else {"is_anomaly": False, "confidence_score": 0}

        score = min(
            100,
            int(
                (float(details.get("confidence_score", 0.0)) * 70)
                + (25 if details.get("is_anomaly") else 0)
                + (15 if event.get("status", "").upper() == "FAILED" else 0)
            ),
        )
        return {
            "threat_type": "INSIDER_ANOMALY" if details.get("is_anomaly") else "BEHAVIOR",
            "risk_score": score,
            "reasoning": f"Behavior model risk={result.get('risk_level', 'LOW')} and anomaly={details.get('is_anomaly', False)}",
            "raw": result,
        }

    def _to_dt(self, value: str) -> datetime:
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(ZoneInfo("UTC"))


engine = TelemetryEngine()
