# Register all the available filter conditions here
from pbpstats.filter_conditions import offensive_rebounds, or_, wowy
from pbpstats.filter_conditions.definition_factory import ConditionDefinitionFactory

# Initialize the conditions definition factory
# When adding a new condition it should be registered below

cdf = ConditionDefinitionFactory()
cdf.register(wowy.CONDITION_TYPE, wowy.WowyCondition)
cdf.register(
    offensive_rebounds.CONDITION_TYPE, offensive_rebounds.OffensiveReboundsCondition
)
cdf.register(or_.CONDITION_TYPE, or_.OrCondition)


def get_conditions_definitions_factory():
    return cdf
