import math

import pbpstats
from pbpstats.resources.enhanced_pbp import Foul, FreeThrow, Turnover, Violation


class FieldGoal(object):
    event_type = [1, 2]

    @property
    def is_made(self):
        return self.event_type == 1

    @property
    def is_blocked(self):
        return not self.is_made and hasattr(self, 'player3_id')

    @property
    def is_assisted(self):
        return self.is_made and hasattr(self, 'player2_id')

    @property
    def rebound(self):
        if not self.is_made and self.next_event.is_real_rebound:
            return self.next_event
        return None

    @property
    def is_heave(self):
        return self.distance > pbpstats.HEAVE_DISTANCE_CUTOFF and self.seconds_remaining < pbpstats.HEAVE_TIME_CUTOFF

    @property
    def is_corner_3(self):
        if self.shot_value != 3:
            return False
        if not hasattr(self, 'locY') or self.locY is None:
            return False
        if self.locY <= 87:
            return True
        return False

    @property
    def distance(self):
        if hasattr(self, 'locX') and hasattr(self, 'locY'):
            x_squared = self.locX ** 2
            y_squared = self.locY ** 2
            # unit for distance is off by factor of 10, divide by 10 to convert to feet
            shot_distance = math.sqrt(x_squared + y_squared) / 10
            return round(shot_distance, 1)
        else:
            # no coordinates - get shot distance from event description
            try:
                return int(self.description.split("'")[0].split(' ')[-1])
            except:
                return None

    @property
    def shot_type(self):
        if self.shot_value == 3:
            if self.is_corner_3:
                return pbpstats.CORNER_3_STRING
            else:
                return pbpstats.ARC_3_STRING

        if self.distance is None:
            return pbpstats.UNKNOWN_SHOT_DISTANCE_STRING
        elif self.distance < pbpstats.AT_RIM_CUTOFF:
            return pbpstats.AT_RIM_STRING
        elif self.distance < pbpstats.SHORT_MID_RANGE_CUTOFF:
            return pbpstats.SHORT_MID_RANGE_STRING
        else:
            return pbpstats.LONG_MID_RANGE_STRING

    @property
    def is_putback(self):
        if self.is_assisted or self.shot_value == 3:
            return False
        prev_evt = self.previous_event
        if prev_evt is None:
            return False
        prev_evt_is_shooting_foul = isinstance(prev_evt, Foul) and (prev_evt.is_shooting_foul or prev_evt.is_shooting_block_foul)
        prev_evt_is_goaltend = isinstance(prev_evt, Violation) and prev_evt.is_goaltend_violation
        if (prev_evt_is_shooting_foul or prev_evt_is_goaltend) and self.clock == prev_evt.clock:
            # sometimes foul event is between rebound and shot on an and 1 or goaltend is between rebound and made shot event
            prev_evt = prev_evt.previous_event
            if prev_evt is None:
                return False
        if not hasattr(prev_evt, 'is_real_rebound'):
            return False
        if not prev_evt.is_real_rebound:
            return False
        return (
            prev_evt.oreb and
            prev_evt.player1_id == self.player1_id and
            prev_evt.seconds_remaining - self.seconds_remaining <= 2
        )

    @property
    def shot_data(self):
        team_ids = list(self.current_players.keys())
        opponent_team_id = team_ids[0] if self.team_id == team_ids[1] else team_ids[1]
        shot_data = {
            'PlayerId': self.player1_id,
            'TeamId': self.team_id,
            'OpponentTeamId': opponent_team_id,
            'LineupId': self.lineup_ids[self.team_id],
            'OpponentLineupId': self.lineup_ids[opponent_team_id],
            'Made': self.is_made,
            'X': self.locX,
            'Y': self.locY,
            'Time': self.seconds_remaining,
            'ShotValue': self.shot_value,
            'Putback': self.is_putback,
            'ShotType': self.shot_type,
            'ScoreMargin': self.score_margin,
            'EventNum': self.event_num
        }
        if self.is_made:
            shot_data['Assisted'] = self.is_assisted
            if self.is_assisted:
                shot_data['AssistPlayerId'] = self.player2_id
        if not self.is_made:
            shot_data['Blocked'] = self.is_blocked
            if self.is_blocked:
                shot_data['BlockPlayerId'] = self.player3_id
        if self.is_second_chance_event():
            prev_event = self.previous_event
            while not (hasattr(prev_event, 'is_real_rebound') and prev_event.is_real_rebound):
                prev_event = prev_event.previous_event
            shot_data['SecondsSinceOReb'] = prev_event.seconds_remaining - self.seconds_remaining
            shot_data['OrebShotPlayerId'] = prev_event.missed_shot.player1_id
            shot_data['OrebReboundPlayerId'] = prev_event.player1_id
            if prev_event.player1_id != 0:
                rebound_shot_type = prev_event.missed_shot.shot_type
                if isinstance(prev_event.missed_shot, FieldGoal) and prev_event.missed_shot.is_blocked:
                    rebound_shot_type += pbpstats.BLOCKED_STRING
            elif isinstance(prev_event.missed_shot, FieldGoal) and prev_event.missed_shot.is_blocked:
                # separate blocked from non blocked because blocked won't have shot clock reset
                rebound_shot_type = 'TeamBlocked'
            else:
                rebound_shot_type = 'Team'
            shot_data['OrebShotType'] = rebound_shot_type
        return shot_data

    @property
    def is_make_that_does_not_end_possession(self):
        """
        this is to make sure possession does not end if there are still FTs to shoot
        to get true and1s need to check the shooter is the player who drew the foul
        """
        # check for foul at time of shot
        shooter_team_id = self.team_id
        fouls_at_time_of_shot = []
        # ignore technical fouls and delay of game fouls when getting last foul
        events_at_shot_time = self.get_all_events_at_current_time()
        for event in events_at_shot_time:
            if isinstance(event, Foul) and not event.is_delay_of_game and not event.is_technical:
                fouls_at_time_of_shot.append(event)

        if len(fouls_at_time_of_shot) == 1:
            foul_event = fouls_at_time_of_shot[0]
            foul_team_team_id = foul_event.team_id

            if foul_event.is_flagrant:
                # flagrant foul and 1
                if foul_team_team_id != shooter_team_id:
                    return True

            other_makes_at_time_of_shot = []
            for event in events_at_shot_time:
                if isinstance(event, FieldGoal) and event.event_num != self.event_num and event.is_made and self.team_id == event.team_id:
                    other_makes_at_time_of_shot.append(event)
            if shooter_team_id != foul_team_team_id:
                # check FT 1 of 1s at time of shot
                ft_1_of_1s_at_time_of_shot = []
                for event in events_at_shot_time:
                    if isinstance(event, FreeThrow) and (event.is_ft_1_of_1 or event.is_ft_1pt) and not event.is_technical_ft:
                        ft_1_of_1s_at_time_of_shot.append(event)

                if len(other_makes_at_time_of_shot) == 1 and len(ft_1_of_1s_at_time_of_shot) == 1:
                    if ft_1_of_1s_at_time_of_shot[0].player1_id == other_makes_at_time_of_shot[0].player1_id:
                        return False
                    elif ft_1_of_1s_at_time_of_shot[0].player1_id == self.player1_id:
                        return True
                elif len(ft_1_of_1s_at_time_of_shot) > 0:
                    for ft_event in ft_1_of_1s_at_time_of_shot:
                        if ft_event.team_id == shooter_team_id:
                            return True
                else:
                    # no free throws - check for lane violation and offensive goaltending
                    for event in events_at_shot_time:
                        if isinstance(event, Turnover) and (event.is_lane_violation or event.is_offensive_goaltending):
                            return True
                        if isinstance(event, Violation) and event.is_double_lane_violation:
                            return True
        elif shooter_team_id not in [event.team_id for event in fouls_at_time_of_shot]:
            ft_1_of_1s_at_time_of_shot = []
            for event in events_at_shot_time:
                if isinstance(event, FreeThrow) and (event.is_ft_1_of_1 or event.is_ft_1pt) and not event.is_technical_ft:
                    ft_1_of_1s_at_time_of_shot.append(event)

            if len(ft_1_of_1s_at_time_of_shot) == 1:
                if ft_1_of_1s_at_time_of_shot[0].team_id == shooter_team_id:
                    return True
            elif len(ft_1_of_1s_at_time_of_shot) > 1:
                for ft_event in ft_1_of_1s_at_time_of_shot:
                    if ft_event.player1_id == self.player1_id:
                        return True
        else:
            opponent_fouls = [event for event in fouls_at_time_of_shot if event.team_id != shooter_team_id]
            if 1 in [event.number_of_fta_for_foul for event in opponent_fouls]:
                # rarely gets here but it is when there is an and1 and then another foul at the same time
                # for example a loose ball foul going for the rebound on the FT
                return True

        return False

    @property
    def event_stats(self):
        stats = []
        is_penalty_event = self.is_penalty_event()
        is_second_chance_event = self.is_second_chance_event()
        if self.distance is not None:
            if self.shot_value == 2:
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': pbpstats.TOTAL_2PT_SHOT_DISTANCE_STRING, 'stat_value': self.distance})
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': pbpstats.TOTAL_2PT_SHOTS_WITH_DISTANCE, 'stat_value': 1})
            else:
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': pbpstats.TOTAL_3PT_SHOT_DISTANCE_STRING, 'stat_value': self.distance})
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': pbpstats.TOTAL_3PT_SHOTS_WITH_DISTANCE, 'stat_value': 1})
                if self.is_heave:
                    if self.is_made:
                        stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': pbpstats.HEAVE_MAKES_STRING, 'stat_value': 1})
                    else:
                        stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': pbpstats.HEAVE_MISSES_STRING, 'stat_value': 1})

        team_ids = list(self.current_players.keys())
        opponent_team_id = team_ids[0] if self.team_id == team_ids[1] else team_ids[1]
        if self.is_made and not self.is_assisted:
            stat_key = f'{pbpstats.UNASSISTED_STRING}{self.shot_type}'
            stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': stat_key, 'stat_value': 1})
            if is_second_chance_event:
                second_chance_stat_key = f'{pbpstats.SECOND_CHANCE_STRING}{stat_key}'
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': second_chance_stat_key, 'stat_value': 1})
            if is_penalty_event:
                penalty_stat_key = f'{pbpstats.PENALTY_STRING}{stat_key}'
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': penalty_stat_key, 'stat_value': 1})
            if self.is_putback:
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': pbpstats.PUTBACKS_STRING, 'stat_value': 1})
        elif self.is_assisted:
            scorer_key = f'{pbpstats.ASSISTED_STRING}{self.shot_type}'
            assist_key = f'{self.shot_type}{pbpstats.ASSISTS_STRING}'
            stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': scorer_key, 'stat_value': 1})
            stats.append({'player_id': self.player2_id, 'team_id': self.team_id, 'stat_key': assist_key, 'stat_value': 1})
            if is_second_chance_event:
                second_chance_scorer_key = f'{pbpstats.SECOND_CHANCE_STRING}{scorer_key}'
                second_chance_assist_key = f'{pbpstats.SECOND_CHANCE_STRING}{assist_key}'
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': second_chance_scorer_key, 'stat_value': 1})
                stats.append({'player_id': self.player2_id, 'team_id': self.team_id, 'stat_key': second_chance_assist_key, 'stat_value': 1})
            if is_penalty_event:
                penalty_scorer_key = f'{pbpstats.PENALTY_STRING}{scorer_key}'
                penalty_assist_key = f'{pbpstats.PENALTY_STRING}{assist_key}'
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': penalty_scorer_key, 'stat_value': 1})
                stats.append({'player_id': self.player2_id, 'team_id': self.team_id, 'stat_key': penalty_assist_key, 'stat_value': 1})
            assist_to_key = f'{self.player2_id}:AssistsTo:{self.player1_id}:{self.shot_type}'
            stats.append({'player_id': self.player2_id, 'team_id': self.team_id, 'stat_key': assist_to_key, 'stat_value': 1})
        elif self.is_blocked:
            shot_key = f'{self.shot_type}{pbpstats.BLOCKED_STRING}'
            stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': shot_key, 'stat_value': 1})
            block_key = f'{pbpstats.BLOCKED_STRING}{self.shot_type}'
            stats.append({'player_id': self.player3_id, 'team_id': opponent_team_id, 'stat_key': block_key, 'stat_value': 1})
            if is_second_chance_event:
                second_chance_shot_key = f'{pbpstats.SECOND_CHANCE_STRING}{shot_key}'
                second_chance_block_key = f'{pbpstats.SECOND_CHANCE_STRING}{block_key}'
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': second_chance_shot_key, 'stat_value': 1})
                stats.append({'player_id': self.player3_id, 'team_id': opponent_team_id, 'stat_key': second_chance_block_key, 'stat_value': 1})
            if is_penalty_event:
                penalty_shot_key = f'{pbpstats.PENALTY_STRING}{shot_key}'
                penalty_block_key = f'{pbpstats.PENALTY_STRING}{block_key}'
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': penalty_shot_key, 'stat_value': 1})
                stats.append({'player_id': self.player3_id, 'team_id': opponent_team_id, 'stat_key': penalty_block_key, 'stat_value': 1})
        else:
            stat_key = f'{pbpstats.MISSED_STRING}{self.shot_type}'
            stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': stat_key, 'stat_value': 1})
            if is_second_chance_event:
                second_chance_stat_key = f'{pbpstats.SECOND_CHANCE_STRING}{stat_key}'
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': second_chance_stat_key, 'stat_value': 1})
            if is_penalty_event:
                penalty_stat_key = f'{pbpstats.PENALTY_STRING}{stat_key}'
                stats.append({'player_id': self.player1_id, 'team_id': self.team_id, 'stat_key': penalty_stat_key, 'stat_value': 1})

        if self.is_made:
            # add plus minus and opponent points - used for lineup/wowy stats to get net rating
            for team_id, players in self.current_players.items():
                multiplier = 1 if team_id == self.team_id else -1
                for player_id in players:
                    stat_item = {
                        'player_id': player_id,
                        'team_id': team_id,
                        'stat_key': pbpstats.PLUS_MINUS_STRING,
                        'stat_value': self.shot_value * multiplier,
                    }
                    stats.append(stat_item)
                    if multiplier == -1:
                        opponent_points_stat_item = {
                            'player_id': player_id,
                            'team_id': team_id,
                            'stat_key': pbpstats.OPPONENT_POINTS,
                            'stat_value': self.shot_value,
                        }
                        stats.append(opponent_points_stat_item)

        lineups_ids = self.lineup_ids
        for stat in stats:
            opponent_team_id = team_ids[0] if stat['team_id'] == team_ids[1] else team_ids[1]
            stat['lineup_id'] = lineups_ids[stat['team_id']]
            stat['opponent_team_id'] = opponent_team_id
            stat['opponent_lineup_id'] = lineups_ids[opponent_team_id]

        return self.base_stats + stats
