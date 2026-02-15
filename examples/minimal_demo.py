# examples/minimal_demo.py

from veip_sdk.veip_types import AuthorityEnvelope, ActionProposal
from veip_sdk.authorize import classify
from veip_sdk.evidence import generate_evidence
from veip_sdk.replay import replay_validate


def main() -> None:
    authority = AuthorityEnvelope(
        scope_id="AML_SCOPE_001",
        issuer="ComplianceOffice",
        permitted_actions=["TRANSFER"],
        valid=True,
    )

    proposal = ActionProposal(
        action_type="TRANSFER",
        payload={"amount": 5000, "currency": "USD"},
    )

    decision = classify(authority, proposal)

    evidence_pack = generate_evidence(
        authority=authority,
        proposal=proposal,
        decision=decision,
        validate_schema=True,
        # Must be >= 7 chars per veip-spec schema
        commit="localdev",
        environment="local",
    )

    ok, reason = replay_validate(
        evidence_pack=evidence_pack,
        authority=authority,
        proposal=proposal,
        validate_schema=True,
    )

    print("Decision:", decision.value)
    print("Replay:", ok, reason)
    print("Evidence Pack keys:", list(evidence_pack.keys()))
    print("Evidence ID:", evidence_pack.get("evidence_id"))


if __name__ == "__main__":
    main()
