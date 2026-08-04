# Sentinel-AI: India’s AI Agent Cyber Shield

Built for National Innovation Hackathon 2026.

## 🛡️ Overview
Sentinel-A is an autonomous cyber-defense platform designed to detect and mitigate modern threats using AI agents.

## 🚀 Key Features
- **AI Phishing Detector**: Heuristic + LLM (Gemini) analysis for deep text inspection.
- **Insider Risk Engine**: Behavioral analytics using Scikit-Learn to catch anomalies.
- **Autonomous Agents**: Self-orchestrating agents that suggest and execute mitigation steps.
- **Cyber-Themed UI**: Modern dashboard with real-time threat maps and glassmorphism.

## 🆕 Advanced Unique Features (New)

Sentinel-A now includes an additional advanced feature pack under `/advanced` with unique capabilities beyond the core phishing + anomaly pipeline:

1. **Threat Intel Blocklist Add**: Register malicious domains/IP indicators.
2. **Threat Intel Blocklist Lookup**: Check indicator reputation quickly.
3. **Threat Intel Blocklist Remove**: De-list indicators safely.
4. **Impossible Travel Detection**: Detect geo-velocity login anomalies.
5. **Device Trust Drift Check**: Compare known vs current fingerprint and score trust.
6. **Honeypot Tripwire Detection**: Trigger critical alerts on decoy endpoint access.
7. **Decoy Credential Abuse Detection**: Catch canary credential usage attempts.
8. **Adaptive Throttle Recommendation**: Dynamic rate-limit policy from pressure score.
9. **IOC Extraction Engine**: Extract IPs, domains, URLs, hashes, and emails from text.
10. **Campaign Correlation Engine**: Cluster incidents into campaigns by behavior signature.
11. **Forensic Evidence Bundle Export**: Export signed incident package with SHA256 digest.
12. **Automated Incident Playbook Generator**: Build SOC response steps from threat + severity.

## 🛠️ Tech Stack
- **Frontend**: Next.js 15, Tailwind CSS, Framer Motion, Lucide React.
- **Backend**: FastAPI, Python 3.11, JWT Security.
- **AI/ML**: Scikit-Learn (Isolation Forest), Google Gemini API (Placeholder).
- **Deployment**: Docker, Docker Compose.

## 📦 Getting Started

### 1. Prerequisites
- Docker & Docker Compose
- Google Gemini API Key (Optional)

### 2. Run with Docker
```bash
docker-compose up --build
```

Backend container now runs `alembic upgrade head` before API startup.

