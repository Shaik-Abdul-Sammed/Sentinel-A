import pytest


@pytest.mark.asyncio
async def test_blocklist_add_and_lookup(async_client):
    login = await async_client.post("/auth/login", data={"username": "soc", "password": "soc2026"})
    token = login.json()["access_token"]
    add_response = await async_client.post(
        "/advanced/threat-intel/blocklist/add",
        json={"indicator": "malicious.example", "source": "feed"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert add_response.status_code == 200
    lookup_response = await async_client.post(
        "/advanced/threat-intel/blocklist/lookup",
        json={"indicator": "malicious.example", "source": "feed"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert lookup_response.status_code == 200
    assert lookup_response.json()["is_blocklisted"] is True
