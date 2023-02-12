from dataclasses import dataclass
from typing import Dict


@dataclass
class ConditionDefinition:
    condition_type: str
    data: Dict
