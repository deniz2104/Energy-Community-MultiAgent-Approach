from enum import Enum

class AgentType(Enum):
    IDEAL = "ideal"
    ENTHUSIASTIC = "enthusiastic"
    NON_ENTHUSIASTIC = "non-enthusiastic"

    @classmethod
    def get_types(cls) -> list[str]:
        return [member.value for member in cls]