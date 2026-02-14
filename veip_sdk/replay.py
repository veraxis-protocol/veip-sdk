from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Tuple

from .authorize import classify
from .schema import validate_evidence_pack
from .veip_types import AuthorityEnvelope, ActionProposal, Decision
from . import VEIP_SPEC_VERSION


def _canonical_json(obj: Dict[str, Any]) -> str:
    # Stable canonicalization: keys sorted, compact separators, UTF-8 stable.
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def replay_validate(
    evidence_pack: Dict[str, Any],
    authority: AuthorityEnvelope,
    proposal: ActionProposal,
    *,
    validate_schema: bool = True
) -> Tuple[bool, str]:
    """
    Deterministic replay validator.

    Verifies:
      - schema validity (optional)
      - veip_version matches this SDK's bound spec version
      - decision recomputes deterministically from AuthorityEnvelope + ActionProposal
      - payload_hash recomputes deterministically from embedded payload

    Returns (ok, reason).
    """
    try:
        if validate_schema:
            validate_evidence_pack(evidence_pack)
    except Exception as e:
        return False, f"Schema validation failed: {e}"

    if evidence_pack.get("veip_version") != VEIP_SPEC_VERSION:
        return False, "VEIP version mismatch"

    expected_decision: Decision = classify(authority, proposal)
    if evidence_pack.get("decision") != expected_decision.value:
        return False, "Decision mismatch on replay"

    payload = evidence_pack.get("payload")
    if not isinstance(payload, dict):
        return False, "Missing/invalid payload object"

    serialized = _canonical_json(payload)
    expected_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    if evidence_pack.get("payload_hash") != expected_hash:
        return False, "Payload hash mismatch on replay"

    return True, "OK"
