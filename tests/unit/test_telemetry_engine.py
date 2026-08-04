import pytest

from backend.app.services.telemetry_engine import TelemetryEngine, TelemetryEvent


@pytest.mark.asyncio
async def test_ingest_phishing_event_creates_alert_shape():
    engine = TelemetryEngine()
    result = await engine.ingest(
        TelemetryEvent(
            source="portal",
            event_type="EMAIL",
            actor_id="u1",
            ip="1.1.1.1",
            endpoint="/mail",
            status="DELIVERED",
            payload={"content": "URGENT verify your account http://phish.test"},
            timestamp="2026-04-17T00:00:00+00:00",
        )
    )
    assert result["event"]["actor_id"] == "u1"
    assert result["alert"]["threat_type"] == "PHISHING"


def test_resolve_alert_returns_none_for_missing_id():
    engine = TelemetryEngine()
    assert engine.resolve_alert("missing") is None
