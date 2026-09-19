# Sentinel-AI: India’s AI Agent Cyber Shield

> **Built for National Innovation Hackathon 2026**  
> *An autonomous, agentic cyber-defense platform delivering real-time threat intelligence, behavioral anomaly detection, and automated mitigation across web and mobile endpoints.*

---

## 🛡️ About the Project

### The Challenge
Modern organizations, universities, and citizen-facing digital services face an escalating onslaught of sophisticated cyber threats—from credential harvesting and spear-phishing campaigns to insider privilege abuse and impossible geo-velocity logins. Traditional Security Information and Event Management (SIEM) systems and manual Security Operations Centers (SOCs) are overwhelmed by:
- **Alert Fatigue**: Thousands of unranked notifications per day.
- **Critical Latency**: Mean time to respond (MTTR) often stretches from hours to days.
- **Static Rule Fragility**: Signature-based IDS/IPS fail against novel attack vectors and polymorphic phishing.
- **Complex Deployment & High Cost**: Enterprise tools require extensive dedicated infrastructure and licensing.

### The Sentinel-A Solution
**Sentinel-A** is an autonomous, agent-orchestrated cyber shield engineered to detect, classify, and mitigate cyber attacks in sub-second timeframes. By integrating lightweight machine learning (Isolation Forests), heuristic and generative LLM reasoning (Google Gemini), and active push telemetry middleware, Sentinel-A turns passive logging into immediate, autonomous defense.

### Key Architectural Pillars
1. **Push-Ingestion Telemetry Pipeline**: Intercepts authentications and endpoint requests via middleware, streaming real-time event logs into the AI engine.
2. **Dual-Layer Detection Engine**:
   - *Heuristic + LLM Phishing Scanner*: Evaluates structural indicators, entropy, punycode, brand imitation, and contextual language patterns.
   - *Behavioral Insider Risk Engine*: Unsupervised Isolation Forest model detecting anomalies in user volume, anomalous login hours, and egress bursts.
3. **Advanced Threat Intelligence Pack**:
   - Indicator of Compromise (IOC) blocklist management and regex extraction.
   - Geo-velocity "Impossible Travel" physics detection.
   - Hardware / User-Agent device trust drift verification.
   - Honeypot decoy endpoints and tripwire credential abuse alarms.
   - Adaptive traffic throttling recommendations.
   - Forensic evidence bundle generation with cryptographic SHA-256 signatures.
   - Automated SOC incident response playbook generator.
4. **Autonomous Policy Orchestrator**: Automatically evaluates aggregate threat severity and executes graduated responses: `ALLOW`, `ALERT`, `ESCALATE`, or `BLOCK`.
5. **Cross-Platform Glassmorphic SOC Console**: Available as both a modern web app and a native mobile application bundled via **Capacitor**.

---

## ⚖️ Comparison with Existing Solutions

