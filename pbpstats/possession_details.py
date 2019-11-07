import math

import pbpstats
from pbpstats import utils
from pbpstats.overrides import BAD_PBP_CASES


class TeamHasBackToBackPossessionsException(Exception):
    pass


class PbpEventOrderErrorException(Exception):
    pass


class PossessionDetails(object):
    """
    attributes that get added with Period.set_base_possession_details is called
        - GameId
        - Period
        - PossessionNumber
        - OffenseTeamId
        - DefenseTeamId
        - StartTime - seconds remaining in period at start of possession
        - EndTime - seconds remaining in period at end of possession
        - PreviousPossessionEndEventNum - event number of last event of previous possession
        - EndEventNum - event number for last event of this possession
        - StartScoreDifferential - score differential at start of possession from perspective of the offensive team
        - Events - list of DataPbpEvent or StatsPbpEvent objects for events for current possession
        - PreviousPossessionEvents - list of DataPbpEvent or StatsPbpEvent objects for events for previous possession
        - OffensiveRebounds - number of offensive rebounds on possession
        - SecondChanceTime - time in seconds of possession after offensive rebound
        - PlayerStats - nested dict with player stats for possession - format: {TeamId:{LineupId:{OpponentLineupId:{PlayerId:{StatKey:StatValue}}}}}
        - ShotData - list of dicts with detailed shot data for each shot taken on the possession

    attributes that get added in where possession.add_previous_possession_ending_data() is called:
        - StartType
        - PreviousPossessionEndShooterPlayerId - player who took shot that ended possession (make or miss)
        - PreviousPossessionEndReboundPlayerId - player who got rebound to end previous possession
        - PreviousPossessionEndTurnoverPlayerId - only live ball turnovers
        - PreviousPossessionEndStealPlayerId - player who got steal to end previous possession
    """
    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __repr__(self):
        return f'<PossessionDetails: {self.__dict__}>'

    def add_previous_possession_ending_data(self):
        """
        adds:
            - StartType
            - PreviousPossessionEndShooterPlayerId
            - PreviousPossessionEndReboundPlayerId
            - PreviousPossessionEndTurnoverPlayerId
            - PreviousPossessionEndStealPlayerId
        """
        previous_possession_end_shooter_player_id = 0  # on makes and misses
        previous_possession_end_rebound_player_id = 0
        previous_possession_end_turnover_player_id = 0  # only live ball turnovers
        previous_possession_end_steal_player_id = 0
        start_type = pbpstats.OFF_DEADBALL_STRING
        if self.PossessionNumber == 1:
            start_type = pbpstats.OFF_DEADBALL_STRING
        else:
            has_timeout = self.possession_has_timeout() or self.previous_possession_has_timeout()
            if has_timeout:
                start_type = pbpstats.OFF_TIMEOUT_STRING
            else:
                previous_possession_ending_event = self.get_previous_possession_ending_event()

                if previous_possession_ending_event.is_made_fg():
                    shot_type = previous_possession_ending_event.get_shot_type()
                    start_type = f'Off{shot_type}{pbpstats.MAKE_STRING}'
                    previous_possession_end_shooter_player_id = previous_possession_ending_event.player_id
                elif previous_possession_ending_event.is_made_ft():
                    start_type = pbpstats.OFF_MADE_FT_STRING
                elif previous_possession_ending_event.is_steal():
                    start_type = pbpstats.OFF_LIVE_BALL_TURNOVER_STRING
                    previous_possession_end_steal_player_id = previous_possession_ending_event.player3_id
                    previous_possession_end_turnover_player_id = previous_possession_ending_event.player_id
                elif previous_possession_ending_event.is_turnover():
                    start_type = pbpstats.OFF_DEADBALL_STRING
                elif previous_possession_ending_event.is_rebound():
                    rebound_data = previous_possession_ending_event.get_rebound_data()
                    if rebound_data is not None:
                        if not rebound_data['player_reb']:
                            start_type = pbpstats.OFF_DEADBALL_STRING
                        elif rebound_data['ft']:
                            start_type = pbpstats.OFF_MISSED_FT_STRING
                            previous_possession_end_rebound_player_id = rebound_data['player_id']
                            previous_possession_end_shooter_player_id = rebound_data['rebounded_shot'].player_id
                        else:
                            shot_type = rebound_data['rebounded_shot'].get_shot_type()
                            if rebound_data['rebounded_shot'].is_blocked_shot():
                                start_type = f'Off{shot_type}{pbpstats.BLOCK_STRING}'
                            else:
                                start_type = f'Off{shot_type}{pbpstats.MISS_STRING}'

                            previous_possession_end_rebound_player_id = rebound_data['player_id']
                            previous_possession_end_shooter_player_id = rebound_data['rebounded_shot'].player_id

                elif previous_possession_ending_event.is_jump_ball():
                    # jump balls tipped out of bounds have no player2_id and should be off deadball
                    if previous_possession_ending_event.player2_id not in ['0', '']:
                        start_type = pbpstats.OFF_LIVE_BALL_TURNOVER_STRING
                    else:
                        start_type = pbpstats.OFF_DEADBALL_STRING

        if start_type is None:
            start_type = pbpstats.OFF_DEADBALL_STRING
        self.StartType = start_type
        self.PreviousPossessionEndShooterPlayerId = previous_possession_end_shooter_player_id
        self.PreviousPossessionEndReboundPlayerId = previous_possession_end_rebound_player_id
        self.PreviousPossessionEndTurnoverPlayerId = previous_possession_end_turnover_player_id
        self.PreviousPossessionEndStealPlayerId = previous_possession_end_steal_player_id

    def possession_has_timeout(self):
        """
        checks if there was a timeout called on the current possession
        """
        for i, event in enumerate(self.Events):
            if event.is_timeout() and event.seconds_remaining != self.EndTime:
                # timeout is not at possession end time
                if not (
                    event.next_event is not None and
                    (event.next_event.is_made_ft() or event.next_event.is_missed_ft()) and
                    event.seconds_remaining == event.next_event.seconds_remaining and
                    not event.next_event.is_technical_ft()
                ):
                    # check to make sure timeout is not between/before FTs
                    return True
            elif event.is_timeout() and event.seconds_remaining == self.EndTime:
                timeout_time = event.seconds_remaining
                after_timeout_index = i + 1
                # call time out and turn ball over at same time as timeout following time out
                for possession_event in self.Events[after_timeout_index:]:
                    if possession_event.is_turnover() and possession_event.seconds_remaining == timeout_time:
                        return True
        return False

    def previous_possession_has_timeout(self):
        """
        check for timeout on previous possession - if there is a timeout at the same time as possession end, current possession starts off timeout
        """
        for event in self.PreviousPossessionEvents:
            if event.is_timeout() and event.seconds_remaining == self.StartTime:
                if not (
                    event.next_event is not None and
                    (event.next_event.is_made_ft() or event.next_event.is_missed_ft()) and
                    event.seconds_remaining == event.next_event.seconds_remaining
                ):
                    # check to make sure timeout is not beween FTs
                    return True
        return False

    def get_previous_possession_ending_event(self):
        """
        gets previous possession ending event - ignoring subs
        """
        previous_event_index = -1
        while self.PreviousPossessionEvents[previous_event_index].is_substitution() and len(self.PreviousPossessionEvents) > abs(previous_event_index):
            previous_event_index -= 1
        return self.PreviousPossessionEvents[previous_event_index]

    def add_time_on_floor(self, foul_tracker, penalty_start_events):
        """
        adds time on floor for each player
        time is calculated by taking time on current event and subtracting time on previous event

        foul_tracker - tracks how many fouls player currently has committed to track time played with x fouls
        penalty_start_events - dict with event number when team is in penalty so that penalty stats can be tracked
        """
        for i, event in enumerate(self.Events):
            in_penalty = self.OffenseTeamId != '0' and penalty_start_events[self.OffenseTeamId] is not None and penalty_start_events[self.OffenseTeamId] < event.order
            if not (i == 0 and self.PossessionNumber == 1):
                if i == 0:
                    lineup_ids = utils.generate_lineup_ids(self.PreviousPossessionEvents[-1].current_players)
                    event_seconds = self.PreviousPossessionEvents[-1].seconds_remaining - event.seconds_remaining
                else:
                    lineup_ids = utils.generate_lineup_ids(self.Events[i - 1].current_players)
                    event_seconds = self.Events[i - 1].seconds_remaining - event.seconds_remaining

                if event_seconds > 0:
                    for team_id in lineup_ids.keys():
                        lineup_id = lineup_ids[team_id]
                        opponent_lineup_id = lineup_ids[utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])]

                        if team_id == self.OffenseTeamId:
                            seconds_played_key = pbpstats.SECONDS_PLAYED_OFFENSE_STRING
                        else:
                            seconds_played_key = pbpstats.SECONDS_PLAYED_DEFENSE_STRING

                        for player_id in lineup_id.split('-'):
                            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][seconds_played_key] += event_seconds
                            number_of_fouls = foul_tracker[player_id]
                            period = self.Period if self.Period <= 4 else 'OT'
                            foul_tracking_seconds_played_key = f'Period{period}Fouls{number_of_fouls}{seconds_played_key}'
                            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][foul_tracking_seconds_played_key] += event_seconds
                            if in_penalty:
                                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.PENALTY_STRING + seconds_played_key] += event_seconds
            # need to add foul tracker counts after time gets added so that time with x fouls is correctly added in
            if event.is_foul():
                self.increment_foul_stats(event, foul_tracker, in_penalty)

    def fix_players_on_floor_for_fts(self):
        """
        sets player on floor for FT to be players on floor for foul
        """
        for pbp_event in self.Events:
            if pbp_event.is_made_ft() or pbp_event.is_missed_ft():
                # player on floor for FTs should be players who were on the floor for foul
                foul_event = pbp_event.get_foul_that_resulted_in_ft()
                if foul_event is not None:
                    pbp_event.current_players = foul_event.current_players.copy()

    def add_counting_stats(self, home_team_id, penalty_start_events, rebounded_shots, ignore_rebound_and_shot_order=False):
        """
        iterates though pbp events and checks if event is an event that triggers an increment to stat count
        """
        for pbp_event in self.Events:
            if pbp_event.is_tracked_event():
                in_penalty = penalty_start_events[self.OffenseTeamId] is not None and penalty_start_events[self.OffenseTeamId] < pbp_event.order
                if pbp_event.is_turnover():
                    self.increment_turnover_stats(pbp_event, in_penalty)
                if pbp_event.is_first_ft() or pbp_event.is_technical_ft():
                    self.increment_free_throw_stats(pbp_event, in_penalty)
                if pbp_event.is_made_fg():
                    self.increment_made_fg_counts(pbp_event, home_team_id, in_penalty)
                if pbp_event.is_missed_fg():
                    self.increment_missed_fg_counts(pbp_event, home_team_id, in_penalty)
                if pbp_event.is_made_ft():
                    self.increment_made_ft_counts(pbp_event, in_penalty)
                if pbp_event.is_rebound():
                    self.increment_rebound_counts(pbp_event, in_penalty, rebounded_shots, ignore_rebound_and_shot_order=ignore_rebound_and_shot_order)
                if pbp_event.is_goaltend_violation():
                    self.increment_goaltend_counts(pbp_event)
                if pbp_event.is_replay_challenge_overturn_ruling() or pbp_event.is_replay_challenge_ruling_stands() or pbp_event.is_replay_challenge_support_ruling():
                    self.increment_challenge_counts(pbp_event)

    def increment_turnover_stats(self, pbp_event, in_penalty):
        """
        increments PlayerStats for appropriate players on turnovers
        """
        player_id = pbp_event.player_id
        team_id = pbp_event.team_id
        opponent_team_id = utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])

        lineup_ids = utils.generate_lineup_ids(pbp_event.current_players)

        lineup_id = lineup_ids[team_id]
        opponent_lineup_id = lineup_ids[opponent_team_id]
        second_chance = pbp_event.is_second_chance_event(self.Events)
        stat_keys = []
        if pbp_event.is_steal():
            # live ball turnover
            stat_keys.append(pbpstats.LIVEBALL_TURNOVERS_STRING)

            if pbp_event.is_lost_ball_turnover():
                stat_keys.append(pbpstats.LOST_BALL_TURNOVER_STRING)
            elif pbp_event.is_bad_pass_turnover():
                stat_keys.append(pbpstats.BAD_PASS_TURNOVER_STRING)

            steal_player_id = pbp_event.player3_id
            steal_team_id = utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])

            steal_lineup_id = lineup_ids[steal_team_id]
            steal_opponent_lineup_id = lineup_ids[utils.swap_team_id_for_game(steal_team_id, [self.OffenseTeamId, self.DefenseTeamId])]

            # add steal for player
            if steal_player_id != steal_team_id:
                # bad pbp events have steal player id as team id - ignore it
                self.PlayerStats[steal_team_id][steal_lineup_id][steal_opponent_lineup_id][steal_player_id][pbpstats.STEALS_STRING] += 1
                if second_chance:
                    self.PlayerStats[steal_team_id][steal_lineup_id][steal_opponent_lineup_id][steal_player_id][pbpstats.SECOND_CHANCE_STRING + pbpstats.STEALS_STRING] += 1
                if in_penalty:
                    self.PlayerStats[steal_team_id][steal_lineup_id][steal_opponent_lineup_id][steal_player_id][pbpstats.PENALTY_STRING + pbpstats.STEALS_STRING] += 1

        else:
            # dead ball turnover
            stat_keys.append(pbpstats.DEADBALL_TURNOVERS_STRING)

            if pbp_event.is_travel():
                stat_keys.append(pbpstats.TRAVELS_STRING)
            elif pbp_event.is_3_second_violation():
                stat_keys.append(pbpstats.THREE_SECOND_VIOLATION_TURNOVER_STRING)
            elif pbp_event.is_step_out_of_bounds_turnover():
                stat_keys.append(pbpstats.STEP_OUT_OF_BOUNDS_TURNOVER_STRING)
            elif pbp_event.is_offensive_goaltending():
                stat_keys.append(pbpstats.OFFENSIVE_GOALTENDING_STRING)
            elif pbp_event.is_lost_ball_out_of_bounds_turnover():
                stat_keys.append(pbpstats.LOST_BALL_OUT_OF_BOUNDS_TURNOVER_STRING)
            elif pbp_event.is_bad_pass_out_of_bounds_turnover():
                stat_keys.append(pbpstats.BAD_PASS_OUT_OF_BOUNDS_TURNOVER_STRING)

            events_to_check = self.Events + self.PreviousPossessionEvents
            if player_id != '0' and player_id not in lineup_id.split('-'):
                # sub in wrong order - fix lineup
                for event in events_to_check:
                    if event.is_substitution() and event.seconds_remaining == pbp_event.seconds_remaining:
                        outgoing_player_id = event.player_id
                        incoming_player_id = event.player2_id
                        if outgoing_player_id == player_id:
                            lineup_id = lineup_id.replace(incoming_player_id, outgoing_player_id)
            if player_id != '0' and player_id not in opponent_lineup_id.split('-'):
                # sub in wrong order - fix lineup
                for event in events_to_check:
                    if event.is_substitution() and event.seconds_remaining == pbp_event.seconds_remaining:
                        outgoing_player_id = event.player_id
                        incoming_player_id = event.player2_id
                        if outgoing_player_id == player_id:
                            opponent_lineup_id = opponent_lineup_id.replace(incoming_player_id, outgoing_player_id)

        for stat_key in stat_keys:
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][stat_key] += 1
            if second_chance:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.SECOND_CHANCE_STRING + stat_key] += 1
            if in_penalty:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.PENALTY_STRING + stat_key] += 1

    def increment_rebound_counts(self, pbp_event, in_penalty, rebounded_shots, ignore_rebound_and_shot_order=False):
        """
        increments PlayerStats for appropriate players on rebounds
        counts are split based on shot zone of missed shot and if shot was missed or blocked

        rebounded_shots - list of rebounds for the period - used to check to make sure same shot doesn't get counted as being rebounded twice due to pbp issue
        ignore_rebound_and_shot_order - when True PbpEventOrderErrorException won't be raised when rebound event is not in correct order
        """
        rebound_data = pbp_event.get_rebound_data()
        if not ignore_rebound_and_shot_order:
            if rebound_data is not None and pbp_event.previous_event is not None and not (pbp_event.previous_event.is_missed_fg() or pbp_event.previous_event.is_missed_ft() or pbp_event.previous_event.is_jump_ball()):
                exception_text = (f"Shot And Rebound Out of Order GameId: {self.GameId}, Period: {self.Period}, Event: {pbp_event.previous_event}, Event Num: {pbp_event.number}")
                raise PbpEventOrderErrorException(exception_text)
            if rebound_data is not None and rebound_data['rebounded_shot'].number in rebounded_shots:
                # Shot counted as being rebounded twice to due to pbp events being out of order
                exception_text = (f"Shot And Rebound Out of Order GameId: {self.GameId}, Period: {self.Period}, Event: {rebound_data['rebounded_shot']}, Event Num: {pbp_event.number}")
                raise PbpEventOrderErrorException(exception_text)

        if rebound_data is not None:
            rebounded_shots.append(rebound_data['rebounded_shot'].number)
            if rebound_data['ft']:
                shot_type = pbpstats.FREE_THROW_STRING
            else:
                shot_type = rebound_data['rebounded_shot'].get_shot_type()

            player_id_string = rebound_data['player_id'] if rebound_data['player_reb'] else pbpstats.TEAM_STAT_PLAYER_ID
            rebound_team_id = rebound_data['team_id']
            rebound_opponent_team_id = utils.swap_team_id_for_game(rebound_team_id, [self.OffenseTeamId, self.DefenseTeamId])

            lineup_ids = utils.generate_lineup_ids(pbp_event.current_players)

            rebound_lineup_id = lineup_ids[rebound_team_id]
            rebound_opponent_lineup_id = lineup_ids[rebound_opponent_team_id]

            if rebound_data['rebounded_shot'].is_blocked_shot():
                # check if block was recovered by their team
                if rebound_data['def_reb']:
                    block_player_id = rebound_data['rebounded_shot'].player3_id
                    recovered_key = pbpstats.BLOCKED_STRING + shot_type + 'Recovered'
                    self.PlayerStats[rebound_team_id][rebound_lineup_id][rebound_opponent_lineup_id][block_player_id][recovered_key] += 1

                shot_type += pbpstats.BLOCKED_STRING

            if not rebound_data['def_reb']:
                reb_key = shot_type + pbpstats.OFFENSIVE_ABBREVIATION_PREFIX + pbpstats.REBOUNDS_STRING
                opportunity_key = shot_type + pbpstats.OFFENSIVE_ABBREVIATION_PREFIX + pbpstats.REBOUND_OPPORTUNITIES_STRING
                opponent_opportunity_key = shot_type + pbpstats.DEFENSIVE_ABBREVIATION_PREFIX + pbpstats.REBOUND_OPPORTUNITIES_STRING
                if self.OffensiveRebounds == 0:
                    self.SecondChanceTime = pbp_event.seconds_remaining - self.EndTime
                    for team_id in lineup_ids.keys():
                        lineup_id = lineup_ids[team_id]
                        opponent_lineup_id = lineup_ids[utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])]

                        if team_id == self.OffenseTeamId:
                            seconds_chance_seconds_played_key = pbpstats.SECOND_CHANCE_SECONDS_PLAYED_OFFENSE_STRING
                        else:
                            seconds_chance_seconds_played_key = pbpstats.SECOND_CHANCE_SECONDS_PLAYED_DEFENSE_STRING

                        for player_id in lineup_id.split('-'):
                            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][seconds_chance_seconds_played_key] += pbp_event.seconds_remaining - self.EndTime
                self.OffensiveRebounds += 1
            if rebound_data['def_reb']:
                reb_key = shot_type + pbpstats.DEFENSIVE_ABBREVIATION_PREFIX + pbpstats.REBOUNDS_STRING
                opportunity_key = shot_type + pbpstats.DEFENSIVE_ABBREVIATION_PREFIX + pbpstats.REBOUND_OPPORTUNITIES_STRING
                opponent_opportunity_key = shot_type + pbpstats.OFFENSIVE_ABBREVIATION_PREFIX + pbpstats.REBOUND_OPPORTUNITIES_STRING

            # increment rebound
            self.PlayerStats[rebound_team_id][rebound_lineup_id][rebound_opponent_lineup_id][player_id_string][reb_key] += 1
            if in_penalty:
                self.PlayerStats[rebound_team_id][rebound_lineup_id][rebound_opponent_lineup_id][player_id_string][pbpstats.PENALTY_STRING + reb_key] += 1

            # increment rebound opportunities
            for player_id in rebound_data['current_players'][rebound_team_id]:
                self.PlayerStats[rebound_team_id][rebound_lineup_id][rebound_opponent_lineup_id][player_id][opportunity_key] += 1
                if in_penalty:
                    self.PlayerStats[rebound_team_id][rebound_lineup_id][rebound_opponent_lineup_id][player_id][pbpstats.PENALTY_STRING + opportunity_key] += 1
                if not rebound_data['def_reb']:
                    # add total offensive rebounds for player on floor - used for calculating usage
                    self.PlayerStats[rebound_team_id][rebound_lineup_id][rebound_opponent_lineup_id][player_id][pbpstats.ON_FLOOR_OFFENSIVE_REBOUND_STRING] += 1
                    if in_penalty:
                        self.PlayerStats[rebound_team_id][rebound_lineup_id][rebound_opponent_lineup_id][player_id][pbpstats.PENALTY_STRING + pbpstats.ON_FLOOR_OFFENSIVE_REBOUND_STRING] += 1
            for player_id in rebound_data['current_players'][rebound_opponent_team_id]:
                self.PlayerStats[rebound_opponent_team_id][rebound_opponent_lineup_id][rebound_lineup_id][player_id][opponent_opportunity_key] += 1
                if in_penalty:
                    self.PlayerStats[rebound_opponent_team_id][rebound_opponent_lineup_id][rebound_lineup_id][player_id][pbpstats.PENALTY_STRING + opponent_opportunity_key] += 1

            # increment stats for player missed shot rebounds
            shooter_player_id = rebound_data['rebounded_shot'].player_id
            if shooter_player_id in rebound_data['current_players'][rebound_team_id]:
                missed_shot_rebounded_key = shot_type + pbpstats.OFFENSIVE_ABBREVIATION_PREFIX + pbpstats.REBOUNDED_STRING
                missed_shot_rebounded_opportunity_key = shot_type + pbpstats.OFFENSIVE_ABBREVIATION_PREFIX + pbpstats.REBOUNDED_OPPORTUNITIES_STRING
                self.PlayerStats[rebound_team_id][rebound_lineup_id][rebound_opponent_lineup_id][shooter_player_id][missed_shot_rebounded_key] += 1
                self.PlayerStats[rebound_team_id][rebound_lineup_id][rebound_opponent_lineup_id][shooter_player_id][missed_shot_rebounded_opportunity_key] += 1
            elif shooter_player_id in rebound_data['current_players'][rebound_opponent_team_id]:
                missed_shot_rebounded_opportunity_key = shot_type + pbpstats.OFFENSIVE_ABBREVIATION_PREFIX + pbpstats.REBOUNDED_OPPORTUNITIES_STRING
                self.PlayerStats[rebound_opponent_team_id][rebound_opponent_lineup_id][rebound_lineup_id][shooter_player_id][missed_shot_rebounded_opportunity_key] += 1

    def increment_made_fg_counts(self, pbp_event, home_team_id, in_penalty):
        """
        increments PlayerStats for appropriate players on made FGs - assisted/unassisted by shot zone
        """
        player_id = pbp_event.player_id
        team_id = pbp_event.team_id
        opponent_team_id = utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])
        lineup_ids = utils.generate_lineup_ids(pbp_event.current_players)
        second_chance = pbp_event.is_second_chance_event(self.Events)

        lineup_id = lineup_ids[team_id]
        opponent_lineup_id = lineup_ids[opponent_team_id]

        shot_data = {
            pbpstats.PLAYER_ID_STRING: player_id,
            pbpstats.TEAM_ID_STRING: team_id,
            pbpstats.OPPONENT_TEAM_ID_STRING: opponent_team_id,
            pbpstats.LINEUP_ID_STRING: lineup_id,
            pbpstats.OPPONENT_LINEUP_ID_STRING: opponent_lineup_id,
            pbpstats.MADE_STRING: True,
            'X': pbp_event.loc_x,
            'Y': pbp_event.loc_y,
            pbpstats.TIME_STRING: pbp_event.seconds_remaining,
            'EventNum': pbp_event.number
        }
        shot_type = pbp_event.get_shot_type()
        if shot_type in [pbpstats.CORNER_3_STRING, pbpstats.ARC_3_STRING]:
            shot_data[pbpstats.SHOT_VALUE_STRING] = 3
        else:
            shot_data[pbpstats.SHOT_VALUE_STRING] = 2

        if pbp_event.is_assisted_shot():
            shot_data[pbpstats.ASSISTED_STRING] = True
            shot_data[pbpstats.PUTBACK_STRING] = False
            assist_player_id = pbp_event.player2_id

            scorer_key = pbpstats.ASSISTED_STRING + shot_type
            assist_key = shot_type + pbpstats.ASSISTS_STRING
            # assists to - used for assist networks
            assist_to_key = f'{assist_player_id}:AssistsTo:{player_id}:{shot_type}'

            # add counts for assists that need to be incremented
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][assist_player_id][assist_key] += 1
            if second_chance:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][assist_player_id][pbpstats.SECOND_CHANCE_STRING + assist_key] += 1
            if in_penalty:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][assist_player_id][pbpstats.PENALTY_STRING + assist_key] += 1

            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][assist_player_id][assist_to_key] += 1
            if second_chance:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][assist_player_id][pbpstats.SECOND_CHANCE_STRING + assist_to_key] += 1
            if in_penalty:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][assist_player_id][pbpstats.PENALTY_STRING + assist_to_key] += 1
            shot_data['AssistPlayerId'] = assist_player_id

        else:
            # unassisted shot
            shot_data[pbpstats.ASSISTED_STRING] = False
            scorer_key = pbpstats.UNASSISTED_STRING + shot_type

        # check previous event for putback
        for i, possession_event in enumerate(self.Events):
            if possession_event.number == pbp_event.number:
                possession_event_num = i

        putback = pbp_event.is_putback()

        last_rebound = None
        for i, possession_event in enumerate(self.Events):
            if i < possession_event_num and possession_event.is_rebound():
                last_rebound = possession_event

        if possession_event_num > 0 and last_rebound is not None:
            rebound_data = last_rebound.get_rebound_data()
            if rebound_data is not None:
                if not rebound_data['def_reb']:
                    shot_data[pbpstats.SECONDS_SINCE_OREB_STRING] = last_rebound.seconds_remaining - pbp_event.seconds_remaining
                    shot_data[pbpstats.OREB_SHOT_PLAYER_ID_STRING] = rebound_data['rebounded_shot'].player_id
                    shot_data[pbpstats.OREB_REBOUND_PLAYER_ID_STRING] = rebound_data['player_id']
                    if rebound_data['player_reb']:
                        if rebound_data['ft']:
                            rebound_shot_type = pbpstats.FREE_THROW_STRING
                        else:
                            rebound_shot_type = rebound_data['rebounded_shot'].get_shot_type()

                        if rebound_data['rebounded_shot'].is_blocked_shot():
                            rebound_shot_type += pbpstats.BLOCKED_STRING

                    elif rebound_data['rebounded_shot'].is_blocked_shot():
                        # separate blocked from non blocked because blocked won't have shot clock reset
                        rebound_shot_type = 'TeamBlocked'
                    else:
                        rebound_shot_type = 'Team'

                    shot_data['OrebShotType'] = rebound_shot_type

        shot_data[pbpstats.PUTBACK_STRING] = putback
        if putback:
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.PUTBACKS_STRING] += 1

        self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][scorer_key] += 1
        shot_distance = pbp_event.get_shot_distance()
        if shot_distance is not None:
            if shot_data[pbpstats.SHOT_VALUE_STRING] == 2:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.TOTAL_2PT_SHOT_DISTANCE_STRING] += shot_distance
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.TOTAL_2PT_SHOTS_WITH_DISTANCE] += 1
            elif shot_data[pbpstats.SHOT_VALUE_STRING] == 3:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.TOTAL_3PT_SHOT_DISTANCE_STRING] += shot_distance
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.TOTAL_3PT_SHOTS_WITH_DISTANCE] += 1
                if shot_distance >= pbpstats.HEAVE_DISTANCE_CUTOFF and pbp_event.seconds_remaining < pbpstats.HEAVE_TIME_CUTOFF:
                    self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.HEAVE_MAKES_STRING] += 1

        shot_data['ShotType'] = shot_type
        if second_chance:
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.SECOND_CHANCE_STRING + scorer_key] += 1
        if in_penalty:
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.PENALTY_STRING + scorer_key] += 1

        score_margin = pbp_event.home_score - pbp_event.visitor_score
        if team_id != home_team_id:
            score_margin = -1 * score_margin
        score_margin = score_margin - shot_data[pbpstats.SHOT_VALUE_STRING]
        shot_data['ScoreMargin'] = score_margin
        self.ShotData.append(shot_data)
        # add plus minus and opponent points - used for lineup/wowy stats to get net rating
        for player_id in lineup_ids[team_id].split('-'):
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.PLUS_MINUS_STRING] += shot_data[pbpstats.SHOT_VALUE_STRING]

        for player_id in lineup_ids[opponent_team_id].split('-'):
            self.PlayerStats[opponent_team_id][opponent_lineup_id][lineup_id][player_id][pbpstats.PLUS_MINUS_STRING] -= shot_data[pbpstats.SHOT_VALUE_STRING]
            self.PlayerStats[opponent_team_id][opponent_lineup_id][lineup_id][player_id][pbpstats.OPPONENT_POINTS] += shot_data[pbpstats.SHOT_VALUE_STRING]

    def increment_missed_fg_counts(self, pbp_event, home_team_id, in_penalty):
        """
        increments PlayerStats for appropriate players on missed FGs and if the shot was blocked increments block stats
        """
        player_id = pbp_event.player_id
        team_id = pbp_event.team_id
        opponent_team_id = utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])
        lineup_ids = utils.generate_lineup_ids(pbp_event.current_players)
        second_chance = pbp_event.is_second_chance_event(self.Events)

        lineup_id = lineup_ids[team_id]
        opponent_lineup_id = lineup_ids[utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])]

        loc_x_int = pbp_event.loc_x
        loc_y_int = pbp_event.loc_y
        shot_data = {
            pbpstats.PLAYER_ID_STRING: player_id,
            pbpstats.TEAM_ID_STRING: team_id,
            pbpstats.OPPONENT_TEAM_ID_STRING: opponent_team_id,
            pbpstats.LINEUP_ID_STRING: lineup_id,
            pbpstats.OPPONENT_LINEUP_ID_STRING: opponent_lineup_id,
            pbpstats.MADE_STRING: False,
            'X': loc_x_int,
            'Y': loc_y_int,
            pbpstats.TIME_STRING: pbp_event.seconds_remaining,
            'EventNum': pbp_event.number
        }

        shot_type = pbp_event.get_shot_type()
        if shot_type in [pbpstats.CORNER_3_STRING, pbpstats.ARC_3_STRING]:
            shot_data[pbpstats.SHOT_VALUE_STRING] = 3
        else:
            shot_data[pbpstats.SHOT_VALUE_STRING] = 2

        shooter_key = pbpstats.MISSED_STRING + shot_type

        is_blocked = pbp_event.is_blocked_shot()
        if is_blocked:
            block_player_id = pbp_event.player3_id
            block_team_id = utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])

            block_lineup_id = opponent_lineup_id
            block_opponent_lineup_id = lineup_id

            block_key = pbpstats.BLOCKED_STRING + shot_type
            shooter_key = shot_type + pbpstats.BLOCKED_STRING

        # check previous event for putback
        for i, possession_event in enumerate(self.Events):
            if possession_event.number == pbp_event.number:
                possession_event_num = i

        putback = pbp_event.is_putback()

        last_rebound = None
        for i, possession_event in enumerate(self.Events):
            if i < possession_event_num and possession_event.is_rebound():
                last_rebound = possession_event

        if possession_event_num > 0 and last_rebound is not None:
            rebound_data = last_rebound.get_rebound_data()
            if rebound_data is not None and not rebound_data['def_reb']:
                shot_data[pbpstats.SECONDS_SINCE_OREB_STRING] = last_rebound.seconds_remaining - pbp_event.seconds_remaining
                shot_data[pbpstats.OREB_SHOT_PLAYER_ID_STRING] = rebound_data['rebounded_shot'].player_id
                shot_data[pbpstats.OREB_REBOUND_PLAYER_ID_STRING] = rebound_data['player_id']
                if rebound_data['player_reb']:
                    if rebound_data['ft']:
                        rebound_shot_type = pbpstats.FREE_THROW_STRING
                    else:
                        rebound_shot_type = rebound_data['rebounded_shot'].get_shot_type()

                    if rebound_data['rebounded_shot'].is_blocked_shot():
                        rebound_shot_type += pbpstats.BLOCKED_STRING
                elif rebound_data['rebounded_shot'].is_blocked_shot():
                    # separate blocked from non blocked because blocked won't have shot clock reset
                    rebound_shot_type = 'TeamBlocked'
                else:
                    rebound_shot_type = 'Team'

                shot_data['OrebShotType'] = rebound_shot_type

        shot_data['Blocked'] = is_blocked
        if is_blocked:
            shot_data['BlockPlayerId'] = block_player_id
            self.PlayerStats[block_team_id][block_lineup_id][block_opponent_lineup_id][block_player_id][block_key] += 1
            if second_chance:
                self.PlayerStats[block_team_id][block_lineup_id][block_opponent_lineup_id][block_player_id][pbpstats.SECOND_CHANCE_STRING + block_key] += 1

        shot_data[pbpstats.PUTBACK_STRING] = putback
        shot_data['ShotType'] = shot_type
        score_margin = pbp_event.home_score - pbp_event.visitor_score
        if team_id != home_team_id:
            score_margin = -1 * score_margin
        shot_data['ScoreMargin'] = score_margin
        self.ShotData.append(shot_data)
        self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][shooter_key] += 1

        shot_distance = pbp_event.get_shot_distance()
        if shot_distance is not None:
            if shot_data[pbpstats.SHOT_VALUE_STRING] == 2:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.TOTAL_2PT_SHOT_DISTANCE_STRING] += shot_distance
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.TOTAL_2PT_SHOTS_WITH_DISTANCE] += 1
            elif shot_data[pbpstats.SHOT_VALUE_STRING] == 3:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.TOTAL_3PT_SHOT_DISTANCE_STRING] += shot_distance
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.TOTAL_3PT_SHOTS_WITH_DISTANCE] += 1
                if shot_distance >= pbpstats.HEAVE_DISTANCE_CUTOFF and pbp_event.seconds_remaining < pbpstats.HEAVE_TIME_CUTOFF:
                    self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.HEAVE_MISSES_STRING] += 1

        if second_chance:
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.SECOND_CHANCE_STRING + shooter_key] += 1

        if in_penalty:
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.PENALTY_STRING + shooter_key] += 1

    def increment_made_ft_counts(self, pbp_event, in_penalty):
        """
        increments PlayerStats for appropriate players on made FTs
        """
        player_id = pbp_event.player_id
        team_id = pbp_event.team_id
        opponent_team_id = utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])

        lineup_ids = utils.generate_lineup_ids(pbp_event.current_players)

        lineup_id = lineup_ids[team_id]
        opponent_lineup_id = lineup_ids[opponent_team_id]
        second_chance = pbp_event.is_second_chance_event(self.Events)

        foul_event = pbp_event.get_foul_that_resulted_in_ft_excluding_techs()
        if foul_event is None:
            # free throws to begin quarter with no foul event in pbp
            take_foul = False
        else:
            foul_type = foul_event.get_foul_type()
            take_foul = foul_type == pbpstats.PERSONAL_TAKE_TYPE_STRING

        self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.FTS_MADE_STRING] += 1
        if second_chance:
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.SECOND_CHANCE_STRING + pbpstats.FTS_MADE_STRING] += 1
        if in_penalty:
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.PENALTY_STRING + pbpstats.FTS_MADE_STRING] += 1
            if take_foul and pbp_event.seconds_remaining < 60 and self.Period >= 4:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.FINAL_MINUTE_PENALTY_TAKE_FOUL_STRING + pbpstats.FTS_MADE_STRING] += 1

        # add plus minus and opponent points - used for lineup/wowy stats to get net rating
        for player_id in lineup_ids[team_id].split('-'):
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.PLUS_MINUS_STRING] += 1

        for player_id in lineup_ids[opponent_team_id].split('-'):
            self.PlayerStats[opponent_team_id][opponent_lineup_id][lineup_id][player_id][pbpstats.PLUS_MINUS_STRING] -= 1
            self.PlayerStats[opponent_team_id][opponent_lineup_id][lineup_id][player_id][pbpstats.OPPONENT_POINTS] += 1

    def increment_foul_stats(self, pbp_event, foul_tracker, in_penalty):
        """
        increments PlayerStats for appropriate players on fouls committed and drawn by foul type
        """
        foul_type = pbp_event.get_foul_type()
        if foul_type is not None and not pbp_event.is_technical_foul() and not pbp_event.is_double_technical_foul():
            player_id = pbp_event.player_id
            team_id = pbp_event.team_id
            opponent_team_id = utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])

            lineup_ids = utils.generate_lineup_ids(pbp_event.current_players)

            lineup_id = lineup_ids[team_id]
            opponent_lineup_id = lineup_ids[opponent_team_id]

            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][foul_type] += 1
            if in_penalty:
                self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.PENALTY_STRING + foul_type] += 1
            if foul_type != pbpstats.DEFENSIVE_3_SECONDS_FOUL_TYPE_STRING:
                foul_tracker[player_id] += 1
            # player3_id is player who drew foul, for double foul they are commiting a foul as well so track that
            if foul_type == pbpstats.DOUBLE_FOUL_TYPE_STRING:
                player3_id_stat_key = foul_type
            else:
                player3_id_stat_key = foul_type + pbpstats.FOULS_DRAWN_TYPE_STRING

            player3_id = pbp_event.player3_id
            if player3_id in lineup_id.split('-'):
                foul_drawing_team_id = team_id
                foul_drawing_lineup_id = lineup_id
                foul_drawing_opponent_lineup_id = opponent_lineup_id
                increment_counts = True
            elif player3_id in opponent_lineup_id.split('-'):
                foul_drawing_team_id = opponent_team_id
                foul_drawing_lineup_id = opponent_lineup_id
                foul_drawing_opponent_lineup_id = lineup_id
                increment_counts = True
            else:
                increment_counts = False
            if increment_counts:
                self.PlayerStats[foul_drawing_team_id][foul_drawing_lineup_id][foul_drawing_opponent_lineup_id][player3_id][player3_id_stat_key] += 1
                if in_penalty:
                    self.PlayerStats[foul_drawing_team_id][foul_drawing_lineup_id][foul_drawing_opponent_lineup_id][player3_id][pbpstats.PENALTY_STRING + player3_id_stat_key] += 1

    def increment_free_throw_stats(self, pbp_event, in_penalty):
        """
        increments PlayerStats for appropriate players for foul that led to free throws:
            - 2pt shooting fouls
            - 2pt and 1s
            - 3pt shooting fouls
            - 3pt and 1s
            - penalty
            - technical
            - flagrant
            - away from play
        """
        player_id = pbp_event.player_id
        team_id = pbp_event.team_id
        opponent_team_id = utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])

        lineup_ids = utils.generate_lineup_ids(pbp_event.current_players)

        lineup_id = lineup_ids[team_id]
        opponent_lineup_id = lineup_ids[opponent_team_id]
        second_chance = pbp_event.is_second_chance_event(self.Events)

        if pbp_event.is_first_ft():
            foul_event = pbp_event.get_foul_that_resulted_in_ft_excluding_techs()
            if foul_event is None:
                # free throws to begin quarter with no foul event in pbp
                num_fts = pbp_event.get_number_of_fta_for_foul()
                free_throw_type = f"{num_fts} Shot Unknown Free Throw Trips"
            else:
                foul_type = foul_event.get_foul_type()
                if foul_type in [pbpstats.SHOOTING_FOUL_TYPE_STRING, pbpstats.SHOOTING_BLOCK_TYPE_STRING]:
                    # check if 1, 2 or 3 shots
                    num_fts = foul_event.get_number_of_fta_for_foul()
                    if num_fts == 1:
                        # and 1
                        and1_shot = foul_event.get_and1_shot()
                        if and1_shot is None:
                            # bug - not an actual shooting foul - away from play foul
                            free_throw_type = '1 Shot Away From Play Free Throw Trips'
                        elif and1_shot.is_3pt_shot():
                            if and1_shot.player_id == pbp_event.player_id:
                                free_throw_type = pbpstats.THREE_POINT_AND1_FREE_THROW_STRING
                            else:
                                # sometimes away from play foul on made fg by other player is called a shooting foul
                                free_throw_type = '1 Shot Away From Play Free Throw Trips'
                        else:
                            if and1_shot.player_id == pbp_event.player_id:
                                free_throw_type = pbpstats.TWO_POINT_AND1_FREE_THROW_STRING
                            else:
                                # sometimes away from play foul on made fg by other player is called a shooting foul
                                free_throw_type = '1 Shot Away From Play Free Throw Trips'
                    else:
                        free_throw_type = f"{num_fts}pt Shooting Foul Free Throw Trips"
                elif foul_type in [pbpstats.FLAGRANT_1_FOUL_TYPE_STRING, pbpstats.FLAGRANT_2_FOUL_TYPE_STRING]:
                    num_fts = foul_event.get_number_of_fta_for_foul()
                    if num_fts is None:
                        # assume 2 shot flagrant if num_fts is None
                        num_fts = 2
                    free_throw_type = f"{num_fts} Shot Flagrant Free Throw Trips"
                elif foul_type == pbpstats.AWAY_FROM_PLAY_FOUL_TYPE_STRING:
                    num_fts = foul_event.get_number_of_fta_for_foul()
                    free_throw_type = f"{num_fts} Shot Away From Play Free Throw Trips"
                elif foul_type == pbpstats.INBOUND_FOUL_TYPE_STRING:
                    num_fts = foul_event.get_number_of_fta_for_foul()
                    free_throw_type = f"{num_fts} Shot Inbound Foul Free Throw Trips"
                else:
                    # penalty
                    # check for 3 shots since sometimes shooting fouls are counted as personal fouls - can't really fix for 2 shot fouls but can for 3
                    num_fts = foul_event.get_number_of_fta_for_foul()
                    if num_fts == 3:
                        free_throw_type = pbpstats.THREE_POINT_SHOOTING_FOUL_FREE_THROW_STRING
                    elif num_fts == 1:
                        and1_shot = foul_event.get_and1_shot()
                        if and1_shot is not None:
                            if player_id == and1_shot.player_id:
                                if and1_shot.is_3pt_shot():
                                    free_throw_type = pbpstats.THREE_POINT_AND1_FREE_THROW_STRING
                                else:
                                    free_throw_type = pbpstats.TWO_POINT_AND1_FREE_THROW_STRING
                            else:
                                free_throw_type = '1 Shot Away From Play Free Throw Trips'
                        else:
                            free_throw_type = '1 Shot Away From Play Free Throw Trips'
                    else:
                        free_throw_type = pbpstats.PENALTY_FREE_THROW_STRING

        elif pbp_event.is_technical_ft():
            free_throw_type = pbpstats.TECHNICAL_FREE_THROW_STRING

        self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][free_throw_type] += 1
        if second_chance:
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.SECOND_CHANCE_STRING + free_throw_type] += 1
        if in_penalty:
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.PENALTY_STRING + free_throw_type] += 1

    def increment_goaltend_counts(self, pbp_event):
        """
        increments PlayerStats for appropriate players for goaltend violations
        """
        player_id = pbp_event.player_id
        team_id = pbp_event.team_id
        opponent_team_id = utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])

        lineup_ids = utils.generate_lineup_ids(pbp_event.current_players)

        lineup_id = lineup_ids[team_id]
        opponent_lineup_id = lineup_ids[opponent_team_id]
        second_chance = pbp_event.is_second_chance_event(self.Events)

        self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.DEFENSIVE_GOALTENDING_STRING] += 1
        if second_chance:
            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][pbpstats.SECOND_CHANCE_STRING + pbpstats.DEFENSIVE_GOALTENDING_STRING] += 1

    def increment_challenge_counts(self, pbp_event):
        """
        increments PlayerStats for appropriate coaches challenge
        """
        event = pbp_event
        while event is not None and pbp_event.seconds_remaining == event.seconds_remaining and not event.is_timeout():
            event = event.previous_event
        if event is not None and event.is_timeout():
            # use timeout event because team isn't in the replay event
            player_id = pbpstats.TEAM_STAT_PLAYER_ID
            team_id = event.team_id
            opponent_team_id = utils.swap_team_id_for_game(team_id, [self.OffenseTeamId, self.DefenseTeamId])

            lineup_ids = utils.generate_lineup_ids(event.current_players)
            lineup_id = lineup_ids[team_id]
            opponent_lineup_id = lineup_ids[opponent_team_id]

            if pbp_event.is_replay_challenge_overturn_ruling():
                stat_key = pbpstats.CHALLENGE_OVERTURN_RULING_STRING
            elif pbp_event.is_replay_challenge_ruling_stands():
                stat_key = pbpstats.CHALLENGE_RULING_STANDS_STRING
            elif pbp_event.is_replay_challenge_support_ruling():
                stat_key = pbpstats.CHALLENGE_SUPPORT_RULING_STRING

            self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id][stat_key] += 1

    def add_possessions(self, penalty_start_events, previous_possession_details=None, ignore_back_to_back_possessions=False):
        """
        increments PlayerStats for appropriate players for offensive and defensive possessions
        possession is counted for players who finished possession on the floor
        any possession starting in final 2 seconds on which no points are scored won't be counted as a possession
        set ignore_back_to_back_possessions to True to avoid raising possession_details.TeamHasBackToBackPossessionsException
        """
        # don't count as possession if it startered in last second of period
        count_possession = True
        if math.floor(self.StartTime) <= 2:
            count_possession = False
            # only count possessions that start with 1 second or less remaining if there were points scored
            for event in self.Events:
                if event.is_made_fg() or event.is_made_ft() or event.is_missed_ft():
                    count_possession = True
        if count_possession:
            # check that team does not have back to back possessions
            # cases where team can have back to back possessions:
            # - flagrant fouls
            # - double lane violation on ft and win jump ball
            offense_team_id = self.OffenseTeamId
            defense_team_id = self.DefenseTeamId

            if not ignore_back_to_back_possessions:
                try:
                    bad_pbp_case = False
                    if self.GameId in BAD_PBP_CASES.keys():
                        if str(self.Period) in BAD_PBP_CASES[self.GameId].keys():
                            if self.PossessionNumber in BAD_PBP_CASES[self.GameId][str(self.Period)]:
                                bad_pbp_case = True

                    if self.PossessionNumber > 1 and previous_possession_details.OffenseTeamId == offense_team_id and not bad_pbp_case:
                        previous_possession_has_flagrant = False
                        previous_possession_lane_violation = False
                        current_possession_jump_ball_win = False

                        for event in self.PreviousPossessionEvents:
                            if event.get_foul_type() in [pbpstats.FLAGRANT_1_FOUL_TYPE_STRING, pbpstats.FLAGRANT_2_FOUL_TYPE_STRING]:
                                previous_possession_has_flagrant = True

                            if event.is_turnover() and 'Lane Violation' in event.description and event.team_id == offense_team_id:
                                previous_possession_lane_violation = True

                        for event in self.Events:
                            if event.is_jump_ball() and event.team_id == offense_team_id:
                                current_possession_jump_ball_win = True

                        for event in previous_possession_details.PreviousPossessionEvents:
                            if event.get_foul_type() in [pbpstats.FLAGRANT_1_FOUL_TYPE_STRING, pbpstats.FLAGRANT_2_FOUL_TYPE_STRING]:
                                if event.team_id != offense_team_id:
                                    previous_possession_has_flagrant = True

                        if not previous_possession_has_flagrant and not (previous_possession_lane_violation and current_possession_jump_ball_win):
                            exception_text = f'GameId: {self.GameId}, Period: {self.Period}, Number: {self.PossessionNumber}, Previous Events: {self.PreviousPossessionEvents}, Events: {self.Events}'
                            raise TeamHasBackToBackPossessionsException(exception_text)
                except:
                    exception_text = f'GameId: {self.GameId}, Period: {self.Period}, Number: {self.PossessionNumber}, Previous Events: {self.PreviousPossessionEvents}, Events: {self.Events}'
                    raise TeamHasBackToBackPossessionsException(exception_text)

            lineup_ids = utils.generate_lineup_ids(self.Events[-1].current_players)
            offense_lineup_id = lineup_ids[offense_team_id]
            defense_lineup_id = lineup_ids[defense_team_id]

            in_penalty = penalty_start_events[offense_team_id] is not None and penalty_start_events[offense_team_id] < self.Events[-1].order
            if in_penalty:
                has_take_foul_ft_made = self.is_final_minute_penalty_take_foul_possession()

            for player_id in offense_lineup_id.split('-'):
                self.PlayerStats[offense_team_id][offense_lineup_id][defense_lineup_id][player_id][pbpstats.OFFENSIVE_POSSESSION_STRING] += 1
                if self.OffensiveRebounds > 0:
                    self.PlayerStats[offense_team_id][offense_lineup_id][defense_lineup_id][player_id][pbpstats.SECOND_CHANCE_STRING + pbpstats.OFFENSIVE_POSSESSION_STRING] += 1
                if in_penalty:
                    self.PlayerStats[offense_team_id][offense_lineup_id][defense_lineup_id][player_id][pbpstats.PENALTY_STRING + pbpstats.OFFENSIVE_POSSESSION_STRING] += 1
                    if has_take_foul_ft_made:
                        self.PlayerStats[offense_team_id][offense_lineup_id][defense_lineup_id][player_id][pbpstats.FINAL_MINUTE_PENALTY_TAKE_FOUL_STRING + pbpstats.OFFENSIVE_POSSESSION_STRING] += 1

            for player_id in defense_lineup_id.split('-'):
                self.PlayerStats[defense_team_id][defense_lineup_id][offense_lineup_id][player_id][pbpstats.DEFENSIVE_POSSESSION_STRING] += 1
                if self.OffensiveRebounds > 0:
                    self.PlayerStats[defense_team_id][defense_lineup_id][offense_lineup_id][player_id][pbpstats.SECOND_CHANCE_STRING + pbpstats.DEFENSIVE_POSSESSION_STRING] += 1
                if in_penalty:
                    self.PlayerStats[defense_team_id][defense_lineup_id][offense_lineup_id][player_id][pbpstats.PENALTY_STRING + pbpstats.DEFENSIVE_POSSESSION_STRING] += 1
                    if has_take_foul_ft_made:
                        self.PlayerStats[defense_team_id][defense_lineup_id][offense_lineup_id][player_id][pbpstats.FINAL_MINUTE_PENALTY_TAKE_FOUL_STRING + pbpstats.DEFENSIVE_POSSESSION_STRING] += 1

    def is_final_minute_penalty_take_foul_possession(self):
        """
        checks if there was a take foul FT made on possession so that it can be counted as a possession
        """
        for team_id in self.PlayerStats.keys():
            for lineup_id in self.PlayerStats[team_id].keys():
                for opponent_lineup_id in self.PlayerStats[team_id][lineup_id].keys():
                    for player_id in self.PlayerStats[team_id][lineup_id][opponent_lineup_id].keys():
                        if pbpstats.FINAL_MINUTE_PENALTY_TAKE_FOUL_STRING + pbpstats.FTS_MADE_STRING in self.PlayerStats[team_id][lineup_id][opponent_lineup_id][player_id].keys():
                            return True
        return False
