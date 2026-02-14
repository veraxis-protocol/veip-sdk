from veip_sdk.types import AuthorityEnvelope, ActionProposal
from veip_sdk.authorize import classify
from veip_sdk.evidence import generate_evidence
from veip_sdk.state_machine import StateMachine


def main():
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

    if decision.value == "ALLOW":
        StateMachine.validate_transition("PROPOSED", "AUTHORIZED")

    evidence = generate_evidence(authority, proposal, decision)

    print("Decision:", decision.value)
    print("Evidence Pack:")
    print(evidence)


if __name__ == "__main__":
    main()
