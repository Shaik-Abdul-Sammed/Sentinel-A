import pytest
from fastapi import HTTPException

from backend.app.api.auth import FAKE_USERS_DB, get_current_user, require_roles


@pytest.mark.asyncio
async def test_get_current_user_returns_admin():
    token_user = next(user for user in FAKE_USERS_DB.values() if user["username"] == "abdul")
    from backend.app.core import security

    token = security.create_access_token({"sub": token_user["username"], "role": token_user["role"]})
    user = await get_current_user(token)
    assert user["username"] == "abdul"
    assert user["role"] == "admin"


@pytest.mark.asyncio
async def test_require_roles_denies_wrong_role():
    checker = require_roles("soc")
    with pytest.raises(HTTPException):
        await checker({"username": "sensor", "role": "sensor"})