| Feature / Capability | Traditional SIEM (e.g. Splunk, QRadar) | Enterprise EDR/XDR (e.g. CrowdStrike, SentinelOne) | Traditional IDS/IPS (e.g. Snort, Suricata) | Darktrace (NDR) | **Sentinel-A (Cyber Shield)** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Autonomous Action Decision** | ❌ Mostly alerting; requires SOAR scripting | ⚠️ Endpoint-only containment; high configuration | ❌ Dropping rule matches only; no contextual logic | ⚠️ Autonomous network throttles | **✅ Native Agent Policy Engine (`ALLOW` / `ALERT` / `ESCALATE` / `BLOCK`)** |
| **Detection Approach** | Static rules & log correlation queries | Endpoint agent process hooks | Signature string/packet matching | Unsupervised network anomaly math | **Dual AI: Heuristics + Scikit-Learn Isolation Forest + LLM Reasoning** |
| **Phishing / Text Inspection** | ❌ External plugin required | ❌ Limited email/text inspection | ❌ Packet matching only | ❌ Metadata-focused | **✅ Built-in Deep Text/URL Heuristic & Generative AI Inspection** |
| **Insider Anomaly Detection** | ⚠️ Expensive UEBA add-ons | ⚠️ Focuses on malware binaries | ❌ Ineffective against valid credentials | ⚠️ Network-level only | **✅ Behavioral Anomaly Profiling (Action Count, Hour, Data Volume)** |
| **Push Telemetry Middleware** | ❌ Pull/Syslog collector forwarders | ❌ Heavy kernel/system agent | ❌ TAP / SPAN port sniffing | ❌ SPAN port monitoring | **✅ Lightweight Ingestion Middleware (`/auth/live-login` hooks)** |
| **Cross-Platform & Mobile App** | ⚠️ Desktop web consoles | ⚠️ Desktop management console | ❌ CLI / third-party GUI | ⚠️ Web portal | **✅ Responsive Web + Native Mobile App via Capacitor** |
| **Forensic Evidence Bundles** | Manual log exports | Proprietary agent telemetry | PCAP capture dumps | Proprietary packet logs | **✅ Cryptographic JSON Bundle with SHA-256 Digest Verification** |
| **Incident Playbook Generation**| Manual runbooks or expensive SOAR | Manual playbooks | ❌ None | ❌ None | **✅ Instant Automated Step-by-Step Playbook Generator** |
| **Resource Footprint** | Extremely heavy (Gigabytes of RAM) | Medium to heavy kernel footprint | Medium | Dedicated hardware appliances | **✅ Ultra-lightweight: Python FastAPI + Next.js + SQLite/Postgres** |

---

## 🗂️ Project Structure

```text
Sentinel-A/
├── .gitignore                      # Git ignore rules for Python, Node, and database files
├── docker-compose.yml              # Multi-container orchestration (FastAPI + Next.js + DB)
├── pytest.ini                      # Pytest runner configuration
├── README.md                       # Comprehensive platform documentation
│
├── ai_layer/                       # Core AI/ML Detection and Autonomous Orchestration
│   ├── __init__.py
│   ├── anomaly_detection/          # Behavioral insider threat & anomaly profiling
│   │   ├── __init__.py
│   │   └── detector.py             # Scikit-Learn Isolation Forest implementation
│   ├── orchestrator/               # Autonomous agent decision and mitigation engine
│   │   ├── __init__.py
│   │   └── policy_agent.py         # Multi-tier risk scoring and response policy
│   └── phishing_detection/         # Deep text and URL phishing inspection
│       ├── __init__.py
│       └── detector.py             # Heuristics (entropy, keywords) + Google Gemini API
│
├── backend/                        # High-Performance FastAPI Backend Service
│   ├── alembic.ini                 # Database migration configuration
│   ├── requirements.txt            # Python dependencies (FastAPI, SQLAlchemy, Scikit-Learn)
│   ├── main.py                     # Application entrypoint & middleware initialization
│   ├── alembic/                    # Database schema versions and migrations
│   │   ├── env.py
│   │   └── versions/
│   │       ├── 20260417_0001_create_telemetry_events_table.py
│   │       └── 20260417_0002_create_roles_and_users_tables.py
│   └── app/
│       ├── api/                    # Route controllers
│       │   ├── advanced.py         # Advanced security suite endpoints (IOC, Geo, Tripwire)
│       │   ├── auth.py             # JWT authentication, role verification, live-login
│       │   ├── telemetry.py        # Log ingestion, alert resolution, simulation endpoints
│       │   └── threats.py          # Threat scanning and evaluation APIs
│       ├── core/                   # Infrastructure utilities & middlewares
│       │   ├── advanced_security.py# Security algorithms (Geo-velocity, IOC regex, bundles)
│       │   ├── config.py           # Environment settings & credentials
│       │   ├── database.py         # SQLAlchemy engine and session makers
│       │   ├── security.py         # Password hashing & JWT token issuance
│       │   ├── telemetry_push_middleware.py # Push-ingestion middleware for auth traffic
│       │   └── ws_manager.py       # WebSocket connection manager for live dashboard feeds
│       └── models/                 # SQLAlchemy database schema models
│           ├── telemetry_event.py  # Events, alerts, and timeline database records
│           └── user.py             # User and role identity models
│
├── frontend/                       # Cross-Platform Web & Mobile Dashboard
│   ├── capacitor.config.ts         # Capacitor TypeScript app configuration
│   ├── capacitor.config.json       # Capacitor fallback JSON configuration
│   ├── next.config.ts              # Next.js configuration (Static HTML Export enabled)
│   ├── package.json                # Dependencies (@capacitor/core, React 19, Lucide, Tailwind)
│   ├── postcss.config.mjs          # PostCSS plugins
│   ├── tsconfig.json               # TypeScript compiler options
│   ├── public/                     # Static icons, favicons, and graphic assets
│   └── src/
│       ├── app/                    # Next.js App Router
│       │   ├── globals.css         # Cyber-defense dark/light styling and variables
│       │   ├── layout.tsx          # Root layout with offline-ready typography
│       │   ├── page.tsx            # Landing showcase & system readiness portal
│       │   ├── login/              # Secure SOC / Admin authentication portal
│       │   │   └── page.tsx
│       │   └── dashboard/          # SOC Operations Center
│       │       ├── page.tsx        # Overview: metrics, attack radar, live telemetry stream
│       │       ├── alerts/         # Alert triage & incident management
│       │       ├── forensics/      # Deep forensic log inspection & analysis
│       │       ├── scan/           # Interactive AI Threat Scanner
│       │       └── settings/       # Cyber shield parameters & Capacitor gateway config
│       ├── components/             # Reusable UI widgets
│       │   ├── dashboard/          # Header, Sidebar, StatCards, ThreatCharts
│       │   └── layout/             # DashboardShell (session guard), ThemeToggle
│       └── lib/                    # Client libraries
│           ├── api.ts              # Axios HTTP client, dynamic gateway base URL, WebSockets
│           └── utils.ts            # Formatting and Tailwind utility helpers
│
├── infrastructure/                 # Container and deployment specifications
│   ├── Dockerfile.backend          # Multi-stage Python 3.11 backend image
│   └── Dockerfile.frontend         # Node.js 20 production runner image
│
├── scripts/                        # Automation & Demonstration Utilities
│   └── simulate_threats.py         # Synthetic threat injection & demo scenario script
│
└── tests/                          # Automated Verification Suite (32 tests)
    ├── conftest.py                 # Pytest fixtures and mock databases
    ├── integration/                # End-to-end API and migration tests
    │   ├── test_advanced_api.py
    │   ├── test_alembic_smoke.py
    │   ├── test_api.py
    │   └── test_websocket_auth.py
    └── unit/                       # Component-level tests
        ├── test_advanced_security.py
        ├── test_auth_roles.py
        ├── test_security.py
        └── test_telemetry_engine.py
```

