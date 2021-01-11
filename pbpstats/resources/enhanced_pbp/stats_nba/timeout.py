from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Timeout


class StatsTimeout(Timeout, StatsEnhancedPbpItem):
    """
    Class for timeout events
    """

    event_type = 9

    def __init__(self, *args):
        super().__init__(*args)
