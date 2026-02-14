from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any


class Decision(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    ESCALATE = "ESCALATE"
    SUPERVISORY = "SUPERVISORY"


@dataclass(frozen=True)
class AuthorityEnvelope:
    scope_id: str
    issuer: str
    permitted_actions: list[str]
    valid: bool = True


@dataclass(frozen=True)
class ActionProposal:
    action_type: str
    payload: Dict[str, Any]