---

## 💻 Tech Stack

### 1. Frontend & Cross-Platform Mobile
- **Framework**: [Next.js 16](https://nextjs.org/) (App Router, Turbopack, Client Static Export)
- **UI Library**: [React 19](https://react.dev/)
- **Mobile Container**: [Capacitor 7](https://capacitorjs.com/) (Transforms Next.js static export into native Android & iOS apps)
- **Styling**: [Tailwind CSS 4](https://tailwindcss.com/) with custom cyber-theme glassmorphism
- **Motion & Icons**: [Framer Motion](https://www.framer.com/motion/) & [Lucide React](https://lucide.dev/)
- **Network / State**: [Axios](https://axios-http.com/) & Native WebSockets for real-time telemetry streaming

### 2. Backend & API Services
- **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance asynchronous Python API)
- **Server**: [Uvicorn](https://www.uvicorn.org/) (ASGI server)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/) & Pydantic-Settings
- **Middleware**: Custom `TelemetryPushMiddleware` for zero-latency event interception

### 3. Artificial Intelligence & Machine Learning
- **Behavioral Analytics**: [Scikit-Learn](https://scikit-learn.org/) (Unsupervised `IsolationForest` for anomaly scoring)
- **Generative AI Reasoning**: [Google Gemini API](https://ai.google.dev/) (`google-generativeai`) for natural-language contextual attack analysis
- **Heuristic Text Engine**: High-speed entropy scoring, domain levelling, and punycode detection

### 4. Database & Identity Management
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async-compatible session architecture)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) (Version-controlled schema evolution)
- **Storage**: SQLite (zero-config local demo) & PostgreSQL (production-ready)
- **Security**: OAuth2 with JWT (via `python-jose` with cryptography) and Passlib (`bcrypt`)

### 5. DevOps & Containerization
- **Containers**: Docker & Docker Compose
- **Testing**: Pytest, AnyIO, AsyncIO test runners

---

## 📋 System Requirements & Prerequisites

### Minimum Hardware
- **CPU**: 2 Cores (4 Cores recommended for local Docker build)
- **RAM**: 4 GB (8 GB recommended)
- **Disk Space**: 5 GB free disk space

### Software Requirements
- **Python**: Version `3.10` or `3.11`
- **Node.js**: Version `20.x` or `22.x` (LTS) & `npm` 10+
- **Docker**: Version `24.0+` & Docker Compose `v2.20+`
- **Capacitor Mobile Build (Optional for Android)**:
  - Android Studio Hedgehog / Iguana / Ladybug
  - Android SDK (API Level 33+)
  - Java Development Kit (JDK 17 or 21)

### Environment Variables
Configure a `.env` file in the root or `backend/` directory:
```bash
# Backend Security
SECRET_KEY=your-super-secret-key-32-chars-minimum
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
DATABASE_URL=sqlite:///./sentinel_a.db
# Or PostgreSQL: postgresql://sentinel_user:password@localhost:5432/sentinel_db

# Optional AI Key
GEMINI_API_KEY=AIzaSy...your-gemini-api-key

# Frontend (frontend/.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚀 Getting Started

### Method 1: Run with Docker Compose (Recommended for Demo)

The fastest way to launch the entire stack:
```bash
# Clone the repository
git clone https://github.com/Shaik-Abdul-Sammed/Sentinel-A.git
cd Sentinel-A

# Build and start all services
docker-compose up --build
```

Access the interfaces:
- **Web App / Console**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Method 2: Run Locally (Development Mode)

#### 1. Backend Setup
```bash
# Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start FastAPI development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Frontend Setup
In a new terminal window:
```bash
cd frontend

# Install Node dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

### Method 3: Run as a Mobile / Web App with Capacitor

Sentinel-A is fully configured as a progressive cross-platform web app powered by Capacitor.

#### 1. Compile Static Web Assets
```bash
cd frontend

# Build optimized static HTML/JS export into frontend/out/
npm run build
```

#### 2. Initialize and Sync Capacitor
```bash
# Add Android native project (requires Android SDK installed)
npm run cap:add:android

# Sync the compiled web assets into native platform assets
npm run cap:sync
```

#### 3. Launch on Android Emulator or Device
```bash
# Open native project directly in Android Studio
npm run cap:open:android
```
*Note*: When running on an Android emulator or device, open **Settings** inside the Sentinel-A app and set the **Backend API URL** to `http://10.0.2.2:8000` (for Android emulator) or your host machine's local IP address (`http://192.168.x.x:8000`).

---

## 🧪 Threat Simulation & Testing

### 1. Run Automated Threat Simulation
While the backend and frontend are running, open a terminal and execute:
```bash
python scripts/simulate_threats.py
```
This triggers real telemetry injections including:
- Phishing link submissions
- Insider credential abuse anomalies
- Impossible travel alerts
- Honeypot tripwire triggers

Observe the live dashboard counters, risk score shifts, and autonomous mitigation logs update in real time via WebSockets!

### 2. Run Test Suite
```bash
# Run all 32 unit and integration tests
.venv/bin/pytest
```

---

## 🔐 Demo Credentials & Roles

| Username | Password | Role | Description |
| :--- | :--- | :--- | :--- |
| `abdul` | `sentinela2026` | `admin` | Full administrative control, system settings, and policy overrides |
| `soc` | `soc2026` | `soc` | Security analyst role with alert triage, scanning, and forensics view |
| `sensor` | `sensor2026` | `sensor` | Dedicated service account for automated telemetry log ingestion |

---

## 👥 Authors & Acknowledgments

- **Lead Developer**: Abdul Sammed Shaik
- **Institution**: Rajiv Gandhi University of Knowledge Technologies (RGUKT RK Valley)
- **Event**: National Innovation Hackathon 2026
- **License**: MIT