from itertools import groupby
from operator import itemgetter

import pbpstats
from pbpstats.resources.enhanced_pbp.field_goal import FieldGoal
from pbpstats.resources.enhanced_pbp.free_throw import FreeThrow
from pbpstats.resources.enhanced_pbp.jump_ball import JumpBall
from pbpstats.resources.enhanced_pbp.rebound import Rebound
from pbpstats.resources.enhanced_pbp.substitution import Substitution
from pbpstats.resources.enhanced_pbp.timeout import Timeout
from pbpstats.resources.enhanced_pbp.turnover import Turnover


class Possession(object):
    def __init__(self, events):
        self.game_id = events[0].game_id
        self.period = events[0].period
        self.events = events

    def __repr__(self):
        return (
            f'<{type(self).__name__} GameId: {self.game_id}, Period: {self.period}, '
            f'Number: {self.number}, StartTime: {self.start_time}, EndTime: {self.end_time}, '
            f'OffenseTeamId: {self.offense_team_id}>'
        )

    @property
    def data(self):
        return self.__dict__

    @property
    def start_time(self):
        if not hasattr(self, 'previous_possession') or self.previous_possession is None:
            return self.events[0].clock
        return self.previous_possession.events[-1].clock

    @property
    def end_time(self):
        return self.events[-1].clock

    @property
    def offense_team_id(self):
        return self.events[0].get_offense_team_id()

    @property
    def possession_has_timeout(self):
        """
        checks if there was a timeout called on the current possession
        """
        for i, event in enumerate(self.events):
            if isinstance(event, Timeout) and event.clock != self.end_time:
                # timeout is not at possession end time
                if not (
                    event.next_event is not None and
                    (isinstance(event.next_event, FreeThrow) and not event.next_event.technical_ft) and
                    event.clock == event.next_event.clock
                ):
                    # check to make sure timeout is not between/before FTs
                    return True
            elif isinstance(event, Timeout) and event.clock == self.end_time:
                timeout_time = event.clock
                after_timeout_index = i + 1
                # call time out and turn ball over at same time as timeout following time out
                for possession_event in self.events[after_timeout_index:]:
                    if isinstance(possession_event, Turnover) and possession_event.clock == timeout_time:
                        return True
        return False

    @property
    def previous_possession_has_timeout(self):
        """
        check for timeout on previous possession - if there is a timeout at the same time as possession end, current possession starts off timeout
        """
        if self.previous_possession is not None:
            for event in self.previous_possession.events:
                if isinstance(event, Timeout) and event.clock == self.start_time:
                    if not (
                        event.next_event is not None and
                        isinstance(event.next_event, FreeThrow) and
                        event.clock == event.next_event.clock
                    ):
                        # check to make sure timeout is not beween FTs
                        return True
        return False

    @property
    def previous_possession_ending_event(self):
        """
        gets previous possession ending event - ignoring subs
        """
        previous_event_index = -1
        while isinstance(self.previous_possession.events[previous_event_index], Substitution) and len(self.previous_possession.events) > abs(previous_event_index):
            previous_event_index -= 1
        return self.previous_possession.events[previous_event_index]

    @property
    def possession_start_type(self):
        if self.number == 1:
            return pbpstats.OFF_DEADBALL_STRING
        if self.possession_has_timeout or self.previous_possession_has_timeout:
            return pbpstats.OFF_TIMEOUT_STRING
        previous_possession_ending_event = self.previous_possession_ending_event
        if isinstance(previous_possession_ending_event, (FieldGoal, FreeThrow)) and previous_possession_ending_event.made:
            shot_type = previous_possession_ending_event.shot_type
            return f'Off{shot_type}{pbpstats.MAKE_STRING}'
        if isinstance(previous_possession_ending_event, Turnover):
            if previous_possession_ending_event.is_steal:
                return pbpstats.OFF_LIVE_BALL_TURNOVER_STRING
            return pbpstats.OFF_DEADBALL_STRING
        if isinstance(previous_possession_ending_event, Rebound):
            if previous_possession_ending_event.player1_id == 0:
                # team rebound
                return pbpstats.OFF_DEADBALL_STRING
            missed_shot = previous_possession_ending_event.missed_shot
            shot_type = missed_shot.shot_type
            if hasattr(missed_shot, 'is_blocked_shot') and missed_shot.is_blocked_shot:
                return f'Off{shot_type}{pbpstats.BLOCK_STRING}'
            return f'Off{shot_type}{pbpstats.MISS_STRING}'

        if isinstance(previous_possession_ending_event, JumpBall):
            # jump balls tipped out of bounds have no player2_id and should be off deadball
            if not hasattr(previous_possession_ending_event, 'player2_id'):
                return pbpstats.OFF_LIVE_BALL_TURNOVER_STRING
            else:
                return pbpstats.OFF_DEADBALL_STRING
        return pbpstats.OFF_DEADBALL_STRING

    @property
    def previous_possession_end_shooter_player_id(self):
        if self.previous_possession is not None:
            previous_possession_ending_event = self.previous_possession_ending_event
            if isinstance(previous_possession_ending_event, FieldGoal) and previous_possession_ending_event.made:
                return previous_possession_ending_event.player1_id
            if isinstance(previous_possession_ending_event, Rebound):
                if previous_possession_ending_event.player1_id != 0:
                    missed_shot = previous_possession_ending_event.missed_shot
                    return missed_shot.player1_id
        return 0

    @property
    def previous_possession_end_rebound_player_id(self):
        if self.previous_possession is not None:
            previous_possession_ending_event = self.previous_possession_ending_event
            if isinstance(previous_possession_ending_event, Rebound):
                if previous_possession_ending_event.player1_id != 0:
                    return previous_possession_ending_event.player1_id
        return 0

    @property
    def previous_possession_end_turnover_player_id(self):
        if self.previous_possession is not None:
            previous_possession_ending_event = self.previous_possession_ending_event
            if isinstance(previous_possession_ending_event, Turnover):
                if previous_possession_ending_event.is_steal:
                    return previous_possession_ending_event.player1_id
        return 0

    @property
    def previous_possession_end_steal_player_id(self):
        if self.previous_possession is not None:
            previous_possession_ending_event = self.previous_possession_ending_event
            if isinstance(previous_possession_ending_event, Turnover):
                if previous_possession_ending_event.is_steal:
                    return previous_possession_ending_event.player3_id
        return 0

    @property
    def possession_stats(self):
        grouper = itemgetter('player_id', 'team_id', 'opponent_team_id', 'lineup_id', 'opponent_lineup_id', 'stat_key')
        results = []
        event_stats = [event_stat for event in self.events for event_stat in event.event_stats]
        for key, group in groupby(sorted(event_stats, key=grouper), grouper):
            temp_dict = dict(zip(['player_id', 'team_id', 'opponent_team_id', 'lineup_id', 'opponent_lineup_id', 'stat_key'], key))
            temp_dict['stat_value'] = sum(item['stat_value'] for item in group)
            results.append(temp_dict)

        return results