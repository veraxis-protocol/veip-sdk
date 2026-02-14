import pytest

from veip_sdk.schema import validate_evidence_pack
from veip_sdk.authorize import classify
from veip_sdk.evidence import generate_evidence
from veip_sdk.veip_types import AuthorityEnvelope, ActionProposal


def test_generated_pack_validates_schema():
    authority = AuthorityEnvelope(scope_id="SCOPE1", issuer="Issuer", permitted_actions=["TRANSFER"])
    proposal = ActionProposal(action_type="TRANSFER", payload={"amount": 1})
    decision = classify(authority, proposal)

    pack = generate_evidence(authority, proposal, decision, validate_schema=True)
    validate_evidence_pack(pack)  # should not raise


def test_invalid_pack_fails_schema():
    with pytest.raises(Exception):
        validate_evidence_pack({"not": "a pack"})
