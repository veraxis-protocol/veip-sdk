from .types import AuthorityEnvelope, ActionProposal, Decision


def classify(authority: AuthorityEnvelope, proposal: ActionProposal) -> Decision:
    if not authority.valid:
        return Decision.DENY

    if proposal.action_type not in authority.permitted_actions:
        return Decision.ESCALATE

    return Decision.ALLOW
