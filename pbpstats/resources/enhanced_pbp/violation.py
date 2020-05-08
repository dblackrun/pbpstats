from pbpstats import DEFENSIVE_GOALTENDING_STRING


class Violation(object):
    """
    Class for violation events
    """

    event_type = 7

    @property
    def is_delay_of_game(self):
        return self.event_action_type == 1

    @property
    def is_goaltend_violation(self):
        return self.event_action_type == 2

    @property
    def is_lane_violation(self):
        return self.event_action_type == 3

    @property
    def is_jumpball_violation(self):
        return self.event_action_type == 4

    @property
    def is_kicked_ball_violation(self):
        return self.event_action_type == 5

    @property
    def is_double_lane_violation(self):
        return self.event_action_type == 6

    @property
    def event_stats(self):
        """
        returns list of dicts with all stats for event
        """
        stats = []
        if self.is_goaltend_violation:
            stats.append(
                {
                    "player_id": self.player1_id,
                    "team_id": self.team_id,
                    "stat_key": DEFENSIVE_GOALTENDING_STRING,
                    "stat_value": 1,
                }
            )
            team_ids = list(self.current_players.keys())
            lineups_ids = self.lineup_ids
            for stat in stats:
                opponent_team_id = (
                    team_ids[0] if stat["team_id"] == team_ids[1] else team_ids[1]
                )
                stat["lineup_id"] = lineups_ids[stat["team_id"]]
                stat["opponent_team_id"] = opponent_team_id
                stat["opponent_lineup_id"] = lineups_ids[opponent_team_id]
        return self.base_stats + stats