### 3. Access the Platform
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`

## 👥 Team Codeverses
- **Lead**: Abdul Sammed Shaik
- **Institution**: RGUKT RK Valley

## 🌐 Real-World Integration Architecture (Hackathon-Ready)

Sentinel-A can be integrated with a real login portal (citizen service, university ERP, or government form site) by adding telemetry hooks in the web app and API gateway. The website sends structured security events (login attempts, suspicious URL submissions, high-volume exports, failed auth bursts) to Sentinel-A's telemetry ingestion API. FastAPI runs the detection pipeline: phishing detector for text/URL content, anomaly detector for behavior patterns, and an orchestration policy agent that produces decisions (`ALLOW`, `ALERT`, `ESCALATE`, `BLOCK`). The frontend dashboard polls live APIs for alerts, system status, and timeline entries so you can show detection -> response -> escalation in real time.

### Proposed Production-Like Flow
1. User interacts with live website (`/login`, `/api/payroll/export`, `/inbox`).
2. Website sends event logs to `POST /telemetry/logs`.
3. Sentinel-A detection pipeline computes risk score.
4. Orchestrator decides action and stores alert/timeline event.
5. Dashboard reads `GET /telemetry/status`, `GET /telemetry/alerts`, `GET /telemetry/timeline`.
6. SOC/admin sees incident and response decisions instantly.

## 🔌 Key API Endpoints for Demo

### Telemetry Ingestion
- `POST /telemetry/logs` - ingest one security event (role: `sensor` or `admin`).
- `POST /telemetry/logs/batch` - ingest bulk events (role: `sensor` or `admin`).
- `POST /auth/live-login` - live login endpoint monitored by push-ingestion middleware.

### Detection + Orchestration
- `POST /telemetry/phishing-scan` - direct phishing text/url scan.
- `POST /telemetry/simulate/phishing` - safe phishing simulation (role: `soc` or `admin`).
- `POST /telemetry/simulate/insider` - safe insider-behavior simulation (role: `soc` or `admin`).

### Advanced Security Pack
- `POST /advanced/threat-intel/blocklist/add`
- `GET /advanced/threat-intel/blocklist`
- `POST /advanced/threat-intel/blocklist/lookup`
- `DELETE /advanced/threat-intel/blocklist/{indicator}`
- `POST /advanced/geo/impossible-travel`
- `POST /advanced/device/trust-check`
- `POST /advanced/honeypot/tripwire`
- `POST /advanced/identity/decoy-credential-check`
- `POST /advanced/network/adaptive-throttle`
- `POST /advanced/ioc/extract`
- `POST /advanced/campaign/correlate`
- `POST /advanced/forensics/export`
- `POST /advanced/playbook/generate`

### Dashboard Data
- `GET /telemetry/status` - shield status + counters + average risk.
- `GET /telemetry/alerts?limit=25` - latest alerts with decisions (role: `soc` or `admin`).
- `GET /telemetry/timeline?limit=50` - detection/response timeline (role: `soc` or `admin`).
- `WS /telemetry/ws?token=<jwt>` - role-protected live push updates (role: `soc` or `admin`).

### SOC Action API
- `POST /telemetry/alerts/{alert_id}/resolve` - resolve alert (role: `soc` or `admin`).

### Demo Roles
- `abdul / sentinela2026` -> `admin`
- `sensor / sensor2026` -> `sensor` (telemetry ingestion)
- `soc / soc2026` -> `soc` (SOC operations)

## 🧠 Agent Orchestration Logic

Risk scoring and decisions are policy-driven:
- Score >= 85 -> `CRITICAL` -> `BLOCK`
- Score >= 65 -> `HIGH` -> `ESCALATE`
- Score >= 40 -> `MEDIUM` -> `ALERT`
- Score < 40 -> `LOW` -> `ALLOW`

Auto-response actions include source blocking, MFA enforcement, SOC escalation, and monitoring escalation.

## 🧪 End-to-End Demo Scenario

1. Start system with Docker.
2. Open dashboard and alerts screens.
3. Trigger phishing simulation.
4. Trigger insider simulation.
5. Show timeline updates and risk score changes.
6. Explain action policy (why one was blocked and one escalated).

### Demo Command
```bash
python scripts/simulate_threats.py
```

This script now triggers real telemetry API simulations and prints status + alerts snapshots.

## 🧩 Minimal Working Snippets

### 1) Log capture from a website (frontend/service)
```javascript
await fetch("http://localhost:8000/telemetry/logs", {
	method: "POST",
	headers: { "Content-Type": "application/json" },
	body: JSON.stringify({
		source: "citizen-portal",
		event_type: "AUTH",
		actor_id: "user_109",
		ip: "10.2.0.41",
		endpoint: "/login",
		status: "FAILED",
		payload: { action_count: 18, hour_of_day: 2, data_volume_mb: 2 },
	}),
})
```

### 2) Anomaly detection + risk build (backend)
```python
features = [[action_count, hour_of_day, data_volume_mb]]
result = anomaly_detector.predict(features)
is_anomaly = result["details"][0]["is_anomaly"]
score = min(100, int(confidence * 70 + (25 if is_anomaly else 0) + failed_auth_bonus))
```

### 3) Alert generation + auto-response (backend)
```python
decision = await orchestrator.decide_response(threat_type="INSIDER_ANOMALY", score=score, evidence=result)
alert = {
	"risk_level": decision["risk_level"],
	"decision": decision["decision"],
	"actions": decision["actions"],
}
```

## 🔒 Safe Attack Simulation Guidance

Use only synthetic data and internal localhost endpoints:
- Simulate phishing with fake URLs/domains only.
- Simulate insider anomaly with dummy users and fake payload sizes.
- Never scan external production targets.
- Keep tests isolated in local Docker network.

## 🐳 Local Deployment (Demo-Ready)

```bash
docker-compose up --build
```

Then open:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

For a strong presentation, keep one terminal running `python scripts/simulate_threats.py` while the dashboard is open to show live detections and autonomous decisions.

## 🧱 Database Migrations (Alembic)

Production-safe schema evolution is now managed with Alembic in `backend/alembic`.

Current revisions:
- `20260417_0001` creates telemetry events, alerts, and timeline tables.
- `20260417_0002` adds normalized `roles` and `users` tables for the future identity model.

### Run migrations locally
```bash
cd backend
alembic upgrade head
```

### Create a new migration
```bash
cd backend
alembic revision -m "add new security fields"
```

### Roll back one migration
```bash
cd backend
alembic downgrade -1
```

## 🔄 True Push Ingestion Middleware

Sentinel-A includes `TelemetryPushMiddleware` that captures real login attempts on `POST /auth/live-login` and pushes them directly into the telemetry pipeline (event ingestion + websocket broadcast) in real time.

Example request:
```bash
curl -X POST "http://localhost:8000/auth/live-login" \
	-H "Content-Type: application/x-www-form-urlencoded" \
	-d "username=soc&password=soc2026"
```