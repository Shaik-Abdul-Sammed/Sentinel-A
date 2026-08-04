from __future__ import annotations

import hashlib
import json
import math
import re
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List


def _parse_iso(value: str) -> datetime:
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_km * c


class AdvancedSecurityService:
    """Provides advanced defensive features beyond base detection pipeline."""

    def __init__(self) -> None:
        self.blocklist: set[str] = set()
        self.honeypot_paths = {"/admin/debug", "/internal/finance-dump", "/legacy-root-shell"}
        self.decoy_usernames = {"admin_test", "canary_user", "vault_probe"}
        self.decoy_password_tokens = {"CanaryToken#2026", "DoNotUse!Sentinel"}

        # Pattern-based triage gives instant root-cause hints from raw browser console logs.
        self.console_error_detectors = [
            {
                "error_type": "CORS_BLOCKED",
                "pattern": re.compile(r"blocked by CORS policy|No 'Access-Control-Allow-Origin'", re.IGNORECASE),
                "severity": "HIGH",
                "root_cause": "Frontend origin is not allowed by backend CORS response headers.",
                "fix": [
                    "Allow the exact frontend origin in backend CORS middleware.",
                    "Return Access-Control-Allow-Credentials only when required.",
                    "Avoid wildcard origin with credentialed requests.",
                ],
                "prevention": "Maintain per-environment origin allow-lists and validate with integration tests.",
            },
            {
                "error_type": "API_500",
                "pattern": re.compile(r"(?:GET|POST|PUT|DELETE)\s+\S+\s+500|status code 500|Internal Server Error", re.IGNORECASE),
                "severity": "CRITICAL",
                "root_cause": "Server-side exception during request processing.",
                "fix": [
                    "Inspect backend stack trace and failing dependency call.",
                    "Add request validation and fallback handling.",
                    "Add circuit-breaker/retry policy where upstream instability exists.",
                ],
                "prevention": "Add structured error telemetry and alert on rising 5xx rates.",
            },
            {
                "error_type": "HYDRATION_MISMATCH",
                "pattern": re.compile(r"hydration failed|does not match server-rendered HTML", re.IGNORECASE),
                "severity": "MEDIUM",
                "root_cause": "Server and client render different DOM or text output.",
                "fix": [
                    "Move browser-only logic into useEffect or client-only components.",
                    "Avoid non-deterministic rendering during SSR (Date.now/random).",
                    "Ensure locale/timezone formatting is consistent across server and client.",
                ],
                "prevention": "Enable SSR consistency checks in CI with deterministic test fixtures.",
            },
            {
                "error_type": "TYPE_ERROR_UNDEFINED",
                "pattern": re.compile(r"Cannot read properties of undefined|undefined is not an object", re.IGNORECASE),
                "severity": "HIGH",
                "root_cause": "Null/undefined access due to missing guards or invalid API response shape.",
                "fix": [
                    "Add optional chaining and response schema validation.",
                    "Guard render paths until data is loaded.",
                    "Introduce runtime type checks for external payloads.",
                ],
                "prevention": "Use strict TypeScript types and API contract tests.",
            },
            {
                "error_type": "CHUNK_LOAD_ERROR",
                "pattern": re.compile(r"ChunkLoadError|Loading chunk \d+ failed", re.IGNORECASE),
                "severity": "HIGH",
                "root_cause": "Client requested outdated or missing build artifact after deployment.",
                "fix": [
                    "Invalidate CDN/static cache after release.",
                    "Use atomic deploy strategy for app and assets.",
                    "Trigger soft reload when chunk mismatch is detected.",
                ],
                "prevention": "Deploy immutable versioned assets with cache busting.",
            },
            {
                "error_type": "WEBSOCKET_DISCONNECT",
                "pattern": re.compile(r"WebSocket.*(1006|closed before|failed)", re.IGNORECASE),
                "severity": "MEDIUM",
                "root_cause": "WebSocket tunnel dropped due to auth expiry, proxy policy, or network instability.",
                "fix": [
                    "Refresh access token before ws reconnect.",
                    "Verify proxy supports Upgrade and Connection headers.",
                    "Add exponential backoff and heartbeat timeouts.",
                ],
                "prevention": "Monitor ws close codes and automate reconnect telemetry.",
            },
            {
                "error_type": "TLS_CERT_INVALID",
                "pattern": re.compile(r"ERR_CERT_AUTHORITY_INVALID|SSL certificate", re.IGNORECASE),
                "severity": "HIGH",
                "root_cause": "Certificate chain is not trusted by the client.",
                "fix": [
                    "Install full certificate chain including intermediates.",
                    "Validate DNS and certificate SAN entries.",
                    "Rotate expired certificates and clear stale edge cache.",
                ],
                "prevention": "Use automated certificate renewal and expiry monitoring.",
            },
        ]

        self.console_scenario_library = [
            {
                "scenario_id": "api-cors-regression",
                "title": "SOC Dashboard API blocked by CORS after gateway change",
                "industry": "FinTech",
                "impact": "Analysts cannot load live alerts during an active phishing wave.",
                "logs": [
                    "Access to fetch at 'https://api.sentinel-a.io/telemetry/alerts' from origin 'https://soc.sentinel-a.io' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present.",
                    "GET https://api.sentinel-a.io/telemetry/alerts net::ERR_FAILED 200 (OK)",
                    "AxiosError: Network Error at getAlerts (api.ts:182)",
                ],
            },
            {
                "scenario_id": "frontend-release-chunk-failure",
                "title": "Production deployment serving stale JS chunks",
                "industry": "E-Commerce",
                "impact": "Users hit blank screens after release and cannot finish checkout.",
                "logs": [
                    "ChunkLoadError: Loading chunk 726 failed.",
                    "(error: https://portal.example.com/_next/static/chunks/726.71f6e.js)",
                    "Uncaught (in promise) ChunkLoadError: Loading chunk 726 failed.",
                ],
            },
            {
                "scenario_id": "token-expiry-ws-drop",
                "title": "WebSocket stream drops after token expiration",
                "industry": "Healthcare",
                "impact": "SOC loses real-time incident feed for several minutes.",
                "logs": [
                    "WebSocket connection to 'wss://soc.health-secure.ai/telemetry/ws?token=...' failed: WebSocket is closed before the connection is established.",
                    "WebSocket closed with code 1006",
                    "Error: failed to subscribe to telemetry stream",
                ],
            },
            {
                "scenario_id": "backend-500-on-login",
                "title": "Login API returns 500 because of DB pool exhaustion",
                "industry": "SaaS",
                "impact": "Authentication unavailable during business hours.",
                "logs": [
                    "POST https://api.example.net/auth/login 500 (Internal Server Error)",
                    "AxiosError: Request failed with status code 500",
                    "Unhandled Runtime Error: Authentication pipeline failed at /auth/login",
                ],
            },
            {
                "scenario_id": "react-hydration-fragment",
                "title": "Hydration mismatch caused by non-deterministic SSR timestamp",
                "industry": "GovTech",
                "impact": "Dashboard widgets flicker and user actions are delayed.",
                "logs": [
                    "Warning: Text content did not match. Server: '2026-04-17T10:21:08.341Z' Client: '2026-04-17T10:21:08.892Z'",
                    "Hydration failed because the initial UI does not match what was rendered on the server.",
                    "TypeError: Cannot read properties of undefined (reading 'risk_level') at DashboardCard (page.tsx:188)",
                ],
            },
        ]
        self.runtime_console_events: List[Dict[str, Any]] = []
        self.runtime_console_buffer_limit = 1000

    # Feature 1: Threat intel blocklist manager
    def add_indicator(self, indicator: str, source: str) -> Dict[str, Any]:
        normalized = indicator.strip().lower()
        self.blocklist.add(normalized)
        return {
            "indicator": normalized,
            "source": source,
            "status": "BLOCKLISTED",
            "total_indicators": len(self.blocklist),
        }

    # Feature 2: Blocklist lookup
    def lookup_indicator(self, indicator: str) -> Dict[str, Any]:
        normalized = indicator.strip().lower()
        return {
            "indicator": normalized,
            "is_blocklisted": normalized in self.blocklist,
            "total_indicators": len(self.blocklist),
        }

    # Feature 3: Blocklist remove
    def remove_indicator(self, indicator: str) -> Dict[str, Any]:
        normalized = indicator.strip().lower()
        existed = normalized in self.blocklist
        if existed:
            self.blocklist.remove(normalized)
        return {
            "indicator": normalized,
            "removed": existed,
            "total_indicators": len(self.blocklist),
        }

    # Feature 4: Impossible travel detection
    def impossible_travel(self, last: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
        distance_km = _haversine_km(
            float(last["lat"]),
            float(last["lon"]),
            float(current["lat"]),
            float(current["lon"]),
        )
        delta_hours = max(
            0.001,
            (_parse_iso(current["timestamp"]) - _parse_iso(last["timestamp"])).total_seconds() / 3600,
        )
        speed_kmph = distance_km / delta_hours
        suspicious = speed_kmph > 900
        return {
            "distance_km": round(distance_km, 2),
            "delta_hours": round(delta_hours, 3),
            "speed_kmph": round(speed_kmph, 2),
            "is_impossible_travel": suspicious,
            "recommended_action": "FORCE_MFA" if suspicious else "ALLOW",
        }

    # Feature 5: Device trust and fingerprint drift
    def device_trust(self, known: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
        keys = ["os", "browser", "device_type", "asn", "country"]
        mismatches = [key for key in keys if str(known.get(key, "")).lower() != str(current.get(key, "")).lower()]
        trust_score = max(0, 100 - (len(mismatches) * 20))
        return {
            "trust_score": trust_score,
            "mismatches": mismatches,
            "status": "UNTRUSTED" if trust_score < 60 else "TRUSTED",
            "recommended_action": "STEP_UP_AUTH" if trust_score < 60 else "ALLOW",
        }

    # Feature 6: Honeypot tripwire
    def honeypot_tripwire(self, endpoint: str, actor_id: str, ip: str) -> Dict[str, Any]:
        touched = endpoint in self.honeypot_paths
        return {
            "endpoint": endpoint,
            "actor_id": actor_id,
            "ip": ip,
            "tripwire_triggered": touched,
            "severity": "CRITICAL" if touched else "LOW",
            "recommended_action": "ISOLATE_SESSION" if touched else "MONITOR",
        }

    # Feature 7: Decoy credential abuse detection
    def decoy_credential_check(self, username: str, password: str) -> Dict[str, Any]:
        tripped = username in self.decoy_usernames or password in self.decoy_password_tokens
        return {
            "username": username,
            "decoy_hit": tripped,
            "severity": "CRITICAL" if tripped else "LOW",
            "recommended_action": "LOCK_ACCOUNT_AND_ESCALATE" if tripped else "ALLOW",
        }

    # Feature 8: Adaptive throttling recommendation
    def adaptive_throttle(self, requests_per_minute: int, failed_ratio: float, risk_score: int) -> Dict[str, Any]:
        pressure = (requests_per_minute / 60) + (failed_ratio * 100) + risk_score
        if pressure >= 160:
            rpm_limit = 10
        elif pressure >= 120:
            rpm_limit = 20
        elif pressure >= 80:
            rpm_limit = 40
        else:
            rpm_limit = 80
        return {
            "pressure_score": round(pressure, 2),
            "recommended_rpm_limit": rpm_limit,
            "recommended_action": "THROTTLE" if rpm_limit <= 20 else "NORMAL_RATE",
        }

    # Feature 9: IOC extraction engine
    def extract_iocs(self, text: str) -> Dict[str, Any]:
        ip_re = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
        domain_re = r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b"
        url_re = r"https?://[^\s\"'<>]+"
        hash_re = r"\b[a-fA-F0-9]{32,64}\b"
        email_re = r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"

        iocs = {
            "ips": sorted(set(re.findall(ip_re, text))),
            "domains": sorted(set(re.findall(domain_re, text))),
            "urls": sorted(set(re.findall(url_re, text))),
            "hashes": sorted(set(re.findall(hash_re, text))),
            "emails": sorted(set(re.findall(email_re, text))),
        }
        ioc_count = sum(len(items) for items in iocs.values())
        return {"ioc_count": ioc_count, "iocs": iocs}

    # Feature 10: Campaign correlation and graph-like grouping
    def correlate_campaigns(self, alerts: List[Dict[str, Any]]) -> Dict[str, Any]:
        buckets: dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for alert in alerts:
            key = f"{alert.get('threat_type', 'UNKNOWN')}|{alert.get('source', 'unknown')}|{alert.get('decision', 'ALERT')}"
            buckets[key].append(alert)

        campaigns = []
        for key, items in buckets.items():
            threat_type, source, decision = key.split("|")
            campaigns.append(
                {
                    "campaign_id": hashlib.sha1(key.encode("utf-8")).hexdigest()[:12],
                    "threat_type": threat_type,
                    "source": source,
                    "decision": decision,
                    "events": len(items),
                    "actors": sorted({str(it.get("actor_id", "unknown")) for it in items}),
                }
            )
        campaigns.sort(key=lambda x: x["events"], reverse=True)
        return {"campaigns": campaigns, "total_campaigns": len(campaigns)}

    # Feature 11: Forensic evidence export package
    def forensic_bundle(self, incident_id: str, alerts: List[Dict[str, Any]], timeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        payload = {
            "incident_id": incident_id,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "alerts": alerts,
            "timeline": timeline,
        }
        serialized = json.dumps(payload, sort_keys=True)
        digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        return {
            "incident_id": incident_id,
            "sha256": digest,
            "record_count": len(alerts) + len(timeline),
            "bundle": payload,
        }

    # Feature 12: Automated incident playbook generator
    def generate_playbook(self, threat_type: str, risk_level: str) -> Dict[str, Any]:
        base = [
            "Validate alert context and asset criticality",
            "Contain affected identities/endpoints",
            "Preserve evidence and timeline",
        ]

        specific = {
            "PHISHING": [
                "Search and purge similar emails",
                "Block sender domain and URLs",
                "Reset impacted user credentials",
            ],
            "INSIDER_ANOMALY": [
                "Freeze privileged sessions",
                "Review data access trail",
                "Notify HR and compliance liaison",
            ],
            "MALWARE": [
                "Isolate endpoint from network",
                "Capture memory and process list",
                "Run targeted IOC hunt across fleet",
            ],
        }

        severity_tail = [
            "Escalate to incident commander",
            "Issue stakeholder update",
        ] if risk_level.upper() in {"HIGH", "CRITICAL"} else ["Continue enhanced monitoring"]

        steps = base + specific.get(threat_type.upper(), ["Run generic triage checklist"]) + severity_tail
        return {
            "threat_type": threat_type.upper(),
            "risk_level": risk_level.upper(),
            "steps": steps,
            "owner": "SOC",
            "eta_minutes": 30 if risk_level.upper() in {"HIGH", "CRITICAL"} else 90,
        }

    # Feature 13: Real-world browser console incident scenarios
    def get_console_scenarios(self) -> Dict[str, Any]:
        return {
            "scenarios": self.console_scenario_library,
            "total": len(self.console_scenario_library),
            "source": "real-world inspired incident playbooks",
        }

    # Feature 14: Console forensics and root-cause triage
    def analyze_console_logs(self, logs: List[str], scenario_id: str | None = None) -> Dict[str, Any]:
        findings: List[Dict[str, Any]] = []
        seen: set[str] = set()

        severity_score = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3,
            "CRITICAL": 4,
        }

        for line_number, line in enumerate(logs, start=1):
            for detector in self.console_error_detectors:
                if detector["pattern"].search(line):
                    key = f"{detector['error_type']}::{line.strip()}"
                    if key in seen:
                        continue
                    seen.add(key)
                    findings.append(
                        {
                            "error_type": detector["error_type"],
                            "severity": detector["severity"],
                            "line_number": line_number,
                            "log_excerpt": line,
                            "root_cause": detector["root_cause"],
                            "how_to_solve": detector["fix"],
                            "preventive_control": detector["prevention"],
                            "confidence": 0.93,
                        }
                    )

        findings.sort(key=lambda f: severity_score[f["severity"]], reverse=True)

        unknown_lines = [
            {"line_number": idx + 1, "log_excerpt": item}
            for idx, item in enumerate(logs)
            if all(not detector["pattern"].search(item) for detector in self.console_error_detectors)
        ]

        triage_priority = [
            {
                "order": i + 1,
                "error_type": finding["error_type"],
                "why_first": "High blast radius and likely customer-facing impact"
                if finding["severity"] in {"CRITICAL", "HIGH"}
                else "Can destabilize UX if unresolved",
            }
            for i, finding in enumerate(findings)
        ]

        return {
            "scenario_id": scenario_id,
            "summary": {
                "total_lines": len(logs),
                "detected_errors": len(findings),
                "unclassified_lines": len(unknown_lines),
                "overall_risk": findings[0]["severity"] if findings else "LOW",
            },
            "detected_errors": findings,
            "unknown_lines": unknown_lines,
            "triage_priority": triage_priority,
            "efficiency_advantage": {
                "auto_grouping": "Groups duplicated stack traces into one actionable issue",
                "root_cause_mapping": "Maps signatures to likely root cause and fix steps",
                "time_saved_estimate": "~40-70% faster first-pass triage vs manual console inspection",
            },
        }

    # Feature 15: Live runtime browser log ingestion (window.onerror, unhandledrejection)
    def ingest_runtime_console_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        message = str(payload.get("message", "")).strip()
        if not message:
            raise ValueError("message is required")

        event = {
            "event_id": hashlib.sha1(
                f"{datetime.now(timezone.utc).isoformat()}::{message}::{payload.get('source', 'runtime')}".encode("utf-8")
            ).hexdigest()[:16],
            "source": str(payload.get("source", "runtime")),
            "level": str(payload.get("level", "error")).lower(),
            "url": payload.get("url"),
            "stack": payload.get("stack"),
            "user_agent": payload.get("user_agent"),
            "message": message,
            "occurred_at": payload.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        }
        self.runtime_console_events.append(event)
        if len(self.runtime_console_events) > self.runtime_console_buffer_limit:
            self.runtime_console_events = self.runtime_console_events[-self.runtime_console_buffer_limit :]

        instant_analysis = self.analyze_console_logs(
            [self._runtime_event_to_line(event)], scenario_id="runtime-live"
        )
        return {
            "status": "ingested",
            "event": event,
            "instant_detected_errors": instant_analysis["detected_errors"],
        }

    def get_runtime_console_events(self, limit: int = 200) -> Dict[str, Any]:
        safe_limit = max(1, min(limit, 1000))
        items = self.runtime_console_events[-safe_limit:]
        return {
            "items": items,
            "total": len(self.runtime_console_events),
            "limit": safe_limit,
        }

    def clear_runtime_console_events(self) -> Dict[str, Any]:
        cleared = len(self.runtime_console_events)
        self.runtime_console_events = []
        return {
            "status": "cleared",
            "cleared": cleared,
        }

    def analyze_runtime_console_events(self, limit: int = 250) -> Dict[str, Any]:
        safe_limit = max(1, min(limit, 1000))
        selected = self.runtime_console_events[-safe_limit:]
        lines = [self._runtime_event_to_line(event) for event in selected]
        result = self.analyze_console_logs(lines, scenario_id="runtime-live")
        result["runtime_context"] = {
            "events_used": len(selected),
            "events_total": len(self.runtime_console_events),
        }
        return result

    def _runtime_event_to_line(self, event: Dict[str, Any]) -> str:
        parts = [
            f"[{event.get('level', 'error').upper()}]",
            str(event.get("message", "")),
        ]
        if event.get("url"):
            parts.append(f"url={event['url']}")
        if event.get("stack"):
            parts.append(f"stack={event['stack']}")
        return " | ".join(parts)


advanced_security = AdvancedSecurityService()
