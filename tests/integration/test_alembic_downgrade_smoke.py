import os
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("alembic")


def test_alembic_downgrade_smoke(tmp_path):
    repo_root = Path(__file__).resolve().parents[2]
    backend_dir = repo_root / "backend"
    db_path = tmp_path / "downgrade_smoke.sqlite"
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{db_path}"
    env["PYTHONPATH"] = os.pathsep.join([str(repo_root), str(backend_dir), env.get("PYTHONPATH", "")]).rstrip(os.pathsep)

    upgrade = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(backend_dir / "alembic.ini"), "upgrade", "head"],
        cwd=str(backend_dir),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert upgrade.returncode == 0, upgrade.stderr

    downgrade = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(backend_dir / "alembic.ini"), "downgrade", "base"],
        cwd=str(backend_dir),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert downgrade.returncode == 0, downgrade.stderr
