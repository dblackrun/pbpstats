import pytest

from pbpstats.data_loader.stats_nba.possessions.file import StatsNbaPossessionFileLoader
from pbpstats.data_loader.stats_nba.possessions.loader import StatsNbaPossessionLoader
from pbpstats.filter_conditions import get_conditions_definitions_factory
from pbpstats.filter_conditions import (
    offensive_rebounds as offensive_rebounds_conditions,
)
from pbpstats.filter_conditions.compare import ComparisonType
from pbpstats.filter_conditions.factory import ConditionsFactory
from pbpstats.resources.enhanced_pbp.rebound import Rebound


@pytest.fixture
def possessions():
    # load in all possessions to use for the test cases
    source_loader = StatsNbaPossessionFileLoader("tests/data")
    possessions_loader = StatsNbaPossessionLoader("0021600270", source_loader)
    return possessions_loader.items


def test_orebs(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": offensive_rebounds_conditions.CONDITION_TYPE,
        "data": {
            "comparison_type": ComparisonType.gte,
            "comparison_value": 1,
        },
    }
    cf.register(condition)

    for possession in possessions:
        found_oreb = False
        for evt in possession.events:
            if isinstance(evt, Rebound) and evt.oreb and evt.is_real_rebound:
                found_oreb = True
        if cf.meets(possession):
            # Condition is met, there should be an offensive rebound on this possession
            assert found_oreb
        else:
            # Condition is not met, there should not be an offensive rebound on this possession
            assert not found_oreb


def test_no_orebs(possessions):
    # get the conditions definition factory
    cdf = get_conditions_definitions_factory()

    # initialize the conditions factory
    cf = ConditionsFactory(cdf)
    # register conditions
    condition = {
        "condition_type": offensive_rebounds_conditions.CONDITION_TYPE,
        "data": {
            "comparison_type": ComparisonType.equals,
            "comparison_value": 0,
        },
    }
    cf.register(condition)

    for possession in possessions:
        found_oreb = False
        for evt in possession.events:
            if isinstance(evt, Rebound) and evt.oreb and evt.is_real_rebound:
                found_oreb = True
        if cf.meets(possession):
            # Condition is met, there should 0 offensive rebounds on this possession
            assert not found_oreb
        else:
            # Condition is not met, there should be an offensive rebound on this possession
            assert found_oreb
