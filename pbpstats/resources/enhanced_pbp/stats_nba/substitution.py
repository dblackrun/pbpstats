from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Substitution


class StatsSubstitution(Substitution, StatsEnhancedPbpItem):
    """
    Class for Substitution events
    """

    def __init__(self, *args):
        super().__init__(*args)
