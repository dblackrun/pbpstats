import pytest

from pbpstats.data_loader.stats_nba.possessions.file import StatsNbaPossessionFileLoader
from pbpstats.data_loader.stats_nba.possessions.loader import StatsNbaPossessionLoader
from pbpstats.filter_conditions import get_conditions_definitions_factory
from pbpstats.filter_conditions import or_ as or_condition
from pbpstats.filter_conditions import wowy as wowy_condition
from pbpstats.filter_conditions.compare import ComparisonType
from pbpstats.filter_conditions.factory import ConditionsFactory


@pytest.fixture
def possessions():
    # load in all possessions to use for the test cases
    source_loader = StatsNbaPossessionFileLoader("tests/data")
    possessions_loader = StatsNbaPossessionLoader("0021600270", source_loader)
    return possessions_loader.items


def test_or_player_on(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition1 = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.on_floor,
            "comparison_type": ComparisonType.equals,
            "comparison_value": 1,
            "player_ids": [202322],  # This is player ID for John Wall
        },
    }
    condition2 = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.on_floor,
            "comparison_type": ComparisonType.equals,
            "comparison_value": 1,
            "player_ids": [203078],  # This is player ID for Bradley Beal
        },
    }
    condition = {
        "condition_type": or_condition.CONDITION_TYPE,
        "data": [condition1, condition2],
    }

    cf.register_conditions(condition)

    for possession in possessions:
        for evt in possession.events:
            if cf.meets(evt):
                # 1610612764 is team ID for the Wizards
                wizards_players = evt.current_players[1610612764]
                # conditions are met, so one of them should be on
                assert 202322 in wizards_players or 203078 in wizards_players
            else:
                # 1610612764 is team ID for the Wizards
                wizards_players = evt.current_players[1610612764]
                # conditions are not met, so neither should be on
                assert 202322 not in wizards_players and 203078 not in wizards_players


def test_or_player_off(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition1 = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.off_floor,
            "comparison_type": ComparisonType.equals,
            "comparison_value": 1,
            "player_ids": [202322],  # This is player ID for John Wall
        },
    }
    condition2 = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.off_floor,
            "comparison_type": ComparisonType.equals,
            "comparison_value": 1,
            "player_ids": [203078],  # This is player ID for Bradley Beal
        },
    }
    condition = {
        "condition_type": or_condition.CONDITION_TYPE,
        "data": [condition1, condition2],
    }

    cf.register_conditions(condition)

    for possession in possessions:
        for evt in possession.events:
            if cf.meets(evt):
                # 1610612764 is team ID for the Wizards
                wizards_players = evt.current_players[1610612764]
                # conditions are met, so one of them should be off
                assert 202322 not in wizards_players or 203078 not in wizards_players
            else:
                # 1610612764 is team ID for the Wizards
                wizards_players = evt.current_players[1610612764]
                # conditions are not met, so neither of them should be off
                assert 202322 in wizards_players and 203078 in wizards_players
