import hashlib
import json
from typing import Dict, Any
from .veip_types import Decision, AuthorityEnvelope, ActionProposal


def generate_evidence(
    authority: AuthorityEnvelope,
    proposal: ActionProposal,
    decision: Decision
) -> Dict[str, Any]:

    payload = {
        "authority_scope": authority.scope_id,
        "issuer": authority.issuer,
        "action_type": proposal.action_type,
        "decision": decision.value,
        "payload": proposal.payload,
    }

    serialized = json.dumps(payload, sort_keys=True)
    payload_hash = hashlib.sha256(serialized.encode()).hexdigest()

    return {
        "veip_version": "0.1.0",
        "decision": decision.value,
        "payload_hash": payload_hash,
        "payload": payload,
    }
