import pytest
import httpx
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from backend.main import app


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


async def get_token(test_client: httpx.AsyncClient, username: str = "abdul", password: str = "sentinela2026") -> str:
    response = await test_client.post("/auth/login", data={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


def get_ws_token(test_client: TestClient, username: str = "abdul", password: str = "sentinela2026") -> str:
    response = test_client.post("/auth/login", data={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_read_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sentinel-A Shield is Online", "status": "active"}


@pytest.mark.asyncio
async def test_health_check(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_login_success(async_client):
    response = await async_client.post("/auth/login", data={"username": "abdul", "password": "sentinela2026"})
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_analyze_url_authorized(async_client):
    token = await get_token(async_client)
    response = await async_client.post(
        "/analyze/url",
        json={"url": "http://suspicious-bank-login.com"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["analysis"]["final_verdict"] == "SUSPICIOUS"


@pytest.mark.asyncio
async def test_analyze_behavior_authorized(async_client):
    token = await get_token(async_client)
    logs = [{"timestamp": 123456, "user_id": "test_user", "action_count": 500, "duration": 1000}]
    response = await async_client.post(
        "/analyze/behavior",
        json={"user_id": "test_user", "activity_logs": logs},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["analysis"]["risk_level"] in ["HIGH", "CRITICAL"]


def test_websocket_auth_success(client):
    token = get_ws_token(client, username="soc", password="soc2026")
    with client.websocket_connect(f"/telemetry/ws?token={token}") as websocket:
        payload = websocket.receive_json()
        assert payload["type"] == "telemetry.bootstrap"
        assert payload["viewer_role"] in {"soc", "admin"}


def test_websocket_auth_failure(client):
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/telemetry/ws") as websocket:
            websocket.receive_text()


@pytest.mark.asyncio
async def test_live_login_middleware_emits_telemetry(async_client):
    before = (await async_client.get("/telemetry/status")).json()["events_processed"]
    response = await async_client.post(
        "/auth/live-login",
        data={"username": "soc", "password": "soc2026"},
    )
    assert response.status_code == 200

    after = (await async_client.get("/telemetry/status")).json()["events_processed"]
    assert after == before + 1
