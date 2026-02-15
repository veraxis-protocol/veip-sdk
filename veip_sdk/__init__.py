from __future__ import annotations

__version__ = "0.1.0"

# The VEIP specification version this SDK is aligned to.
VEIP_SPEC_VERSION = "0.1.0"

# SHA-256 of the vendored canonical schema file:
# veip_sdk/schemas/veip-evidence-pack.schema.json
VEIP_SCHEMA_SHA256 = "3ff025de2c91737e84aceae529e2da78a86622a26f7f5998b73ed880c15ebbf0"


def assert_spec_binding() -> None:
    """
    Enforce that:

      1) The vendored schema hash matches the pinned VEIP_SCHEMA_SHA256.
      2) If the schema constrains veip_version via const/enum,
         it matches VEIP_SPEC_VERSION.

    This prevents silent drift between:
      - veip-spec canonical schema
      - veip-sdk reference implementation
    """
    from .schema import (
        load_evidence_pack_schema,
        schema_sha256,
        infer_veip_version_from_schema,
    )

    actual_hash = schema_sha256()

    if actual_hash != VEIP_SCHEMA_SHA256:
        raise RuntimeError(
            f"Schema binding failed: expected {VEIP_SCHEMA_SHA256}, "
            f"got {actual_hash}. "
            "Sync schema from veip-spec and update the pinned hash."
        )

    schema = load_evidence_pack_schema()
    ok, inferred = infer_veip_version_from_schema(schema)

    if ok and inferred != VEIP_SPEC_VERSION:
        raise RuntimeError(
            f"Version binding failed: schema expects "
            f"veip_version={inferred} but SDK uses {VEIP_SPEC_VERSION}"
        )
