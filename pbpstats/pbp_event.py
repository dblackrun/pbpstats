import math

import pbpstats


class PbpEvent(object):
    """
    class for methods shared by DataPbpEvent and StatsPbpEvent objects
    """
    def __repr__(self):
        return f"<PbpEvent: Description: {self.description}, Time: {self.clock_time}, EventNum: {self.number}>"

    def is_made_fg(self):
        return self.etype == 1

    def is_missed_fg(self):
        return self.etype == 2

    def get_shot_distance(self):
        """
        returns shot distance in feet
        """
        if not(self.is_made_fg() or self.is_missed_fg()):
            return None
        if self.loc_x is not None:
            x_squared = self.loc_x ** 2
            y_squared = self.loc_y ** 2
            shot_distance = math.sqrt(x_squared + y_squared) / 10  # unit for distance is off by factor of 10, divide by 10 to convert to feet
            return round(shot_distance, 1)
        elif not self.is_3pt_shot():
            # no coordinates - get shot distance from event description
            try:
                return int(self.description.split("'")[0].split(' ')[-1])
            except:
                return None

    def is_corner_3(self):
        """
        checks if 3 was a corner 3
        loc_y <= 87:
        """
        if not self.is_3pt_shot():
            return False
        if self.loc_x is None:
            return False
        if self.loc_y <= 87:
            return True
        return False

    def get_shot_type(self):
        """
        returns shot type string - AtRim, ShortMidRange, LongMidRange, Corner3, Arc3
        """
        if not(self.is_made_fg() or self.is_missed_fg()):
            return None
        if self.is_3pt_shot():
            if self.is_corner_3():
                return pbpstats.CORNER_3_STRING
            else:
                return pbpstats.ARC_3_STRING

        else:
            shot_distance = self.get_shot_distance()
            if shot_distance < pbpstats.AT_RIM_CUTOFF:
                return pbpstats.AT_RIM_STRING
            elif shot_distance < pbpstats.SHORT_MID_RANGE_CUTOFF:
                return pbpstats.SHORT_MID_RANGE_STRING
            else:
                return pbpstats.LONG_MID_RANGE_STRING

    def is_made_ft(self):
        if self.etype == 3:
            return not self.is_missed_ft()
        return False

    def is_timeout(self):
        return self.etype == 9

    def is_substitution(self):
        return self.etype == 8

    def is_technical_foul(self):
        return self.etype == 6 and self.mtype in [11, 12, 13, 18, 19, 25, 30]

    def is_double_technical_foul(self):
        return self.etype == 6 and self.mtype == 16

    def is_ejection(self):
        return self.etype == 11

    def is_turnover(self):
        return self.etype == 5 and 'No Turnover' not in self.description

    def is_shot_clock_violation(self):
        return self.etype == 5 and self.mtype == 11

    def is_kicked_ball_violation_turnover(self):
        return self.etype == 5 and self.mtype == 19

    def is_replay_event(self):
        return self.etype == 18

    def is_replay_challenge_support_ruling(self):
        return self.etype == 18 and self.mtype == 4

    def is_replay_challenge_overturn_ruling(self):
        return self.etype == 18 and self.mtype == 5

    def is_replay_challenge_ruling_stands(self):
        return self.etype == 18 and self.mtype == 6

    def is_rebound(self):
        """
        checks if event is a rebound - etype == 4 and mtype == 0
        edge case where mtype is 1 on player rebound - not sure why

        returns bool
        """
        return self.etype == 4 and (self.mtype == 0 or self.player_id != '0')

    def is_putback(self):
        """
        checks if made basket was a putback
        putback defined as rebound within 2 seconds by the player who scored

        returns bool
        """
        if self.is_assisted_shot() or self.is_3pt_shot():
            return False
        prev_evt = self.previous_event
        if prev_evt is None:
            return False
        if (
            (prev_evt.get_foul_type() in [pbpstats.SHOOTING_BLOCK_TYPE_STRING, pbpstats.SHOOTING_FOUL_TYPE_STRING] or prev_evt.is_goaltend_violation()) and
            self.seconds_remaining == prev_evt.seconds_remaining
        ):
            # sometimes foul event is between rebound and shot on an and 1 or goaltend is between rebound and made shot event
            prev_evt = prev_evt.previous_event
            if prev_evt is None:
                return False
        if not prev_evt.is_rebound():
            return False
        rebound_data = prev_evt.get_rebound_data()
        if rebound_data is None:
            return False
        return (
            not rebound_data['def_reb'] and
            prev_evt.player_id == self.player_id and
            prev_evt.seconds_remaining - self.seconds_remaining <= 2
        )

    def is_foul(self):
        return self.etype == 6

    def get_foul_type(self):
        """
        returns foul type
        mtype:
            *1 - Personal
            *2 - Shooting
            *3 - Loose Ball
            *4 - Offensive
            *5 - Inbound foul (1 FTA)
            *6 - Away from play
            8 - Punch foul (Technical)
            *9 - Clear Path
            *10 - Double Foul
            11 - Technical
            12 - Non-Unsportsmanlike (Technical)
            13 - Hanging (Technical)
            *14 - Flagrant 1
            *15 - Flagrant 2
            16 - Double Technical
            *17 - Defensive 3 seconds (Technical)
            18 - Delay of game
            19 - Taunting (Technical)
            25 - Excess Timeout (Technical)
            *26 - Charge
            *27 - Personal Block
            *28 - Personal Take
            *29 - Shooting Block
            30 - Too many players (Technical)
        """
        if self.etype == 6:
            if self.mtype == 1:
                return pbpstats.PERSONAL_FOUL_TYPE_STRING
            if self.mtype == 2:
                return pbpstats.SHOOTING_FOUL_TYPE_STRING
            if self.mtype == 3:
                return pbpstats.LOOSE_BALL_FOUL_TYPE_STRING
            if self.mtype == 4:
                return pbpstats.OFFENSIVE_FOUL_TYPE_STRING
            if self.mtype == 5:
                return pbpstats.INBOUND_FOUL_TYPE_STRING
            if self.mtype == 6:
                return pbpstats.AWAY_FROM_PLAY_FOUL_TYPE_STRING
            if self.mtype == 9:
                return pbpstats.CLEAR_PATH_FOUL_TYPE_STRING
            if self.mtype == 10:
                return pbpstats.DOUBLE_FOUL_TYPE_STRING
            if self.mtype == 14:
                return pbpstats.FLAGRANT_1_FOUL_TYPE_STRING
            if self.mtype == 15:
                return pbpstats.FLAGRANT_2_FOUL_TYPE_STRING
            if self.mtype == 17:
                return pbpstats.DEFENSIVE_3_SECONDS_FOUL_TYPE_STRING
            if self.mtype == 26:
                return pbpstats.CHARGE_FOUL_TYPE_STRING
            if self.mtype == 27:
                return pbpstats.PERSONAL_BLOCK_TYPE_STRING
            if self.mtype == 28:
                return pbpstats.PERSONAL_TAKE_TYPE_STRING
            if self.mtype == 29:
                return pbpstats.SHOOTING_BLOCK_TYPE_STRING
        return None

    def is_foul_that_counts_toward_penalty(self):
        """
        checks if foul is a foul that counts toward the penalty - all defensive fouls and loose ball fouls count.
        """
        return self.etype == 6 and self.mtype in [1, 2, 3, 5, 6, 9, 15, 17, 27, 28, 29]

    def is_first_ft(self):
        return (self.is_made_ft() or self.is_missed_ft()) and ' 1 of ' in self.description

    def is_technical_ft(self):
        return (self.is_made_ft() or self.is_missed_ft()) and 'Free Throw Technical' in self.description

    def get_and1_shot(self):
        """
        gets shot that occurred at same time as foul, but before foul
        """
        previous_event = self
        while previous_event is not None and previous_event.seconds_remaining == self.seconds_remaining and not previous_event.is_made_fg():
            previous_event = previous_event.previous_event

        if previous_event is not None and previous_event.is_made_fg() and previous_event.seconds_remaining == self.seconds_remaining:
            return previous_event
        else:
            return None

    def get_foul_that_resulted_in_ft_excluding_techs(self):
        """
        gets foul that led to free throws
        """
        seconds_remaining = self.seconds_remaining
        # foul should be before FT so start by going backwards
        event = self
        while event is not None and event.seconds_remaining == seconds_remaining and not (event.is_foul() and not event.is_technical_foul() and not event.is_double_technical_foul()):
            event = event.previous_event

        if event is not None and event.is_foul() and not event.is_technical_foul() and not event.is_double_technical_foul() and event.seconds_remaining == seconds_remaining:
            return event

        # bug in pbp where foul is after FT
        event = self
        while event is not None and event.seconds_remaining == seconds_remaining and not (event.is_foul() and not event.is_technical_foul() and not event.is_double_technical_foul()):
            event = event.next_event

        if event is not None and event.is_foul() and not event.is_technical_foul() and not event.is_double_technical_foul() and event.seconds_remaining == seconds_remaining:
            return event
        return None

    def get_foul_that_resulted_in_ft(self):
        """
        gets foul that led to free throws, including technical FTs
        """
        seconds_remaining = self.seconds_remaining
        # foul should be before FT so start by going backwards
        event = self
        while event is not None and event.seconds_remaining == seconds_remaining and not event.is_foul():
            event = event.previous_event

        if event is not None and event.is_foul() and event.seconds_remaining == seconds_remaining:
            return event

        # bug in pbp where foul is after FT
        event = self
        while event is not None and event.seconds_remaining == seconds_remaining and not event.is_foul():
            event = event.next_event

        if event is not None and event.is_foul() and event.seconds_remaining == seconds_remaining:
            return event
        return None

    def is_start_of_period(self):
        return self.etype == 12 and self.mtype == 0

    def is_end_of_period(self):
        return self.etype == 13 and self.mtype == 0

    def is_delay_of_game(self):
        return self.etype == 6 and self.mtype == 18

    def is_ft_1_of_1(self):
        return self.etype == 3 and self.mtype == 10

    def is_ft_2_of_2(self):
        return self.etype == 3 and self.mtype == 12

    def is_ft_3_of_3(self):
        return self.etype == 3 and self.mtype == 15

    def is_jump_ball(self):
        return self.etype == 10

    def is_away_from_play_ft(self):
        """
        checks if final free throw is from an away from play foul
        used to determin if it should be a possession changing event
        FT 1 of 1 or FT 2 of 2 from away from play FT should not trigger possession change because team gets the ball back after FT
        away from play drawn at same time as team made shot should return False because you don't get the ball back after - it's like a normal and 1

        returns bool
        """
        foul = self.get_foul_that_resulted_in_ft_excluding_techs()
        if (self.is_ft_1_of_1() or self.is_ft_2_of_2()) and foul is not None and foul.get_foul_type() == pbpstats.AWAY_FROM_PLAY_FOUL_TYPE_STRING:
            made_shots_at_event_time = []
            fts_by_other_player_at_event_time = []
            events_at_event_time = self.get_all_events_at_event_time()
            for event in events_at_event_time:
                if event.is_made_fg():
                    made_shots_at_event_time.append(event)
                if event.is_made_ft() and event.player_id != self.player_id:
                    fts_by_other_player_at_event_time.append(event)

            if len(made_shots_at_event_time) == 0:
                # check for made free throw by other player - edge case where player is fouled going for rebound on made FT
                if len(fts_by_other_player_at_event_time) == 0:
                    return True
                else:
                    for ft in fts_by_other_player_at_event_time:
                        if ft.team_id != self.team_id:
                            return True
            else:
                made_shots_at_event_time = sorted(made_shots_at_event_time, key=lambda k: k.order)
                if (made_shots_at_event_time[0].team_id == foul.team_id) and (self.player_id != made_shots_at_event_time[0].player_id):
                    # make sure player who made shot is not player who shot FT
                    return True

        return False

    def is_inbound_foul_ft(self):
        """
        checks if free throw is from a inbound foul

        returns bool
        """
        if self.is_ft_1_of_1():
            events_at_event_time = self.get_all_events_at_event_time()
            for event in events_at_event_time:
                if event.get_foul_type() == pbpstats.INBOUND_FOUL_TYPE_STRING:
                    return True

        return False

    def is_lane_violation_turnover(self):
        return self.etype == 5 and self.mtype == 17

    def is_lane_violation(self):
        return self.etype == 7 and self.mtype == 3

    def is_double_lane_violation(self):
        return self.etype == 7 and self.mtype == 6

    def is_goaltend_violation(self):
        return self.etype == 7 and self.mtype == 2

    def is_offensive_goaltending(self):
        return self.etype == 5 and self.mtype == 15

    def is_travel(self):
        return self.etype == 5 and self.mtype == 4

    def is_3_second_violation(self):
        return self.etype == 5 and self.mtype == 8

    def is_step_out_of_bounds_turnover(self):
        return self.etype == 5 and self.mtype == 39

    def is_lost_ball_turnover(self):
        return self.etype == 5 and self.mtype == 2

    def is_lost_ball_out_of_bounds_turnover(self):
        return self.etype == 5 and self.mtype == 40

    def is_bad_pass_turnover(self):
        return self.etype == 5 and self.mtype == 1

    def is_bad_pass_out_of_bounds_turnover(self):
        return self.etype == 5 and self.mtype == 45

    def is_jumpball_violation(self):
        return self.etype == 7 and self.mtype == 4

    def is_and1_shot(self):
        """
        checks if there was a foul on a made shot
        """
        # check for foul at time of shot
        shooter_team_id = self.team_id
        fouls_at_time_of_shot = []
        # ignore technical fouls and delay of game fouls when getting last foul
        events_at_event_time = self.get_all_events_at_event_time()
        for event in events_at_event_time:
            if event.is_foul() and not event.is_delay_of_game() and not event.is_technical_foul():
                fouls_at_time_of_shot.append(event)

        if len(fouls_at_time_of_shot) == 1:
            foul_event = fouls_at_time_of_shot[0]
            foul_team_team_id = foul_event.team_id

            if foul_event.get_foul_type() in [pbpstats.FLAGRANT_1_FOUL_TYPE_STRING, pbpstats.FLAGRANT_2_FOUL_TYPE_STRING]:
                # flagrant foul and 1
                if foul_team_team_id != shooter_team_id:
                    return True

            if shooter_team_id != foul_team_team_id:
                # check FT 1 of 1s at time of shot
                ft_1_of_1s_at_time_of_shot = []
                for event in events_at_event_time:
                    if event.is_ft_1_of_1() and not event.is_technical_ft():
                        ft_1_of_1s_at_time_of_shot.append(event)

                if len(ft_1_of_1s_at_time_of_shot) != 0:
                    for ft_event in ft_1_of_1s_at_time_of_shot:
                        if ft_event.team_id == shooter_team_id:
                            return True
                else:
                    # no free throws - check for lane violation and offensive goaltending
                    for event in events_at_event_time:
                        if event.is_lane_violation_turnover() or event.is_double_lane_violation() or event.is_offensive_goaltending():
                            return True
        elif shooter_team_id not in [event.team_id for event in fouls_at_time_of_shot]:
            ft_1_of_1s_at_time_of_shot = []
            for event in events_at_event_time:
                if event.is_ft_1_of_1() and not event.is_technical_ft():
                    ft_1_of_1s_at_time_of_shot.append(event)

            if len(ft_1_of_1s_at_time_of_shot) == 1:
                if ft_1_of_1s_at_time_of_shot[0].team_id == shooter_team_id:
                    return True
            elif len(ft_1_of_1s_at_time_of_shot) > 1:
                for ft_event in ft_1_of_1s_at_time_of_shot:
                    if ft_event.player_id == self.player_id:
                        return True
        else:
            opponent_fouls = [event for event in fouls_at_time_of_shot if event.team_id != shooter_team_id]
            if 1 in [event.get_number_of_fta_for_foul() for event in opponent_fouls]:
                return True

        return False

    def get_rebound_data(self):
        """
        Finds event for each rebound to determine rebound and shot type for each rebound
        self should be rebound event
        Returns:
        dict with additional data on rebound and shot that was rebounded
        """
        next_event = self.next_event
        if next_event is not None and next_event.is_replay_event():
            # ignore replay event when checking if next event is end of period
            next_event = next_event.next_event
        if (
            (self.clock_time == '00:00.0' or self.clock_time == '0:00') and
            self.player_id == '0' and
            ((next_event is not None and next_event.is_end_of_period()) or next_event is None)
        ):
            # 00:00.0 is data.nba.com, 0:00 is stats.nba.com
            # Ignore team rebounds at end of period since they aren't actual rebounds, they are just placeholder events
            return None
        else:
            # ignore if shot clock violation at time of team rebond shot clock violation etype == 5 mtype == 11
            # these get logged as team rebounds but they aren't actual rebounds, they are turnovers
            events_at_event_time = self.get_all_events_at_event_time()
            for event in events_at_event_time:
                if (event.is_shot_clock_violation() or event.is_kicked_ball_violation_turnover()) and self.player_id == '0':
                    return None

            rebound_player_id = None
            shooter_player_id = None
            player_reb = True
            player_id = self.player_id
            if player_id == '0':
                # team rebound if pid is 0
                rebound_team_id = self.team_id
                player_reb = False
            else:
                # player rebound
                rebound_team_id = self.team_id
                rebound_player_id = player_id

            event = self.previous_event
            while event is not None and not (event.is_missed_ft() or event.is_missed_fg()):
                event = event.previous_event
            last_miss_before_rebound = event

            if last_miss_before_rebound is not None:
                # sometimes rebound on buzzer beater is given the same time as shot - don't count these
                if last_miss_before_rebound.seconds_remaining <= 3 and self.seconds_remaining == last_miss_before_rebound.seconds_remaining and self.player_id == '0':
                    # only don't count if rebound is last event before end of period event
                    if self.next_event is not None and self.next_event.is_end_of_period():
                        return None

                shooter_team_id = last_miss_before_rebound.team_id
                shooter_player_id = last_miss_before_rebound.player_id
                # check if missed shot was rebounded by player who took the shot
                own_miss = shooter_player_id == rebound_player_id

                # check if missed shot as a 3 point attempt
                three = last_miss_before_rebound.is_3pt_shot()

                # check if defensive rebound
                def_reb = rebound_team_id != shooter_team_id

                # check if missed shot was a free throw
                ft = False
                if last_miss_before_rebound.is_missed_ft():
                    if not (last_miss_before_rebound.is_ft_1_of_1() or last_miss_before_rebound.is_ft_2_of_2() or last_miss_before_rebound.is_ft_3_of_3()):
                        return None
                    ft = True
            else:
                return None

            return {
                'def_reb': def_reb,
                'player_reb': player_reb,
                'player_id': rebound_player_id,
                'team_id': rebound_team_id,
                'ft': ft,
                'three': three,
                'self': own_miss,
                'current_players': self.current_players if hasattr(self, 'current_players') else None,
                'rebounded_shot': last_miss_before_rebound,
            }

    def is_tracked_event(self):
        """
        returns True if event is an event that should trigger a counting stat getting incremented
        """
        if self.is_turnover():
            return True
        if self.is_foul():
            return True
        if self.is_first_ft() or self.is_technical_ft():
            return True
        if self.is_made_fg():
            return True
        if self.is_missed_fg():
            return True
        if self.is_made_ft():
            return True
        if self.is_rebound():
            return True
        if self.is_goaltend_violation():
            return True
        if self.is_replay_challenge_overturn_ruling() or self.is_replay_challenge_ruling_stands() or self.is_replay_challenge_support_ruling():
            return True

        return False

    def is_second_chance_event(self, possession_events):
        """
        checks whether event is after an offensive rebound on the possession
        """
        possession_start_event = possession_events[0]
        event = self
        while event.number != possession_start_event.number and event.previous_event is not None:
            if event.is_rebound():
                rebound_data = event.get_rebound_data()
                if rebound_data is not None and not rebound_data['def_reb']:
                    return True
            event = event.previous_event

        return False

    def get_all_events_at_event_time(self):
        """
        gets all events at current event time
        returns list ordered ascendingly by event order
        """
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
