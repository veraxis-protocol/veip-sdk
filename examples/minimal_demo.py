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
    )

    ok, reason = replay_validate(
        evidence_pack=evidence_pack,
        authority=authority,
        proposal=proposal,
        validate_schema=True,
    )

    print("Decision:", decision.value)
    print("Replay:", ok, reason)
    print("Evidence Pack:")
    print(evidence_pack)


if __name__ == "__main__":
    main()
