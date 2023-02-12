from typing import Dict, List

from pbpstats.filter_conditions.condition import Condition
from pbpstats.filter_conditions.condition_definition import ConditionDefinition


class ConditionDefinitionFactory(object):

    _conditions_definitions: Dict[str, ConditionDefinition]

    def __init__(self) -> None:
        self._conditions_definitions = {}

    def register(self, conditions_type: str, definition: ConditionDefinition) -> None:
        self._conditions_definitions[conditions_type] = definition

    def create(self, definition: Dict) -> Condition:
        """
        uses factory to create a condition from a defintion dict
        """
        cd = ConditionDefinition(**definition)
        if cd.condition_type not in self._conditions_definitions:
            raise Exception(
                f"No definition found for condition_type: {cd.condition_type}"
            )
        condition = self._conditions_definitions[cd.condition_type]
        return condition(cd.data)

    def create_conditions(self, definition: Dict) -> List[Condition]:
        """
        uses factory to create condition from a defintion dict containing other conditions (ex. an or or not condition)
        """
        conditions = []
        condition = self._conditions_definitions[definition["condition_type"]]
        for defn in definition["data"]:
            cd = ConditionDefinition(**defn)
            if cd.condition_type not in self._conditions_definitions:
                raise Exception(
                    f"No definition found for condition_type: {cd.condition_type}"
                )
            cond = self._conditions_definitions[cd.condition_type]
            conditions.append(cond(cd.data))

        return condition(conditions)
