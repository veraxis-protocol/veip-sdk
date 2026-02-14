from typing import Dict
from .veip_types import Decision


class StateMachine:
    VALID_TRANSITIONS: Dict[str, list[str]] = {
        "PROPOSED": ["AUTHORIZED", "DENIED", "ESCALATED", "SUPERVISORY"],
        "AUTHORIZED": ["EXECUTED"],
        "SUPERVISORY": ["AUTHORIZED", "DENIED"],
    }

    @staticmethod
    def validate_transition(current: str, next_state: str):
        allowed = StateMachine.VALID_TRANSITIONS.get(current, [])
        if next_state not in allowed:
            raise ValueError(f"Invalid transition: {current} → {next_state}")
