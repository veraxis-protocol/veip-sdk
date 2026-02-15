from __future__ import annotations

__version__ = "0.1.0"

# The VEIP spec version this SDK is bound to (reference implementation posture).
VEIP_SPEC_VERSION = "0.1.0"

# Schema binding: pin to the exact canonical schema bytes vendored from veip-spec.
VEIP_SCHEMA_SHA256 = "<PASTE_HASH_HERE>"



def assert_spec_binding() -> None:
    """
    Enforce that:
      - Vendored schema hash matches the pinned VEIP_SCHEMA_SHA256.
      - If the schema constrains veip_version via const/enum, it matches VEIP_SPEC_VERSION.
    """
    from .schema import load_evidence_pack_schema, schema_sha256, infer_veip_version_from_schema

    actual_hash = schema_sha256()
    if VEIP_SCHEMA_SHA256 == "REPLACE_ME_AFTER_COPY":
        raise RuntimeError(
            "VEIP_SCHEMA_SHA256 not set. Compute it from vendored schema and update veip_sdk/__init__.py."
        )

    if actual_hash != VEIP_SCHEMA_SHA256:
        raise RuntimeError(
            f"Schema binding failed: expected {VEIP_SCHEMA_SHA256}, got {actual_hash}. "
            "Sync schema from veip-spec and update the pinned hash."
        )

    schema = load_evidence_pack_schema()
    ok, inferred = infer_veip_version_from_schema(schema)
    if ok and inferred != VEIP_SPEC_VERSION:
        raise RuntimeError(
            f"Version binding failed: schema expects veip_version={inferred} but SDK uses {VEIP_SPEC_VERSION}"
        )
