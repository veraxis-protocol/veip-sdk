from __future__ import annotations

import hashlib
import json
import os
import uuid
from dataclasses import asdict, is_dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from . import VEIP_SPEC_VERSION, assert_spec_binding
from .schema import validate_evidence_pack
from .veip_types import Decision, AuthorityEnvelope, ActionProposal


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _to_plain(obj: Any) -> Any:
    if is_dataclass(obj):
        return asdict(obj)
    return obj


def generate_evidence(
    authority: AuthorityEnvelope,
    proposal: ActionProposal,
    decision: Decision,
    *,
    validate_schema: bool = True,
    reason_code: str = "RULE_MATCH",
    policy_id: str = "VEIP-Core",
    policy_version: str | None = None,
    policy_hash: str | None = None,
    constraints_ref: str = "constraints/VEIP-Core",
    context_refs: list[str] | None = None,
    executor: str = "veip-sdk",
    environment: str = "dev",
    commit: str = "local",
) -> Dict[str, Any]:
    """
    Emit a VEIP Evidence Pack compliant with veip-spec/schemas/veip-evidence-pack.schema.json.

    Notes:
      - This is a reference implementation; values like policy_id/constraints_ref/context_refs are
        defaults that should be supplied by integrators in real deployments.
    """
    assert_spec_binding()

    now = _utc_now_iso()

    # Defaults
    if policy_version is None:
        policy_version = VEIP_SPEC_VERSION

    if policy_hash is None:
        policy_hash = _sha256_hex(f"{policy_id}@{policy_version}")[:64]

    if context_refs is None:
        context_refs = ["context/example"]

    # Minimal deterministic action_id from proposal contents
    action_fingerprint = _canonical_json(
        {"action_type": proposal.action_type, "payload": _to_plain(proposal.payload)}
    )
    action_id = _sha256_hex(action_fingerprint)[:32]

    pack: Dict[str, Any] = {
        "schema_version": VEIP_SPEC_VERSION,
        "evidence_id": str(uuid.uuid4()),
        "created_at": now,
        "authority": {
            "scope_id": authority.scope_id,
            "issuer": authority.issuer,
            # schema requires these timestamps and a constraints_ref
            "valid_from": now,
            "valid_to": (datetime.now(timezone.utc) + timedelta(days=365)).isoformat(),
            "constraints_ref": constraints_ref,
        },
        "policy": {
            "policy_id": policy_id,
            "policy_version": policy_version,
            "policy_hash": policy_hash,
        },
        "action": {
            "action_id": action_id,
            "action_type": proposal.action_type,
            "proposed_at": now,
            "context_refs": context_refs,
        },
        "decision": {
            "classification": decision.value,
            "reason_code": reason_code,
            "evaluated_at": now,
        },
        "execution": {
            "executed": False,
            "executed_at": now,
            "executor": executor,
            "outcome": {
                "status": "SKIPPED",
                "result_ref": "result/none",
            },
            # "supervisory": {...} is optional in your schema
        },
        "provenance": {
            "system_id": os.getenv("VEIP_SYSTEM_ID", "veip-sdk-reference"),
            "build": {
                "version": VEIP_SPEC_VERSION,
                "commit": commit,
            },
            "environment": environment,
        },
    }

    if validate_schema:
        validate_evidence_pack(pack)

    return pack
