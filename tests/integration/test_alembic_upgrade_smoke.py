import os
import subprocess
import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect

pytest.importorskip("alembic")


def test_alembic_upgrade_smoke(tmp_path):
    repo_root = Path(__file__).resolve().parents[2]
    backend_dir = repo_root / "backend"
    db_path = tmp_path / "upgrade_smoke.sqlite"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{db_path}"
    env["PYTHONPATH"] = os.pathsep.join([str(repo_root), str(backend_dir), env.get("PYTHONPATH", "")]).rstrip(os.pathsep)

    result = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(backend_dir / "alembic.ini"), "upgrade", "head"],
        cwd=str(backend_dir),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr

    engine = create_engine(f"sqlite:///{db_path}")
    tables = set(inspect(engine).get_table_names())
    assert {"telemetry_events", "alerts", "timeline", "roles", "users"}.issubset(tables)
