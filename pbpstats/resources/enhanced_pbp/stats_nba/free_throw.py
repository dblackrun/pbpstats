from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import FreeThrow


class StatsFreeThrow(FreeThrow, StatsEnhancedPbpItem):
    """
    Class for free throw events
    """

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_made(self):
        """
        returns True if shot was made, False otherwise
        """
        return "MISS " not in self.description

    def get_offense_team_id(self):
        """
        returns team id that took the shot
        """
        return self.team_id
