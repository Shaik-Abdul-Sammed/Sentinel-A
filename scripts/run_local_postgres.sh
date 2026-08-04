#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_ACTIVATE="$ROOT_DIR/.venv/bin/activate"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
DB_URL="postgresql+psycopg2://sentinel:sentinel@localhost:5432/sentinel_a"

if [[ ! -f "$VENV_ACTIVATE" ]]; then
  echo "Missing virtual environment at $VENV_ACTIVATE"
  echo "Create it first, then install backend dependencies."
  exit 1
fi

if ! command -v docker-compose >/dev/null 2>&1; then
  echo "docker-compose is required but not installed."
  exit 1
fi

# Stop any previous local backend started by this script pattern.
pkill -f "uvicorn backend.main:app --host 0.0.0.0 --port 8000" >/dev/null 2>&1 || true

if docker info >/dev/null 2>&1; then
  docker-compose -f "$ROOT_DIR/docker-compose.yml" up -d postgres
else
  echo "Docker daemon requires elevated privileges."
  sudo docker-compose -f "$ROOT_DIR/docker-compose.yml" up -d postgres
fi

source "$VENV_ACTIVATE"

# Wait until Postgres accepts TCP connections before applying migrations.
for attempt in $(seq 1 30); do
  if PYTHONPATH="$ROOT_DIR:$ROOT_DIR/backend" DATABASE_URL="$DB_URL" \
    "$VENV_PYTHON" -c "import os; from sqlalchemy import create_engine, text; engine=create_engine(os.environ['DATABASE_URL']); conn=engine.connect(); conn.execute(text('SELECT 1')); conn.close(); engine.dispose()" >/dev/null 2>&1; then
    break
  fi
  if [[ "$attempt" -eq 30 ]]; then
    echo "Postgres did not become ready in time."
    exit 1
  fi
  sleep 1
done

(
  cd "$ROOT_DIR/backend"
  PYTHONPATH="$ROOT_DIR:$ROOT_DIR/backend" DATABASE_URL="$DB_URL" alembic upgrade head
)

(
  cd "$ROOT_DIR"
  PYTHONPATH="$ROOT_DIR:$ROOT_DIR/backend" DATABASE_URL="$DB_URL" \
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
) &
BACKEND_PID=$!

cleanup() {
  if kill -0 "$BACKEND_PID" >/dev/null 2>&1; then
    kill "$BACKEND_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT INT TERM

cd "$ROOT_DIR/frontend"
npm run dev
