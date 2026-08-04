import pytest


@pytest.mark.asyncio
async def test_live_login_middleware_emits_telemetry_event(async_client):
    before = (await async_client.get("/telemetry/status")).json()["events_processed"]
    response = await async_client.post("/auth/live-login", data={"username": "soc", "password": "soc2026"})
    assert response.status_code == 200
    after = (await async_client.get("/telemetry/status")).json()["events_processed"]
    assert after == before + 1
