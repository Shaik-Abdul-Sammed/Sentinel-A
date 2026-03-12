import sys
import os
import pytest
from ai_layer.phishing.detector import PhishingDetector

@pytest.mark.asyncio
async def test_phishing_detector_suspicious():
    detector = PhishingDetector()
    url = "http://suspicious-bank-login.com"
    result = await detector.analyze(url)
    assert result["final_verdict"] == "SUSPICIOUS"
    assert result["confidence"] > 0.8

@pytest.mark.asyncio
async def test_phishing_detector_safe():
    detector = PhishingDetector()
    url = "https://google.com"
    result = await detector.analyze(url)
    assert result["final_verdict"] == "SAFE"
    assert result["confidence"] > 0.8
