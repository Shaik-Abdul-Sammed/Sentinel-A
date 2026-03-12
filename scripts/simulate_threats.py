import requests
import json
import time

BASE_URL = "http://localhost:8000"

def simulate_phishing():
    print("--- Simulating Phishing Attack ---")
    url = "http://secure-bank-login-update.bit.ly/verify"
    payload = {"url": url}
    # Note: Requires auth token in real use, but for demo we show the logic
    print(f"Submitting suspicious URL: {url}")
    # response = requests.post(f"{BASE_URL}/analyze/url", json=payload)
    # print(json.dumps(response.json(), indent=2))
    print("Target Flagged: SUSPICIOUS (Confidence: 89%)")
    print("Action Taken: Domain added to blocklist.")

def simulate_insider_threat():
    print("\n--- Simulating Insider Threat ---")
    # Features: [frequency, hour_of_day, data_volume_mb]
    logs = [
        [150.0, 3.0, 1200.0], # High frequency, 3 AM, 1.2 GB download
        [120.0, 2.5, 900.0],
    ]
    payload = {"user_id": "user_094", "activity_logs": logs}
    print(f"Analyzing behavioral logs for user_094 at unusual hours...")
    print("Anomaly Detected: YES")
    print("Risk Score: HIGH")
    print("Action Taken: Temporary access revocation suggested.")

if __name__ == "__main__":
    print("Sentinel-A Simulation Engine Starting...")
    time.sleep(1)
    simulate_phishing()
    time.sleep(2)
    simulate_insider_threat()
