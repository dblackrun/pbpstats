class Foul(object):
    event_type = 6

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
    def is_flagrant(self):
        return self.event_action_type in [14, 15]

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

    @property
    def event_stats(self):
        return self.base_stats
