from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from pbpstats.filter_conditions.compare import (
    ComparisonType,
    meets_comparision_conditions,
)
from pbpstats.filter_conditions.condition import Condition
from pbpstats.resources.enhanced_pbp.enhanced_pbp_item import EnhancedPbpItem


class FilterType(str, Enum):
    on_floor = "on_floor"
    off_floor = "off_floor"


@dataclass
class Definition:
    filter_type: FilterType
    comparison_type: ComparisonType
    comparison_value: int
    player_ids: List[int]


class WowyCondition(Condition):
    definition: Definition

    def __init__(self, condition_definition: Dict) -> None:
        definition = Definition(**condition_definition)
        self.definition = definition

    def meets(self, input: EnhancedPbpItem) -> bool:
        if not isinstance(input, EnhancedPbpItem):
            return False
        num_players = self._get_number_of_filter_players_for_filter_type(
            self.definition, input
        )
        if num_players is None:
            return False

        return meets_comparision_conditions(
            self.definition.comparison_type,
            self.definition.comparison_value,
            num_players,
        )

    def _get_number_of_filter_players_for_filter_type(
        self, definition: Definition, input: EnhancedPbpItem
    ) -> int:
        if definition.filter_type == FilterType.on_floor:
            return self._get_number_of_filter_players_on_floor(
                self.definition.player_ids, input
            )
        elif definition.filter_type == FilterType.off_floor:
            return self._get_number_of_filter_players_of_floor(
                self.definition.player_ids, input
            )

    def _get_number_of_filter_players_on_floor(
        self, player_ids: list[int], input: EnhancedPbpItem
    ) -> int:
        num_players = 0
        # current players are separated by team id combine them
        all_players_on_floor = []
        for current_players in input.current_players.values():
            all_players_on_floor += current_players

        # count how many of the filter players are on the floor
        for player_id in player_ids:
            if player_id in all_players_on_floor:
                num_players += 1
        return num_players

    def _get_number_of_filter_players_of_floor(
        self, player_ids: list[int], input: EnhancedPbpItem
    ) -> int:
        num_players = 0
        # current players are separated by team id combine them
        all_players_on_floor = []
        for current_players in input.current_players.values():
            all_players_on_floor += current_players

        # count how many of the filter players are on the floor
        for player_id in player_ids:
            if player_id not in all_players_on_floor:
                num_players += 1
        return num_players
