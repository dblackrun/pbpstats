from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Ejection


class StatsEjection(Ejection, StatsEnhancedPbpItem):
    """
    Class for Ejection events
    """

    def __init__(self, *args):
        super().__init__(*args)
