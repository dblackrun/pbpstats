from dataclasses import dataclass
from typing import Dict, List, Union

from pbpstats.filter_conditions.condition import Condition
from pbpstats.resources.enhanced_pbp.enhanced_pbp_item import EnhancedPbpItem
from pbpstats.resources.possessions.possession import Possession


@dataclass
class Definition:
    conditions: List[Condition]


class OrCondition(Condition):
    definition: Definition

    def __init__(self, condition_definition: List[Dict]) -> None:
        definition = Definition(condition_definition)
        self.definition = definition

    def meets(self, input: Union[EnhancedPbpItem, Possession]) -> bool:
        for condition in self.definition.conditions:
            if condition.meets(input):
                return True
