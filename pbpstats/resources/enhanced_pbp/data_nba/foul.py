from pbpstats.resources.enhanced_pbp.data_nba.enhanced_pbp_item import (
    DataEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Foul


class DataFoul(Foul, DataEnhancedPbpItem):
    """
    Class for foul events
    """

    event_type = 6

    def __init__(self, *args):
        super().__init__(*args)

    @property
    def number_of_fta_for_foul(self):
        """
        returns the number of free throws resulting from the foul
        """
        if "(1 FTA)" in self.description:
            return 1
        elif "(2 FTA)" in self.description:
            return 2
        elif "(3 FTA)" in self.description:
            return 3

    @property
    def is_personal_foul(self):
        return self.event_action_type == 1

    @property
    def is_shooting_foul(self):
        return self.event_action_type == 2

    @property
    def is_loose_ball_foul(self):
        return self.event_action_type == 3

    @property
    def is_offensive_foul(self):
        return self.event_action_type == 4

    @property
    def is_inbound_foul(self):
        return self.event_action_type == 5

    @property
    def is_away_from_play_foul(self):
        return self.event_action_type == 6

    @property
    def is_clear_path_foul(self):
        return self.event_action_type == 9

    @property
    def is_double_foul(self):
        return self.event_action_type == 10

    @property
    def is_technical(self):
        return self.event_action_type in [11, 12, 13, 18, 19, 25, 30]

    @property
    def is_flagrant1(self):
        return self.event_action_type == 14

    @property
    def is_flagrant2(self):
        return self.event_action_type == 15

    @property
    def is_double_technical(self):
        return self.event_action_type == 16

    @property
    def is_defensive_3_seconds(self):
        return self.event_action_type == 17

    @property
    def is_delay_of_game(self):
        return self.event_action_type == 18

    @property
    def is_charge(self):
        return self.event_action_type == 26

    @property
    def is_personal_block_foul(self):
        return self.event_action_type == 27

    @property
    def is_personal_take_foul(self):
        return self.event_action_type == 28

    @property
    def is_shooting_block_foul(self):
        return self.event_action_type == 29
