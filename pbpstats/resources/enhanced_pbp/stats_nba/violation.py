from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Violation


class StatsViolation(Violation, StatsEnhancedPbpItem):
    """
    Class for violation events
    """

    event_type = 7

    def __init__(self, *args):
        super().__init__(*args)

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
