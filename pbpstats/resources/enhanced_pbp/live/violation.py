from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import Violation


class LiveViolation(Violation, LiveEnhancedPbpItem):
    """
    Class for violation events
    """

    action_type = "violation"

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_delay_of_game(self):
        return self.stripped_sub_type == "delayofgame"

    @property
    def is_goaltend_violation(self):
        return self.stripped_sub_type == "defensivegoaltending"

    @property
    def is_lane_violation(self):
        return self.stripped_sub_type == "lane"

    @property
    def is_jumpball_violation(self):
        return self.stripped_sub_type == "jumpball"

    @property
    def is_kicked_ball_violation(self):
        return self.stripped_sub_type == "kickedball"

    @property
    def is_double_lane_violation(self):
        return self.stripped_sub_type == "doublelane"
