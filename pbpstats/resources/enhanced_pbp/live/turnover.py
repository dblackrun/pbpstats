from pbpstats.resources.enhanced_pbp.live.enhanced_pbp_item import LiveEnhancedPbpItem
from pbpstats.resources.enhanced_pbp import Turnover


class LiveTurnover(Turnover, LiveEnhancedPbpItem):
    """
    Class for Turnover events
    """

    action_type = "turnover"

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_no_turnover(self):
        return not hasattr(self, "sub_type")

    @property
    def is_bad_pass(self):
        return (
            hasattr(self, "sub_type")
            and self.stripped_sub_type == "badpass"
            and self.is_steal
        )

    @property
    def is_lost_ball(self):
        return (
            hasattr(self, "sub_type")
            and self.stripped_sub_type == "lostball"
            and self.is_steal
        )

    @property
    def is_travel(self):
        return hasattr(self, "sub_type") and self.stripped_sub_type == "traveling"

    @property
    def is_3_second_violation(self):
        return hasattr(self, "sub_type") and self.stripped_sub_type == "3secviolation"

    @property
    def is_shot_clock_violation(self):
        return hasattr(self, "sub_type") and self.stripped_sub_type == "shotclock"

    @property
    def is_offensive_goaltending(self):
        return (
            hasattr(self, "sub_type")
            and self.stripped_sub_type == "offensivegoaltending"
        )

    @property
    def is_lane_violation(self):
        return hasattr(self, "sub_type") and self.stripped_sub_type == "LaneViolation"

    @property
    def is_kicked_ball(self):
        return hasattr(self, "sub_type") and self.stripped_sub_type == "kickedball"

    @property
    def is_step_out_of_bounds(self):
        return (
            hasattr(self, "sub_type")
            and self.stripped_sub_type == "outofbounds"
            and self.descriptor == "step"
        )

    @property
    def is_lost_ball_out_of_bounds(self):
        return (
            hasattr(self, "sub_type")
            and self.stripped_sub_type == "outofbounds"
            and self.descriptor == "lost ball"
        )

    @property
    def is_bad_pass_out_of_bounds(self):
        return (
            hasattr(self, "sub_type")
            and self.stripped_sub_type == "outofbounds"
            and self.descriptor == "bad pass"
        )
