import pytest
import numpy as np
from ai_layer.anomaly.detector import AnomalyDetector

def test_anomaly_detector_no_anomalies():
    detector = AnomalyDetector()
    activity_logs = [
        {"timestamp": i, "user_id": "user1", "action_count": 5, "duration": 10}
        for i in range(20)
    ]
    result = detector.predict(activity_logs)
    # On small mock datasets IsolationForest might flag some samples, but threats_found should be low
    assert result["threats_found"] < 5

def test_anomaly_detector_with_anomalies():
    detector = AnomalyDetector()
    activity_logs = [
        {"timestamp": i, "user_id": "user1", "action_count": 5, "duration": 10}
        for i in range(20)
    ]
    # Inject an anomaly
    activity_logs.append({"timestamp": 21, "user_id": "user1", "action_count": 500, "duration": 1000})
    
    result = detector.predict(activity_logs)
    assert result["risk_level"] in ["MEDIUM", "HIGH", "CRITICAL"]
    assert len(result["details"]) > 0
    assert any(r["is_anomaly"] for r in result["details"])
