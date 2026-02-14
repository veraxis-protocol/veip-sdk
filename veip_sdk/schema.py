from __future__ import annotations

import hashlib
import json
from importlib import resources
from typing import Any, Dict, Tuple

from jsonschema import Draft202012Validator


_SCHEMA_PACKAGE = "veip_sdk.schemas"
_SCHEMA_FILENAME = "veip-evidence-pack.schema.json"


def load_evidence_pack_schema() -> Dict[str, Any]:
    """
    Load the vendored VEIP Evidence Pack schema shipped with this SDK.
    """
    with resources.files(_SCHEMA_PACKAGE).joinpath(_SCHEMA_FILENAME).open("r", encoding="utf-8") as f:
        return json.load(f)


def schema_sha256() -> str:
    """
    Compute SHA-256 of the vendored schema file (bytes) for binding and provenance.
    """
    with resources.files(_SCHEMA_PACKAGE).joinpath(_SCHEMA_FILENAME).open("rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()


def infer_veip_version_from_schema(schema: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Attempt to infer the expected VEIP version string from schema constraints.
    Supports:
      - properties.veip_version.const
      - properties.veip_version.enum (single value)
    Returns (ok, version_or_reason).
    """
    props = schema.get("properties", {})
    vv = props.get("veip_version", {})
    if isinstance(vv, dict):
        if "const" in vv and isinstance(vv["const"], str):
            return True, vv["const"]
        if "enum" in vv and isinstance(vv["enum"], list) and len(vv["enum"]) == 1 and isinstance(vv["enum"][0], str):
            return True, vv["enum"][0]
    return False, "Schema does not constrain properties.veip_version via const/enum"


def validate_evidence_pack(evidence_pack: Dict[str, Any]) -> None:
    """
    Validate an Evidence Pack against the vendored JSON Schema.
    Raises jsonschema.ValidationError on failure.
    """
    schema = load_evidence_pack_schema()
    Draft202012Validator(schema).validate(evidence_pack)
