from __future__ import annotations

import json
from typing import Any, Dict, Tuple

from . import VEIP_SPEC_VERSION
from .authorize import classify
from .schema import validate_evidence_pack
from .veip_types import AuthorityEnvelope, ActionProposal, Decision


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def replay_validate(
    evidence_pack: Dict[str, Any],
    authority: AuthorityEnvelope,
    proposal: ActionProposal,
    *,
    validate_schema: bool = True,
) -> Tuple[bool, str]:
    """
    Deterministic replay validation for the VEIP Evidence Pack envelope.

    Checks:
      - optional schema validation
      - schema_version matches SDK bound version
      - decision.classification equals recomputed classify(authority, proposal)
      - action.action_type equals proposal.action_type
    """
    try:
        if validate_schema:
            validate_evidence_pack(evidence_pack)
    except Exception as e:
        return False, f"Schema validation failed: {e}"

    if evidence_pack.get("schema_version") != VEIP_SPEC_VERSION:
        return False, "schema_version mismatch"

    expected: Decision = classify(authority, proposal)

    decision_obj = evidence_pack.get("decision", {})
    if decision_obj.get("classification") != expected.value:
        return False, "Decision classification mismatch on replay"

    action_obj = evidence_pack.get("action", {})
    if action_obj.get("action_type") != proposal.action_type:
        return False, "Action type mismatch on replay"

    return True, "OK"
