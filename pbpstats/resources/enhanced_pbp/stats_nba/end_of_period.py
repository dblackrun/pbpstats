from pbpstats.resources.enhanced_pbp import EndOfPeriod
from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)


class StatsEndOfPeriod(EndOfPeriod, StatsEnhancedPbpItem):
    """
    Class for end of period events
    """

    event_type = 13

    def __init__(self, *args):
        super().__init__(*args)
