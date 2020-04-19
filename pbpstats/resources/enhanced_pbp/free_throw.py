import abc

from pbpstats import FREE_THROW_STRING
from pbpstats.resources.enhanced_pbp.foul import Foul


class FreeThrow(metaclass=abc.ABCMeta):
    event_type = 3
    shot_type = FREE_THROW_STRING

    @abc.abstractproperty
    def made(self):
        pass

    @property
    def ft_1_of_1(self):
        return self.event_action_type == 10

    @property
    def ft_1_of_2(self):
        return self.event_action_type == 11

    @property
    def ft_2_of_2(self):
        return self.event_action_type == 12

    @property
    def ft_1_of_3(self):
        return self.event_action_type == 13

    @property
    def ft_2_of_3(self):
        return self.event_action_type == 14

    @property
    def ft_3_of_3(self):
        return self.event_action_type == 15

    @property
    def first_ft(self):
        return '1 of' in self.description or self.ft_1pt or self.ft_2pt or self.ft_3pt

    @property
    def end_ft(self):
        return self.ft_1_of_1 or self.ft_2_of_2 or self.ft_3_of_3 or self.ft_1pt or self.ft_2pt or self.ft_3pt

    @property
    def technical_ft(self):
        return ' Technical' in self.description

    @property
    def ft_1pt(self):
        """
        only used in g-league, starting in 2019-20 season
        """
        return self.event_action_type == 30 or self.event_action_type == 35

    @property
    def ft_2pt(self):
        """
        only used in g-league, starting in 2019-20 season
        """
        return self.event_action_type == 31 or self.event_action_type == 36

    @property
    def ft_3pt(self):
        """
        only used in g-league, starting in 2019-20 season
        """
        return self.event_action_type == 32 or self.event_action_type == 37

    @property
    def is_away_from_play_ft(self):
        foul = self.foul_that_led_to_ft
        if ((self.ft_1_of_1 or self.ft_1pt) or (self.ft_2_of_2 or self.ft_2pt)) and foul is not None and foul.is_away_from_play_foul:
            made_shots_at_event_time = []
            fts_by_other_player_at_event_time = []
            events_at_event_time = self.get_all_events_at_current_time()
            for event in events_at_event_time:
                if hasattr(event, 'made') and event.made:
                    if not isinstance(event, FreeThrow):
                        made_shots_at_event_time.append(event)
                    if isinstance(event, FreeThrow) and event.player1_id != self.player1_id:
                        fts_by_other_player_at_event_time.append(event)

            if len(made_shots_at_event_time) == 0:
                # check for made free throw by other player - this is where player is fouled going for rebound on made FT
                if len(fts_by_other_player_at_event_time) == 0:
                    return True
                for ft in fts_by_other_player_at_event_time:
                    if ft.team_id != self.team_id:
                        return True
            else:
                made_shots_at_event_time = sorted(made_shots_at_event_time, key=lambda k: k.order)
                if (made_shots_at_event_time[0].team_id == foul.team_id) and (self.player1_id != made_shots_at_event_time[0].player1_id):
                    # make sure player who made shot is not player who shot FT
                    return True

        return False

    @property
    def is_inbound_foul_ft(self):
        if self.ft_1_of_1 or self.ft_1pt:
            events_at_event_time = self.get_all_events_at_current_time()
            for event in events_at_event_time:
                if isinstance(event, Foul) and event.is_inbound_foul:
                    return True

        return False

    @property
    def foul_that_led_to_ft(self):
        clock = self.clock
        # foul should be before FT so start by going backwards
        event = self
        while event is not None and event.clock == clock and not (isinstance(event, Foul) and not event.is_technical and not event.is_double_technical):
            event = event.previous_event

        if isinstance(event, Foul) and not event.is_technical and not event.is_double_technical and event.clock == clock:
            return event

        # bug in pbp where foul is after FT
        event = self
        while event is not None and event.clock == clock and not (isinstance(event, Foul) and not event.is_technical and not event.is_double_technical):
            event = event.next_event

        if isinstance(event, Foul) and not event.is_technical and not event.is_double_technical and event.clock == clock:
            return event
        return None

    @property
    def num_ft_for_trip(self):
        if 'of 1' in self.description:
            return 1
        elif 'of 2' in self.description:
            return 2
        elif 'of 3' in self.description:
            return 3

    @property
    def free_throw_type(self):
        if self.technical_ft:
            return 'Technical'
        num_fts = self.num_ft_for_trip

        if num_fts == 1:
            # check for shot before FT at same time as FT
            previous_event = self
            while previous_event is not None and previous_event.clock == self.clock and not (hasattr(previous_event, 'made') and previous_event.made and not isinstance(previous_event, FreeThrow)):
                previous_event = previous_event.previous_event
            if previous_event is not None and previous_event.clock == self.clock and (hasattr(previous_event, 'made') and previous_event.made and not isinstance(previous_event, FreeThrow)):
                and1_shot = previous_event
                if self.player1_id == and1_shot.player1_id:
                    return f'{and1_shot.shot_value}pt And 1'
                else:
                    return '1 Shot Away From Play Foul'
            else:
                return '1 Shot Away From Play Foul'
        foul_event = self.foul_that_led_to_ft
        if foul_event.is_shooting_foul or foul_event.is_shooting_block_foul:
            return f'{num_fts}pt Shooting Foul'
        elif foul_event.is_flagrant:
            if num_fts is None:
                # assume 2 shot flagrant if num_fts is None
                num_fts = 2
            return f'{num_fts} Shot Flagrant Foul'
        elif foul_event.is_away_from_play_foul:
            return f'{num_fts} Shot Away From Play Foul'
        elif foul_event.is_inbound_foul:
            return f'{num_fts} Shot Inbound Foul'
        elif foul_event.is_clear_path_foul:
            return f'{num_fts} Shot Clear Path Foul'
        elif num_fts == 3:
            return '3pt Shooting Foul'
        else:
            return 'Penalty'

    @property
    def current_players_for_plus_minus(self):
        return self.foul_that_led_to_ft.current_players

    @property
    def event_stats(self):
        return self.base_stats
