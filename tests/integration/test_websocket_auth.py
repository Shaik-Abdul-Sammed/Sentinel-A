import pytest
from starlette.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from backend.main import app


def test_websocket_auth_success_and_bootstrap():
    with TestClient(app) as client:
        token = client.post("/auth/login", data={"username": "soc", "password": "soc2026"}).json()["access_token"]
        with client.websocket_connect(f"/telemetry/ws?token={token}") as websocket:
            payload = websocket.receive_json()
            assert payload["type"] == "telemetry.bootstrap"


def test_websocket_auth_failure_without_token():
    with TestClient(app) as client:
        with pytest.raises(WebSocketDisconnect):
            with client.websocket_connect("/telemetry/ws"):
                pass
