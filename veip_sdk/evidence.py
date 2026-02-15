import hashlib
import json
from typing import Dict, Any

from .schema import validate_evidence_pack
from .veip_types import Decision, AuthorityEnvelope, ActionProposal
from . import VEIP_SPEC_VERSION, assert_spec_binding


def _canonical_json(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def generate_evidence(
    authority: AuthorityEnvelope,
    proposal: ActionProposal,
    decision: Decision,
    *,
    validate_schema: bool = True
) -> Dict[str, Any]:
    # Ensure the SDK is bound to the correct canonical schema before emitting packs.
    assert_spec_binding()

    payload = {
        "authority_scope": authority.scope_id,
        "issuer": authority.issuer,
        "action_type": proposal.action_type,
        "decision": decision.value,
        "payload": proposal.payload,
    }

    serialized = _canonical_json(payload)
    payload_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    evidence_pack = {
        "veip_version": VEIP_SPEC_VERSION,
        "decision": decision.value,
        "payload_hash": payload_hash,
        "payload": payload,
    }

    if validate_schema:
        validate_evidence_pack(evidence_pack)

    return evidence_pack
