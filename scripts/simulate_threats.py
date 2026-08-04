import requests
import json
import time

BASE_URL = "http://localhost:8000"


def get_soc_headers():
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": "soc", "password": "soc2026"},
        timeout=15,
    )
    response.raise_for_status()
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def simulate_phishing():
    print("--- Simulating Phishing Attack ---")
    response = requests.post(f"{BASE_URL}/telemetry/simulate/phishing", headers=get_soc_headers(), timeout=15)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))

def simulate_insider_threat():
    print("\n--- Simulating Insider Threat ---")
    response = requests.post(f"{BASE_URL}/telemetry/simulate/insider", headers=get_soc_headers(), timeout=15)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))


def print_snapshot():
    print("\n--- Sentinel-A Snapshot ---")
    status = requests.get(f"{BASE_URL}/telemetry/status", timeout=15)
    alerts = requests.get(f"{BASE_URL}/telemetry/alerts?limit=5", headers=get_soc_headers(), timeout=15)
    status.raise_for_status()
    alerts.raise_for_status()
    print("Status:")
    print(json.dumps(status.json(), indent=2))
    print("Recent Alerts:")
    print(json.dumps(alerts.json(), indent=2))

if __name__ == "__main__":
    print("Sentinel-A Simulation Engine Starting...")
    time.sleep(1)
    simulate_phishing()
    time.sleep(2)
    simulate_insider_threat()
    time.sleep(1)
    print_snapshot()
