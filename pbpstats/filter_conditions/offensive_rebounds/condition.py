from dataclasses import dataclass
from typing import Dict

from pbpstats.filter_conditions.compare import (
    ComparisonType,
    meets_comparision_conditions,
)
from pbpstats.filter_conditions.condition import Condition
from pbpstats.resources.enhanced_pbp import Rebound
from pbpstats.resources.possessions.possession import Possession


@dataclass
class Definition:
    comparison_type: ComparisonType
    comparison_value: int


class OffensiveReboundsCondition(Condition):
    definition: Definition

    def __init__(self, condition_definition: Dict) -> None:
        definition = Definition(**condition_definition)
        self.definition = definition

    def meets(self, input: Possession) -> bool:
        if not isinstance(input, Possession):
            return False
        num_orebs = self._get_number_of_orebs(input)

        return meets_comparision_conditions(
            self.definition.comparison_type, self.definition.comparison_value, num_orebs
        )

    def _get_number_of_orebs(self, input: Possession) -> int:
        orebs = 0
        for event in input.events:
            if isinstance(event, Rebound) and event.is_real_rebound and event.oreb:
                orebs += 1
        return orebs
