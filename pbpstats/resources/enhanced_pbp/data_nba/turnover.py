from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Turnover


class DataTurnover(Turnover, DataEnhancedPbpItem):
    """
    Class for Turnover events
    """

    event_type = 5

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def is_no_turnover(self):
        return self.event_action_type == 0

    @property
    def is_bad_pass(self):
        return self.event_action_type == 1 and self.is_steal

    @property
    def is_lost_ball(self):
        return self.event_action_type == 2 and self.is_steal

    @property
    def is_travel(self):
        return self.event_action_type == 4

    @property
    def is_3_second_violation(self):
        return self.event_action_type == 8

    @property
    def is_shot_clock_violation(self):
        return self.event_action_type == 11

    @property
    def is_offensive_goaltending(self):
        return self.event_action_type == 15

    @property
    def is_lane_violation(self):
        return self.event_action_type == 17

    @property
    def is_kicked_ball(self):
        return self.event_action_type == 19

    @property
    def is_step_out_of_bounds(self):
        return self.event_action_type == 39

    @property
    def is_lost_ball_out_of_bounds(self):
        # some labelled as lost ball but should be lost ball out of bounds (missing player3 id)
        return self.event_action_type == 40 or (
            self.event_action_type == 2 and not self.is_steal
        )

    @property
    def is_bad_pass_out_of_bounds(self):
        # some labelled as bad pass but should be bad pass out of bounds (missing player3 id)
        return self.event_action_type == 45 or (
            self.event_action_type == 1 and not self.is_steal
        )
