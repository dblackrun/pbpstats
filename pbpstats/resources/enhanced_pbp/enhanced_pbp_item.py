import abc

import pbpstats
from pbpstats.resources.enhanced_pbp.end_of_period import EndOfPeriod
from pbpstats.resources.enhanced_pbp.field_goal import FieldGoal
from pbpstats.resources.enhanced_pbp.free_throw import FreeThrow


class EnhancedPbpItem(metaclass=abc.ABCMeta):
    def __repr__(self):
        return f"<{type(self).__name__} GameId: {self.game_id}, Description: {self.description}, Time: {self.clock}, EventNum: {self.event_num}>"

    @abc.abstractproperty
    def is_possession_ending_event(self):
        pass

    @abc.abstractproperty
    def event_stats(self):
        pass

    @property
    def base_stats(self):
        """
        these are event stats for all event types
        - seconds played off/def
        - possession off/def
        """
        stat_items = []
        team_ids = list(self.current_players.keys())
        lineups_ids = self.lineup_ids
        if self.seconds_since_previous_event != 0:
            for team_id, players in self.previous_event.current_players.items():
                seconds_stat_key = (
                    pbpstats.SECONDS_PLAYED_OFFENSE_STRING
                    if team_id == self.get_offense_team_id()
                    else pbpstats.SECONDS_PLAYED_DEFENSE_STRING
                )
                opponent_team_id = team_ids[0] if team_id == team_ids[1] else team_ids[1]
                previous_poss_lineup_ids = self.previous_event.lineup_ids
                for player_id in players:
                    seconds_stat_item = {
                        'player_id': player_id,
                        'team_id': team_id,
                        'opponent_team_id': opponent_team_id,
                        'lineup_id': previous_poss_lineup_ids[team_id],
                        'opponent_lineup_id': previous_poss_lineup_ids[opponent_team_id],
                        'stat_key': seconds_stat_key,
                        'stat_value': self.seconds_since_previous_event,
                    }
                    stat_items.append(seconds_stat_item)

        if self.count_as_possession:
            for team_id, players in self.current_players.items():
                possessions_stat_key = (
                    pbpstats.OFFENSIVE_POSSESSION_STRING
                    if team_id == self.get_offense_team_id()
                    else pbpstats.DEFENSIVE_POSSESSION_STRING
                )
                opponent_team_id = team_ids[0] if team_id == team_ids[1] else team_ids[1]
                for player_id in players:
                    possessions_stat_item = {
                        'player_id': player_id,
                        'team_id': team_id,
                        'opponent_team_id': opponent_team_id,
                        'lineup_id': lineups_ids[team_id],
                        'opponent_lineup_id': lineups_ids[opponent_team_id],
                        'stat_key': possessions_stat_key,
                        'stat_value': 1,
                    }
                    stat_items.append(possessions_stat_item)
        return stat_items

    def get_all_events_at_current_time(self):
        events = [self]
        # going backwards
        event = self
        while event is not None and self.seconds_remaining == event.seconds_remaining:
            if event != self:
                events.append(event)
            event = event.previous_event
        # going forwards
        event = self
        while event is not None and self.seconds_remaining == event.seconds_remaining:
            if event != self:
                events.append(event)
            event = event.next_event
        return sorted(events, key=lambda k: k.order)

    def get_offense_team_id(self):
        if not self.previous_event.count_as_possession:
            if self.previous_event.is_possession_ending_event:
                # this is to avoid team having back to back possessions when last possession doesn't count
                team_ids = list(self.current_players.keys())
                return team_ids[0] if team_ids[1] == self.previous_event.get_offense_team_id() else team_ids[1]
            return self.previous_event.get_offense_team_id()
        else:
            team_ids = list(self.current_players.keys())
            return team_ids[0] if team_ids[1] == self.previous_event.get_offense_team_id() else team_ids[1]

    @property
    def seconds_remaining(self):
        split = self.clock.split(':')
        return float(split[0]) * 60 + float(split[1])

    @property
    def current_players(self):
        """
        for all non subsitution events current players are just
        the same as previous event
        this gets overwritten in Substitution class
        """
        return self.previous_event.current_players

    @property
    def lineup_ids(self):
        """
        hyphen separated sorted player id strings
        """
        lineup_ids = {}
        for team_id, team_players in self.current_players.items():
            players = [str(player_id) for player_id in team_players]
            sorted_player_ids = sorted(players)
            lineup_id = '-'.join(sorted_player_ids)
            lineup_ids[team_id] = lineup_id
        return lineup_ids

    @property
    def seconds_until_next_event(self):
        if self.next_event is None:
            return 0
        return self.seconds_remaining - self.next_event.seconds_remaining

    @property
    def seconds_since_previous_event(self):
        if self.previous_event is None:
            return 0
        return self.previous_event.seconds_remaining - self.seconds_remaining

    @property
    def count_as_possession(self):
        """
        don't count possession change if it starts with <= 2 seconds left
        and no points are scored before period ends
        """
        if self.is_possession_ending_event:
            if self.seconds_remaining > 2:
                return True
            elif not isinstance(self, EndOfPeriod):
                # possession starts in final 2 seconds
                # return True if there is a FT or FGM
                next_event = self.next_event
                while next_event is not None:
                    if isinstance(next_event, FreeThrow) or (isinstance(next_event, FieldGoal) and next_event.made):
                        return True
                    next_event = next_event.next_event
            if isinstance(self, EndOfPeriod):
                return True
        return False