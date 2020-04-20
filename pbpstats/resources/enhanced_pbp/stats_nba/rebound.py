from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import StatsEnhancedPbpItem
from pbpstats.resources.enhanced_pbp.rebound import Rebound
from pbpstats.resources.enhanced_pbp.turnover import Turnover


class StatsRebound(Rebound, StatsEnhancedPbpItem):
    def __init__(self, *args):
        super().__init__(*args)

    def get_offense_team_id(self):
        """
        overrides method inherited from StatsEnhancedPbpItem
        """
        if self.is_real_rebound:
            return self.team_id
        if isinstance(self.previous_event, Turnover):
            # shot clock turnover has place holder rebound after turnover
            # this correct team starts next possession
            team_ids = list(self.current_players.keys())
            return team_ids[0] if team_ids[1] == self.previous_event.team_id else team_ids[1]
        return self.previous_event.get_offense_team_id()
