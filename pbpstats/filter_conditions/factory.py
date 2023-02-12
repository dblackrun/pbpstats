from typing import List, Union

from pbpstats.filter_conditions.condition import Condition
from pbpstats.filter_conditions.condition_definition import ConditionDefinition
from pbpstats.filter_conditions.definition_factory import ConditionDefinitionFactory
from pbpstats.resources.enhanced_pbp.enhanced_pbp_item import EnhancedPbpItem
from pbpstats.resources.possessions.possession import Possession


class ConditionsFactory(object):

    _cdf: ConditionDefinitionFactory
    _conditions: List[Condition]

    def __init__(self, cdf: ConditionDefinitionFactory) -> None:
        self._cdf = cdf
        self._conditions = []

    def register(self, definition: ConditionDefinition) -> None:
        """
        registers a condition definition
        """
        condition = self._cdf.create(definition)
        self._conditions.append(condition)

    def register_conditions(self, definition: ConditionDefinition) -> None:
        """
        registers a condition from a defintion containing other conditions (ex. an or or not condition)
        """
        condition = self._cdf.create_conditions(definition)
        self._conditions.append(condition)

    def meets(self, input: Union[Possession, EnhancedPbpItem]) -> bool:
        for cond in self._conditions:
            if not cond.meets(input):
                return False
        return True
