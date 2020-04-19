from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import StatsEnhancedPbpItem
from pbpstats.resources.enhanced_pbp.free_throw import FreeThrow


class StatsFreeThrow(FreeThrow, StatsEnhancedPbpItem):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def made(self):
        return 'MISS ' not in self.description
