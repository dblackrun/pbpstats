import pytest

from pbpstats.data_loader.stats_nba.possessions.file import StatsNbaPossessionFileLoader
from pbpstats.data_loader.stats_nba.possessions.loader import StatsNbaPossessionLoader
from pbpstats.filter_conditions import get_conditions_definitions_factory
from pbpstats.filter_conditions import wowy as wowy_condition
from pbpstats.filter_conditions.compare import ComparisonType
from pbpstats.filter_conditions.factory import ConditionsFactory


@pytest.fixture
def possessions():
    # load in all possessions to use for the test cases
    source_loader = StatsNbaPossessionFileLoader("tests/data")
    possessions_loader = StatsNbaPossessionLoader("0021600270", source_loader)
    return possessions_loader.items


def test_player_on(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.on_floor,
            "comparison_type": ComparisonType.equals,
            "comparison_value": 1,
            "player_ids": [202322],  # This is player ID for John Wall
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            if cf.meets(evt):
                # 1610612764 is team ID for the Wizards
                assert 202322 in evt.current_players[1610612764]
            else:
                assert 202322 not in evt.current_players[1610612764]


def test_player_off(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.off_floor,
            "comparison_type": ComparisonType.equals,
            "comparison_value": 1,
            "player_ids": [202322],  # This is player ID for John Wall
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            if cf.meets(evt):
                # 1610612764 is team ID for the Wizards
                assert 202322 not in evt.current_players[1610612764]
            else:
                assert 202322 in evt.current_players[1610612764]


def test_players_on(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.on_floor,
            "comparison_type": ComparisonType.equals,
            "comparison_value": 2,
            "player_ids": [
                202322,
                203078,
            ],  # This is player ID for John Wall and Bradley Beal
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            # 1610612764 is team ID for the Wizards
            wizards_players = evt.current_players[1610612764]
            if cf.meets(evt):
                assert 202322 in wizards_players and 203078 in wizards_players
            else:
                assert 202322 not in wizards_players or 203078 not in wizards_players


def test_players_off(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.off_floor,
            "comparison_type": ComparisonType.equals,
            "comparison_value": 2,
            "player_ids": [
                202322,
                203078,
            ],  # This is player ID for John Wall and Bradley Beal
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            # 1610612764 is team ID for the Wizards
            wizards_players = evt.current_players[1610612764]
            if cf.meets(evt):
                assert 202322 not in wizards_players and 203078 not in wizards_players
            else:
                assert 202322 in wizards_players or 203078 in wizards_players


def test_players_on_gt(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.on_floor,
            "comparison_type": ComparisonType.gt,
            "comparison_value": 1,
            "player_ids": [
                202322,
                203078,
            ],  # This is player ID for John Wall and Bradley Beal
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            # 1610612764 is team ID for the Wizards
            wizards_players = evt.current_players[1610612764]
            if cf.meets(evt):
                assert 202322 in wizards_players and 203078 in wizards_players
            else:
                assert 202322 not in wizards_players or 203078 not in wizards_players


def test_players_off_gt(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.off_floor,
            "comparison_type": ComparisonType.gt,
            "comparison_value": 1,
            "player_ids": [
                202322,
                203078,
            ],  # This is player ID for John Wall and Bradley Beal
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            # 1610612764 is team ID for the Wizards
            wizards_players = evt.current_players[1610612764]
            if cf.meets(evt):
                assert 202322 not in wizards_players and 203078 not in wizards_players
            else:
                assert 202322 in wizards_players or 203078 in wizards_players


def test_players_on_lt(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.on_floor,
            "comparison_type": ComparisonType.lt,
            "comparison_value": 1,
            "player_ids": [
                202322,
                203078,
            ],  # This is player ID for John Wall and Bradley Beal
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            # 1610612764 is team ID for the Wizards
            wizards_players = evt.current_players[1610612764]
            if cf.meets(evt):
                assert 202322 not in wizards_players and 203078 not in wizards_players
            else:
                assert 202322 in wizards_players or 203078 in wizards_players


def test_players_off_lt(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.off_floor,
            "comparison_type": ComparisonType.lt,
            "comparison_value": 1,
            "player_ids": [
                202322,
                203078,
            ],  # This is player ID for John Wall and Bradley Beal
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            # 1610612764 is team ID for the Wizards
            wizards_players = evt.current_players[1610612764]
            if cf.meets(evt):
                assert 202322 in wizards_players and 203078 in wizards_players
            else:
                assert 202322 not in wizards_players or 203078 not in wizards_players


def test_players_on_gte(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.on_floor,
            "comparison_type": ComparisonType.gte,
            "comparison_value": 2,
            "player_ids": [
                202322,
                203078,
            ],  # This is player ID for John Wall and Bradley Beal
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            # 1610612764 is team ID for the Wizards
            wizards_players = evt.current_players[1610612764]
            if cf.meets(evt):
                assert 202322 in wizards_players and 203078 in wizards_players
            else:
                assert 202322 not in wizards_players or 203078 not in wizards_players


def test_players_off_gte(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.off_floor,
            "comparison_type": ComparisonType.gte,
            "comparison_value": 2,
            "player_ids": [
                202322,
                203078,
            ],  # This is player ID for John Wall and Bradley Beal
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            # 1610612764 is team ID for the Wizards
            wizards_players = evt.current_players[1610612764]
            if cf.meets(evt):
                assert 202322 not in wizards_players and 203078 not in wizards_players
            else:
                assert 202322 in wizards_players or 203078 in wizards_players


def test_players_on_lte(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.on_floor,
            "comparison_type": ComparisonType.lte,
            "comparison_value": 1,
            "player_ids": [
                202322,
                203078,
            ],  # This is player ID for John Wall and Bradley Beal
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            # 1610612764 is team ID for the Wizards
            wizards_players = evt.current_players[1610612764]
            if cf.meets(evt):
                assert 202322 not in wizards_players or 203078 not in wizards_players
            else:
                assert 202322 in wizards_players and 203078 in wizards_players


def test_players_off_lte(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": wowy_condition.CONDITION_TYPE,
        "data": {
            "filter_type": wowy_condition.FilterType.off_floor,
            "comparison_type": ComparisonType.lte,
            "comparison_value": 1,
            "player_ids": [
                202322,
                203078,
            ],  # This is player ID for John Wall and Bradley Beal
        },
    }
    cf.register(condition)

    for possession in possessions:
        for evt in possession.events:
            # 1610612764 is team ID for the Wizards
            wizards_players = evt.current_players[1610612764]
            if cf.meets(evt):
                assert not (
                    202322 not in wizards_players and 203078 not in wizards_players
                )
            else:
                assert 202322 not in wizards_players and 203078 not in wizards_players
