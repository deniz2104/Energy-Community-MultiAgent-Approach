from enum import Enum
import random
from typing import Literal

class AgentType(Enum):
    IDEAL = "ideal"
    ENTHUSIASTIC = "enthusiastic"
    NON_ENTHUSIASTIC = "non-enthusiastic"

    @classmethod
    def get_random_type(cls) -> Literal["ideal", "enthusiastic", "non-enthusiastic"]:
        return (random.choice(list(cls))).value