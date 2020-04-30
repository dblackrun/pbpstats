from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import StatsEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import FieldGoal


class StatsFieldGoal(FieldGoal, StatsEnhancedPbpItem):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def shot_value(self):
        return 3 if ' 3PT ' in self.description else 2

    def get_offense_team_id(self):
        """
        overrides method inherited from StatsEnhancedPbpItem
        """
        return self.team_id
