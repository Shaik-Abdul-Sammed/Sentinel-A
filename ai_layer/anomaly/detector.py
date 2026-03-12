import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from typing import List, Dict, Any

class AnomalyDetector:
    def __init__(self):
        # contamination is the expected proportion of outliers (threats)
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.is_trained = False

    def train_mock_model(self):
        """Pre-trains the model with baseline 'normal' behavior data."""
        # Normal behavior: low frequency, working hours, typical data volume
        # Features: [frequency, hour_of_day, data_volume_mb]
        n_samples = 100
        normal_data = np.random.normal(loc=[5, 12, 10], scale=[2, 4, 5], size=(n_samples, 3))
        
        # Anomalous behavior: high frequency, odd hours, high data volume
        anomaly_data = np.random.normal(loc=[100, 2, 1000], scale=[10, 1, 100], size=(5, 3))
        
        X = np.vstack([normal_data, anomaly_data])
        self.model.fit(X)
        self.is_trained = True

    def predict(self, activity_data: List[Any]) -> Dict[str, Any]:
        if not self.is_trained:
            self.train_mock_model()
        
        # Preprocess if data is a list of dicts
        X_processed = []
        if len(activity_data) > 0 and isinstance(activity_data[0], dict):
            for log in activity_data:
                # Features: [frequency (action_count), day_part (mocked), volume (duration)]
                X_processed.append([
                    float(log.get("action_count", 0)),
                    float(log.get("timestamp", 0) % 24), # Mock hour of day
                    float(log.get("duration", 0))
                ])
            X = np.array(X_processed)
        else:
            X = np.array(activity_data)
        
        predictions = self.model.predict(X) # 1 for normal, -1 for anomaly
        scores = self.model.decision_function(X) # Higher is more normal
        
        results = []
        for i, pred in enumerate(predictions):
            results.append({
                "is_anomaly": bool(pred == -1),
                "confidence_score": float(abs(scores[i])),
                "risk_level": "HIGH" if pred == -1 else "LOW"
            })
            
        return {
            "summary": f"Analyzed {len(results)} activity clusters.",
            "threats_found": sum(1 for r in results if r["is_anomaly"]),
            "risk_level": "CRITICAL" if any(r["risk_level"] == "CRITICAL" for r in results) else 
                          "HIGH" if any(r["risk_level"] == "HIGH" for r in results) else "LOW",
            "details": results
        }
