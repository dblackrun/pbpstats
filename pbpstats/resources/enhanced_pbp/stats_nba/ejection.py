from pbpstats.resources.enhanced_pbp import Ejection
from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)


class StatsEjection(Ejection, StatsEnhancedPbpItem):
    """
    Class for Ejection events
    """

    event_type = 11

    def __init__(self, *args):
        super().__init__(*args)
