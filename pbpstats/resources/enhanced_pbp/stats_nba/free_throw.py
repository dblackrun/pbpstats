from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import StatsEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import FreeThrow


class StatsFreeThrow(FreeThrow, StatsEnhancedPbpItem):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_made(self):
        return 'MISS ' not in self.description

    def get_offense_team_id(self):
        """
        overrides method inherited from StatsEnhancedPbpItem
        """
        return self.team_id
