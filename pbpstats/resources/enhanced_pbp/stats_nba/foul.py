from pbpstats.resources.enhanced_pbp.stats_nba.enhanced_pbp_item import (
    StatsEnhancedPbpItem,
)
from pbpstats.resources.enhanced_pbp import Foul


class StatsFoul(Foul, StatsEnhancedPbpItem):
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
        clock = self.clock
        event = self
        while (
            event is not None
            and event.clock == clock
            and not (
                hasattr(event, "is_first_ft")
                and not event.is_technical_ft
                and self.team_id != event.team_id
            )
        ):
            event = event.next_event

        if (
            event is not None
            and hasattr(event, "is_first_ft")
            and not event.is_technical_ft
            and event.clock == clock
            and (not hasattr(self, "player3_id") or self.player3_id == event.player1_id)
        ):
            # player3 id check is to make sure player who got fouled is player shooting free throws, prior to 2005-06 because foul drawning player isn't in pbp
            if "of 1" in event.description:
                return 1
            elif "of 2" in event.description:
                return 2
            elif "of 3" in event.description:
                return 3

        # if we haven't found ft yet, try going backwards
        event = self
        while (
            event is not None
            and event.clock == clock
            and not (
                hasattr(event, "is_first_ft")
                and not event.is_technical_ft
                and self.team_id != event.team_id
            )
        ):
            event = event.previous_event

        if (
            event is not None
            and hasattr(event, "is_first_ft")
            and not event.is_technical_ft
            and event.clock == clock
            and (not hasattr(self, "player3_id") or self.player3_id == event.player1_id)
        ):
            # player3 id check is to make sure player who got fouled is player shooting free throws, prior to 2005-06 because foul drawning player isn't in pbp
            if "of 1" in event.description:
                return 1
            elif "of 2" in event.description:
                return 2
            elif "of 3" in event.description:
                return 3
        return None

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
