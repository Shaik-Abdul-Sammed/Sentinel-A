import pytest
import httpx
from httpx import ASGITransport
from backend.main import app

@pytest.mark.asyncio
async def test_read_root():
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Sentinel-A Shield is Online", "status": "active"}

@pytest.mark.asyncio
async def test_health_check():
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_login_success():
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        response = await client.post(
            "/auth/login",
            data={"username": "abdul", "password": "sentinela2026"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_analyze_url_authorized():
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        # Get token
        login_resp = await client.post(
            "/auth/login",
            data={"username": "abdul", "password": "sentinela2026"}
        )
        token = login_resp.json()["access_token"]
        
        # Analyze URL
        response = await client.post(
            "/analyze/url",
            json={"url": "http://suspicious-bank-login.com"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert "analysis" in response.json()
        assert response.json()["analysis"]["final_verdict"] == "SUSPICIOUS"

@pytest.mark.asyncio
async def test_analyze_behavior_authorized():
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
        # Get token
        login_resp = await client.post(
            "/auth/login",
            data={"username": "abdul", "password": "sentinela2026"}
        )
        token = login_resp.json()["access_token"]
        
        # Analyze Behavior
        logs = [
            {"timestamp": 123456, "user_id": "test_user", "action_count": 500, "duration": 1000}
        ]
        response = await client.post(
            "/analyze/behavior",
            json={"user_id": "test_user", "activity_logs": logs},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["analysis"]["risk_level"] in ["HIGH", "CRITICAL"]
