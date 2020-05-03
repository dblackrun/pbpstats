import abc

import pbpstats
from pbpstats.resources.enhanced_pbp import FieldGoal, Foul, FreeThrow, Rebound


class EnhancedPbpItem(metaclass=abc.ABCMeta):
    def __repr__(self):
        return f"<{type(self).__name__} GameId: {self.game_id}, Description: {self.description}, Time: {self.clock}, EventNum: {self.event_num}>"

    @abc.abstractproperty
    def is_possession_ending_event(self):
        pass

    @abc.abstractproperty
    def event_stats(self):
        pass

    @abc.abstractmethod
    def get_offense_team_id(self):
        pass

    @property
    def base_stats(self):
        """
        these are event stats for all event types
        - seconds played off/def
        - possession off/def
        """
        return self._get_seconds_played_stats_items() + self._get_possessions_played_stats_items()

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
    def score_margin(self):
        """
        from perspective of offense team
        """
        if self.previous_event is None:
            score = self.score
        else:
            score = self.previous_event.score
        offense_team_id = self.get_offense_team_id()
        offense_points = score[offense_team_id]
        defense_points = 0
        for team_id, points in score.items():
            if team_id != offense_team_id:
                defense_points = points
        return offense_points - defense_points

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
    def seconds_since_previous_event(self):
        if self.previous_event is None:
            return 0
        return self.previous_event.seconds_remaining - self.seconds_remaining

    def is_second_chance_event(self):
        event = self.previous_event
        if isinstance(event, Rebound) and event.is_real_rebound and event.oreb:
            return True
        while not (event is None or event.is_possession_ending_event):
            if isinstance(event, Rebound) and event.is_real_rebound and event.oreb:
                return True
            event = event.previous_event
        return False

    def is_penalty_event(self):
        if hasattr(self, 'fouls_to_give'):
            team_ids = list(self.current_players.keys())
            offense_team_id = self.get_offense_team_id()
            defense_team_id = team_ids[0] if offense_team_id == team_ids[1] else team_ids[1]
            if self.fouls_to_give[defense_team_id] == 0:
                if isinstance(self, (Foul, FreeThrow, Rebound)):
                    # if foul or free throw or rebound on a missed ft
                    # check foul event and should return false is foul
                    # was shooting foul and team had a foul to give
                    if isinstance(self, Foul):
                        foul_event = self
                    elif isinstance(self, FreeThrow):
                        foul_event = self.foul_that_led_to_ft
                    else:
                        # if rebound is on missed ft, also need to look at foul that led to FT
                        if not self.oreb and isinstance(self.missed_shot, FreeThrow):
                            foul_event = self.missed_shot.foul_that_led_to_ft
                        else:
                            return True
                    if foul_event is None:
                        return True
                    fouls_to_give_prior_to_foul = foul_event.previous_event.fouls_to_give[defense_team_id]
                    if fouls_to_give_prior_to_foul > 0:
                        return False
                return True
        return False

    @property
    def count_as_possession(self):
        """
        don't count possession change if it starts with <= 2 seconds left
        and no points are scored before period ends
        """
        if self.is_possession_ending_event:
            if self.seconds_remaining > 2:
                return True
            # check when previous possession ended
            prev_event = self.previous_event
            while prev_event is not None and not prev_event.is_possession_ending_event:
                prev_event = prev_event.previous_event
            if prev_event is None or prev_event.seconds_remaining > 2:
                return True
            # possession starts in final 2 seconds
            # return True if there is a FT or FGM between now and end of period
            next_event = prev_event.next_event
            while next_event is not None:
                if isinstance(next_event, FreeThrow) or (isinstance(next_event, FieldGoal) and next_event.is_made):
                    return True
                next_event = next_event.next_event
        return False

    def _get_seconds_played_stats_items(self):
        """
        makes event stats items for:
        - seconds played
        - seconds played for number of fouls
        - second chance seconds played
        - penalty seconds played
        """
        stat_items = []
        team_ids = list(self.current_players.keys())
        offense_team_id = self.get_offense_team_id()
        is_penalty_event = self.is_penalty_event()
        is_second_chance_event = self.is_second_chance_event()
        if self.seconds_since_previous_event != 0:
            for team_id, players in self.previous_event.current_players.items():
                seconds_stat_key = (
                    pbpstats.SECONDS_PLAYED_OFFENSE_STRING
                    if team_id == offense_team_id
                    else pbpstats.SECONDS_PLAYED_DEFENSE_STRING
                )
                opponent_team_id = team_ids[0] if team_id == team_ids[1] else team_ids[1]
                previous_poss_lineup_ids = self.previous_event.lineup_ids
                for player_id in players:
                    keys_to_add = [seconds_stat_key]
                    player_fouls = self.previous_event.player_game_fouls[player_id]
                    period = self.period if self.period <= 4 else 'OT'
                    foul_tracking_seconds_stat_key = f'Period{period}Fouls{player_fouls}{seconds_stat_key}'
                    keys_to_add.append(foul_tracking_seconds_stat_key)
                    if is_second_chance_event:
                        seconds_chance_seconds_stat_key = f'{pbpstats.SECOND_CHANCE_STRING}{seconds_stat_key}'
                        keys_to_add.append(seconds_chance_seconds_stat_key)
                    if is_penalty_event:
                        penalty_seconds_stat_key = f'{pbpstats.PENALTY_STRING}{seconds_stat_key}'
                        keys_to_add.append(penalty_seconds_stat_key)
                    for stat_key in keys_to_add:
                        stat_item = {
                            'player_id': player_id,
                            'team_id': team_id,
                            'opponent_team_id': opponent_team_id,
                            'lineup_id': previous_poss_lineup_ids[team_id],
                            'opponent_lineup_id': previous_poss_lineup_ids[opponent_team_id],
                            'stat_key': stat_key,
                            'stat_value': self.seconds_since_previous_event,
                        }
                        stat_items.append(stat_item)
        return stat_items

    def _get_possessions_played_stats_items(self):
        """
        makes event stats items for:
        - possessions played
        - second chance possessions played
        - penalty possessions played
        """
        stat_items = []
        team_ids = list(self.current_players.keys())
        offense_team_id = self.get_offense_team_id()
        is_penalty_event = self.is_penalty_event()
        is_second_chance_event = self.is_second_chance_event()
        if self.count_as_possession:
            if isinstance(self, FreeThrow):
                current_players = self.event_for_efficiency_stats.current_players
                lineup_ids = self.event_for_efficiency_stats.lineup_ids
            else:
                current_players = self.current_players
                lineup_ids = self.lineup_ids
            for team_id, players in current_players.items():
                possessions_stat_key = (
                    pbpstats.OFFENSIVE_POSSESSION_STRING
                    if team_id == offense_team_id
                    else pbpstats.DEFENSIVE_POSSESSION_STRING
                )
                opponent_team_id = team_ids[0] if team_id == team_ids[1] else team_ids[1]
                for player_id in players:
                    keys_to_add = [possessions_stat_key]
                    if is_second_chance_event:
                        seconds_chance_possessions_stat_key = f'{pbpstats.SECOND_CHANCE_STRING}{possessions_stat_key}'
                        keys_to_add.append(seconds_chance_possessions_stat_key)
                    if is_penalty_event:
                        penalty_possessions_stat_key = f'{pbpstats.PENALTY_STRING}{possessions_stat_key}'
                        keys_to_add.append(penalty_possessions_stat_key)
                    for stat_key in keys_to_add:
                        stat_item = {
                            'player_id': player_id,
                            'team_id': team_id,
                            'opponent_team_id': opponent_team_id,
                            'lineup_id': lineup_ids[team_id],
                            'opponent_lineup_id': lineup_ids[opponent_team_id],
                            'stat_key': stat_key,
                            'stat_value': 1,
                        }
                        stat_items.append(stat_item)

        return stat_items
