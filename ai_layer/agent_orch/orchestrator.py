from typing import List, Dict, Any
import os

class AgentOrchestrator:
    def __init__(self):
        # In a real environment, this would initialize the Google Generative AI client
        self.api_key = os.getenv("GOOGLE_API_KEY", "MOCK_KEY_FOR_PROTOTYPE")

    async def get_mitigation_suggestions(self, threat_type: str, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Uses LLM context to suggest defensive actions.
        For the prototype, we provide logic-based suggestions that simulate AI reasoning.
        """
        suggestions = []
        
        if threat_type == "PHISHING":
            suggestions = [
                {"action": "Block URL", "description": "Add domain to organization-wide blocklist."},
                {"action": "Flag Email", "description": "Mark similar messages in all inboxes as phishing."},
                {"action": "Reset Password", "description": "Enforce password change for users who clicked the link."}
            ]
        elif threat_type == "INSIDER_THREAT":
            risk_level = threat_data.get("risk_level", "LOW")
            if risk_level == "HIGH":
                suggestions = [
                    {"action": "Revoke Access", "description": "Temporarily disable sensitive system access."},
                    {"action": "Enable Monitoring", "description": "Trigger full session recording for this user."},
                    {"action": "Audit Trail", "description": "Search for lateral movement in other internal services."}
                ]
            else:
                suggestions = [
                    {"action": "Verification", "description": "Send a push notification to verify the unusual activity."}
                ]
        
        return {
            "agent_verdict": f"The Sentinel-A Agent recommends {len(suggestions)} immediate actions.",
            "actions": suggestions,
            "reasoning": f"Based on {threat_type} analysis and organization security policy."
        }

    def get_risk_level(self, score: int) -> str:
        if score >= 85:
            return "CRITICAL"
        if score >= 65:
            return "HIGH"
        if score >= 40:
            return "MEDIUM"
        return "LOW"

    async def decide_response(self, threat_type: str, score: int, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Policy-first response engine for auto-response and escalation."""
        risk_level = self.get_risk_level(score)

        if score >= 85:
            decision = "BLOCK"
            actions = [
                "Block source IP/domain",
                "Disable impacted account session",
                "Escalate to SOC L2",
            ]
        elif score >= 65:
            decision = "ESCALATE"
            actions = [
                "Force MFA challenge",
                "Notify SOC analyst",
                "Increase monitoring window",
            ]
        elif score >= 40:
            decision = "ALERT"
            actions = [
                "Create alert ticket",
                "Monitor for repeated behavior",
            ]
        else:
            decision = "ALLOW"
            actions = ["Log event as informational"]

        title = f"{threat_type.replace('_', ' ').title()} - {risk_level}"
        return {
            "title": title,
            "risk_level": risk_level,
            "score": score,
            "decision": decision,
            "actions": actions,
            "evidence": evidence,
        }

    async def generate_threat_report(self, threat_summary: str) -> str:
        # Placeholder for Gemini generating a human-readable report
        return f"AI Generated Report: Sentinel-A has detected a potential {threat_summary}. No data exfiltration detected yet."
