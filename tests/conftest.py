import os
import sys
from pathlib import Path

import httpx
import pytest_asyncio
from httpx import ASGITransport

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
TEST_DB = ROOT / ".sentinel_test.sqlite"

if TEST_DB.exists():
    TEST_DB.unlink()

for path in (ROOT, BACKEND):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

os.environ.setdefault("DATABASE_URL", f"sqlite:///{TEST_DB}")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from app.core.database import Base, engine  # noqa: E402
from app.models import identity, telemetry  # noqa: F401,E402

Base.metadata.create_all(bind=engine)


@pytest_asyncio.fixture()
async def async_client():
    from backend.main import app  # noqa: E402

    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as test_client:
        yield test_client
