from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Replay


class StatsReplay(Replay, StatsEnhancedPbpItem):
    """
    Class for replay events
    """

    def __init__(self, *args):
        super().__init__(*args)
