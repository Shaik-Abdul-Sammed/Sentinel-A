import pytest
from ai_layer.agent_orch.orchestrator import AgentOrchestrator

@pytest.mark.asyncio
async def test_agent_orchestrator_phishing():
    orchestrator = AgentOrchestrator()
    analysis_data = {"final_verdict": "SUSPICIOUS", "confidence": 0.9}
    suggestions = await orchestrator.get_mitigation_suggestions("PHISHING", analysis_data)
    assert len(suggestions["actions"]) > 0
    assert any("Block" in s["action"] for s in suggestions["actions"])

@pytest.mark.asyncio
async def test_agent_orchestrator_insider_threat():
    orchestrator = AgentOrchestrator()
    analysis_data = {"threats_found": 3, "risk_level": "HIGH"}
    suggestions = await orchestrator.get_mitigation_suggestions("INSIDER_THREAT", analysis_data)
    assert len(suggestions["actions"]) > 0
    assert any("Revoke" in s["action"] for s in suggestions["actions"])
