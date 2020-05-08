from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Rebound, Turnover


class StatsRebound(Rebound, StatsEnhancedPbpItem):
    """
    Class for rebound events
    """

    def __init__(self, *args):
        super().__init__(*args)

    def get_offense_team_id(self):
        """
        returns team id for team on offense for the shot that was rebounded
        """
        if self.is_real_rebound:
            return self.missed_shot.team_id
        if (
            isinstance(self.previous_event, Turnover)
            and not self.previous_event.is_no_turnover
        ):
            # shot clock turnover has place holder rebound after turnover
            # this correct team starts next possession
            team_ids = list(self.current_players.keys())
            return (
                team_ids[0]
                if team_ids[1] == self.previous_event.team_id
                else team_ids[1]
            )
        return self.previous_event.get_offense_team_id()
