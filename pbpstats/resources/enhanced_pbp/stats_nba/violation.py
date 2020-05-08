from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Violation


class StatsViolation(Violation, StatsEnhancedPbpItem):
    """
    Class for violation events
    """

    def __init__(self, *args):
        super().__init__(*args)
