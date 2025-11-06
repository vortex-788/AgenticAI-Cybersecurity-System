from dataclasses import dataclass
from typing import Dict,Any
import time, uuid
ALLOWED_ACTIONS = {"NOOP":"tagged_for_analysis","CREATE_INCIDENT":"ticket_created","BLOCK_IP_TEMP":"applied","ISOLATE_HOST_REQUEST":"requested_human","COLLECT_FOR_ANALYSIS":"collection_scheduled"}
@dataclass
class EnrichedAlert:
    alert: Dict[str,Any]
    whois: Dict[str,Any]
    passive_dns: Dict[str,Any]
    host_info: Dict[str,Any]
    mitre: Dict[str,Any]
    score: float
    rationale: str
def mock_enrich(alert: Dict[str,Any]) -> Dict[str,Any]:
    obs = alert.get("observables", {})
    whois = {"asn":"AS13335","country":"US"} if obs.get("ip",""
).startswith("192") else {"asn":"AS-UNKNOWN","country":"Unknown"}
    passive_dns = {"related_domains": [obs.get("domain","")+"-c2.example"]} if obs.get("domain") else {}
    host = obs.get("hostname","unknown")
    host_info = {"hostname":host, "owner":("finance-app-team" if "finance" in host or "bank" in host else "unknown"), "role":("db-server" if "db" in host else "user-workstation")}
    mitre = {"technique":None, "tactic":None}
    cmd = obs.get("cmdline",""
).lower()
    if "encrypt" in cmd or "ransom" in cmd or obs.get("filehash",""
).endswith("deadbeef"):
        mitre = {"technique":"T1486","tactic":"Impact"}
    elif obs.get("port") == 22 and "ssh" in obs.get("process",""):
        mitre = {"technique":"T1021","tactic":"Lateral Movement"}
    elif "curl" in cmd or "wget" in cmd:
        mitre = {"technique":"T1071","tactic":"Command and Control"}
    return {"whois":whois, "passive_dns":passive_dns, "host_info":host_info, "mitre":mitre}

def compute_score(enrichment: Dict[str,Any], alert: Dict[str,Any]) -> float:
    score = 0.0
    mitre = enrichment.get("mitre", {})
    obs = alert.get("observables", {})
    if mitre.get("tactic") == "Impact":
        score += 0.7
    if mitre.get("technique") == "T1486":
        score += 0.2
    cmd = obs.get("cmdline",""
                  ).lower()
    if "curl" in cmd or "wget" in cmd:
        score += 0.15
    if obs.get("filehash",""
              ).endswith("deadbeef"):
        score += 0.2
    ip = obs.get("ip","")
    if ip.startswith("10.") or ip.startswith("192.168."):
        score += 0.05
    return min(1.0, score)

def decide_action(enriched: EnrichedAlert) -> Dict[str,Any]:
    score = enriched.score
    mitre = enriched.mitre
    host_role = enriched.host_info.get("role", "unknown")
    action = "NOOP"
    reasons = []
    if score >= 0.95:
        if mitre.get("technique") in ("T1071","T1021","T1486"):
            action = "BLOCK_IP_TEMP"
            reasons.append("score >= 0.95 and suspicious technique")
    elif score >= 0.7:
        action = "CREATE_INCIDENT"
        reasons.append("score >= 0.7 -> create incident")
        if mitre.get("tactic") == "Impact":
            reasons.append("Impact tactic -> request isolation")
            if host_role != "db-server":
                action = "ISOLATE_HOST_REQUEST"
    elif score >= 0.4:
        action = "COLLECT_FOR_ANALYSIS"
        reasons.append("score between 0.4 and 0.7 -> collect artifacts")
    else:
        action = "NOOP"
        reasons.append("low score -> tag for observation")
    rationale = "; ".join(reasons) if reasons else "no rationale"
    return {"action":action, "rationale":rationale, "score":score}

def execute_action(decision: Dict[str,Any], enriched: EnrichedAlert) -> Dict[str,Any]:
    action = decision.get("action")
    entry = {"event_id": enriched.alert.get("id"), "timestamp": time.time(), "action": action, "score": decision.get("score"), "rationale": decision.get("rationale"), "observable": enriched.alert.get("observables"), "mitre": enriched.mitre, "host": enriched.host_info}
    if action == "BLOCK_IP_TEMP":
        entry.update({"firewall_rule_id": "fw-"+uuid.uuid4().hex[:8], "ttl_seconds":3600, "status":"applied"})
    elif action == "ISOLATE_HOST_REQUEST":
        entry.update({"status":"requested_human"})
    elif action == "CREATE_INCIDENT":
        entry.update({"ticket_id":"INC-"+uuid.uuid4().hex[:6].upper(), "status":"ticket_created"})
    elif action == "COLLECT_FOR_ANALYSIS":
        entry.update({"collection_job_id":"COL-"+uuid.uuid4().hex[:6].upper(), "status":"collection_scheduled"})
    else:
        entry.update({"status":"tagged_for_analysis"})
    return entry
