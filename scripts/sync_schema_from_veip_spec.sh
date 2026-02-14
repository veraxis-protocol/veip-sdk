#!/usr/bin/env bash
set -euo pipefail

# Sync schema from a local checkout of veip-spec.
# Usage:
#   bash scripts/sync_schema_from_veip_spec.sh ../veip-spec

SPEC_REPO_PATH="${1:-}"
if [[ -z "$SPEC_REPO_PATH" ]]; then
  echo "Usage: $0 /path/to/local/veip-spec"
  exit 1
fi

SRC="$SPEC_REPO_PATH/schemas/veip-evidence-pack.schema.json"
DST="veip_sdk/schemas/veip-evidence-pack.schema.json"

if [[ ! -f "$SRC" ]]; then
  echo "Source schema not found: $SRC"
  exit 1
fi

mkdir -p "$(dirname "$DST")"
cp "$SRC" "$DST"
echo "Copied $SRC -> $DST"
