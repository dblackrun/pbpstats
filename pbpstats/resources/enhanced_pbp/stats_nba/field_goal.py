from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import FieldGoal


class StatsFieldGoal(FieldGoal, StatsEnhancedPbpItem):
    """
    Class for field goal events
    """

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def shot_value(self):
        """
        returns 3 if shot is a 3 point attempt, 2 otherwise
        """
        return 3 if " 3PT " in self.description else 2

    def get_offense_team_id(self):
        """
        returns team id that took the shot
        """
        return self.team_id
