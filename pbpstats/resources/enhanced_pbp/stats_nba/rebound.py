from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import StatsEnhancedPbpItem
from pbpstats.resources.enhanced_pbp.rebound import Rebound


class StatsRebound(Rebound, StatsEnhancedPbpItem):
    def __init__(self, *args):
        super().__init__(*args)
