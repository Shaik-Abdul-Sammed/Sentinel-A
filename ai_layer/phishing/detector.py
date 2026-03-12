import re
from typing import Dict, Any

class PhishingDetector:
    def __init__(self):
        self.suspicious_keywords = ["urgent", "verify", "account", "suspended", "password", "bank", "login", "security"]
        self.suspicious_patterns = [
            r"bit\.ly", r"t\.co", r"tinyurl\.com",
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        ]

    def heuristic_analysis(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        keyword_matches = [word for word in self.suspicious_keywords if word in text_lower]
        url_matches = re.findall(r"http[s]?://\S+", text)
        
        score = len(keyword_matches) * 0.1
        if url_matches:
            score += 0.3
        
        return {
            "heuristic_score": min(score, 1.0),
            "keywords_found": keyword_matches,
            "urls_extracted": url_matches,
            "is_suspicious": score > 0.4
        }

    async def llm_analysis(self, text: str) -> Dict[str, Any]:
        # Placeholder for Google Gemini API integration
        # In a real implementation, we would call the Gemini API here
        return {
            "llm_confidence": 0.85,
            "reasoning": "Text uses urgent language typical of phishing, but requires domain verification.",
            "verdict": "SUSPICIOUS"
        }

    async def analyze(self, text: str) -> Dict[str, Any]:
        heuristic = self.heuristic_analysis(text)
        
        # If heuristics are ambiguous, escalate to LLM
        if heuristic["is_suspicious"]:
            llm_result = await self.llm_analysis(text)
            return {
                "final_verdict": llm_result["verdict"],
                "confidence": llm_result["llm_confidence"],
                "heuristic_data": heuristic,
                "ai_reasoning": llm_result["reasoning"]
            }
        
        return {
            "final_verdict": "SAFE",
            "confidence": 0.9,
            "heuristic_data": heuristic,
            "ai_reasoning": "Heuristics show no immediate threat patterns."
        }
