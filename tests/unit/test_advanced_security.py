from backend.app.services.advanced_security import advanced_security


def test_blocklist_add_lookup_and_remove():
    added = advanced_security.add_indicator("bad.example", "intel-feed")
    assert added["status"] == "BLOCKLISTED"
    lookup = advanced_security.lookup_indicator("bad.example")
    assert lookup["is_blocklisted"] is True
    removed = advanced_security.remove_indicator("bad.example")
    assert removed["removed"] is True


def test_extract_iocs_finds_values():
    findings = advanced_security.extract_iocs("Contact a@b.com from http://evil.test using 10.0.0.1 and hash abcdef1234567890abcdef1234567890")
    assert findings["ioc_count"] >= 3


def test_generate_playbook_high_risk():
    playbook = advanced_security.generate_playbook("phishing", "HIGH")
    assert playbook["owner"] == "SOC"
    assert len(playbook["steps"]) >= 4
