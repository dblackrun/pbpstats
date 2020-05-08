from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Turnover


class StatsTurnover(Turnover, StatsEnhancedPbpItem):
    """
    Class for Turnover events
    """

    def __init__(self, *args):
        super().__init__(*args)

    def get_offense_team_id(self):
        """
        returns team id for team on offense for event
        """
        if self.is_no_turnover:
            return self.previous_event.get_offense_team_id()
        return self.team_id
