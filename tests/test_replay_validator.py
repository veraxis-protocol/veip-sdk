from veip_sdk.authorize import classify
from veip_sdk.evidence import generate_evidence
from veip_sdk.replay import replay_validate
from veip_sdk.veip_types import AuthorityEnvelope, ActionProposal


def test_replay_ok():
    authority = AuthorityEnvelope(scope_id="SCOPE1", issuer="Issuer", permitted_actions=["TRANSFER"])
    proposal = ActionProposal(action_type="TRANSFER", payload={"amount": 10})
    decision = classify(authority, proposal)
    pack = generate_evidence(authority, proposal, decision, validate_schema=True)

    ok, reason = replay_validate(pack, authority, proposal, validate_schema=True)
    assert ok, reason


def test_replay_detects_tamper():
    authority = AuthorityEnvelope(scope_id="SCOPE1", issuer="Issuer", permitted_actions=["TRANSFER"])
    proposal = ActionProposal(action_type="TRANSFER", payload={"amount": 10})
    decision = classify(authority, proposal)
    pack = generate_evidence(authority, proposal, decision, validate_schema=True)

    pack["payload"]["payload"]["amount"] = 9999

    ok, reason = replay_validate(pack, authority, proposal, validate_schema=True)
    assert not ok
    assert "hash" in reason.lower() or "mismatch" in reason.lower()
