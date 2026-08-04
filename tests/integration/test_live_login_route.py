import pytest


@pytest.mark.asyncio
async def test_live_login_route_returns_token(async_client):
    response = await async_client.post("/auth/live-login", data={"username": "soc", "password": "soc2026"})
    assert response.status_code == 200
    assert "access_token" in response.json()
