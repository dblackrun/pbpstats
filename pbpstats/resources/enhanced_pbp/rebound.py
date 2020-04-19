from pbpstats.resources.enhanced_pbp.end_of_period import EndOfPeriod
from pbpstats.resources.enhanced_pbp.field_goal import FieldGoal
from pbpstats.resources.enhanced_pbp.free_throw import FreeThrow
from pbpstats.resources.enhanced_pbp.replay import Replay
from pbpstats.resources.enhanced_pbp.turnover import Turnover


class Rebound(object):
    event_type = 4

    @property
    def is_real_rebound(self):
        """
        all missed shots have a rebound in the play-by-play but
        not all of these rebounds should be counted as actual rebounds
        """
        if self.is_placeholder:
            return False

        if self.is_buzzer_beater_placeholder:
            return False

        if self.is_turnover_placeholder:
            return False

        if self.is_non_live_ft_placeholder:
            return False

        if self.is_buzzer_beater_rebound_at_shot_time:
            return False

        return True

    @property
    def is_placeholder(self):
        """
        these are team rebounds on for example missed FT 1 of 2
        """
        return self.event_action_type != 0 and self.player1_id == 0

    @property
    def is_turnover_placeholder(self):
        """
        ignore if shot clock violation or kicked ball turnover at time of team rebound
        these get logged as team rebounds but they aren't actual rebounds, they are turnovers
        """
        events_at_event_time = self.get_all_events_at_current_time()
        for event in events_at_event_time:
            if (isinstance(event, Turnover) and (event.is_shot_clock_violation or event.is_kicked_ball)) and self.player1_id == 0:
                return True
        return False

    @property
    def is_non_live_ft_placeholder(self):
        """
        example: rebound after missed flagrant FT 2 of 2
        """
        if isinstance(self.missed_shot, FreeThrow) and not self.missed_shot.end_ft:
            return True
        return False

    @property
    def is_buzzer_beater_placeholder(self):
        """
        rebounds occur after time has expired but are still logged in play-by-play
        """
        next_event = self.next_event
        if isinstance(next_event, Replay):
            next_event = next_event.next_event
        if (
            (self.clock == '00:00.0' or self.clock == '0:00') and
            self.player1_id == 0 and
            (next_event is not None and isinstance(next_event, EndOfPeriod) or next_event is None)
        ):
            return True
        return False

    @property
    def is_buzzer_beater_rebound_at_shot_time(self):
        """
        sometimes rebound on buzzer beater is given the same time as shot - don't count these
        only don't count if rebound is last event before end of period event, ignoring replay events
        """
        if self.missed_shot.seconds_remaining <= 3 and self.seconds_remaining == self.missed_shot.seconds_remaining and self.player1_id == 0:
            next_event = self.next_event
            if isinstance(next_event, Replay):
                next_event = next_event.next_event
            if isinstance(next_event, EndOfPeriod):
                return True
        return False

    @property
    def missed_shot(self):
        if isinstance(self.previous_event, (FieldGoal, FreeThrow)):
            if not self.previous_event.made:
                return self.previous_event
        elif isinstance(self.previous_event, Turnover) and self.previous_event.is_shot_clock_violation:
            if isinstance(self.previous_event, FieldGoal):
                return self.previous_event.previous_event
        raise ValueError(f'previous event: {self.previous_event} is not a missed free throw or field goal. check event order.')

    @property
    def oreb(self):
        return self.team_id == self.missed_shot.team_id

    @property
    def self_reb(self):
        return self.player1_id == self.missed_shot.player1_id

    @property
    def event_stats(self):
        return self.base_stats
